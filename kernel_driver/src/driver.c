#include <ntddk.h>

#define DEVICE_NAME L"\\Device\\TitanRW"
#define SYMLINK_NAME L"\\DosDevices\\TitanRW"

#define IOCTL_TITAN_READ  CTL_CODE(FILE_DEVICE_UNKNOWN, 0x801, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define IOCTL_TITAN_WRITE CTL_CODE(FILE_DEVICE_UNKNOWN, 0x802, METHOD_BUFFERED, FILE_ANY_ACCESS)

typedef struct _RW_REQUEST {
    ULONG pid;
    ULONGLONG address;
    ULONG size;
    UCHAR data[1];
} RW_REQUEST, *PRW_REQUEST;

void DriverUnload(PDRIVER_OBJECT DriverObject) {
    UNICODE_STRING symLink = RTL_CONSTANT_STRING(SYMLINK_NAME);
    IoDeleteSymbolicLink(&symLink);
    IoDeleteDevice(DriverObject->DeviceObject);
}

NTSTATUS ReadProcessMemory(ULONG pid, ULONGLONG address, PVOID buffer, ULONG size) {
    PEPROCESS target = NULL;
    NTSTATUS status = PsLookupProcessByProcessId((HANDLE)(ULONG_PTR)pid, &target);
    if (!NT_SUCCESS(status)) {
        return status;
    }
    SIZE_T bytes = 0;
    status = MmCopyVirtualMemory(target, PsGetCurrentProcess(), (PVOID)(ULONG_PTR)address,
                                 PsGetCurrentProcess(), buffer, size, KernelMode, &bytes);
    ObDereferenceObject(target);
    return status;
}

NTSTATUS WriteProcessMemory(ULONG pid, ULONGLONG address, PVOID buffer, ULONG size) {
    PEPROCESS target = NULL;
    NTSTATUS status = PsLookupProcessByProcessId((HANDLE)(ULONG_PTR)pid, &target);
    if (!NT_SUCCESS(status)) {
        return status;
    }
    SIZE_T bytes = 0;
    status = MmCopyVirtualMemory(PsGetCurrentProcess(), target, buffer,
                                 (PVOID)(ULONG_PTR)address, size, KernelMode, &bytes);
    ObDereferenceObject(target);
    return status;
}

NTSTATUS DeviceControl(PDEVICE_OBJECT DeviceObject, PIRP Irp) {
    UNREFERENCED_PARAMETER(DeviceObject);
    PIO_STACK_LOCATION stack = IoGetCurrentIrpStackLocation(Irp);
    ULONG controlCode = stack->Parameters.DeviceIoControl.IoControlCode;
    NTSTATUS status = STATUS_INVALID_DEVICE_REQUEST;

    PRW_REQUEST request = (PRW_REQUEST)Irp->AssociatedIrp.SystemBuffer;
    if (request == NULL) {
        status = STATUS_INVALID_PARAMETER;
    } else if (controlCode == IOCTL_TITAN_READ) {
        status = ReadProcessMemory(request->pid, request->address, request->data, request->size);
        Irp->IoStatus.Information = request->size;
    } else if (controlCode == IOCTL_TITAN_WRITE) {
        status = WriteProcessMemory(request->pid, request->address, request->data, request->size);
        Irp->IoStatus.Information = 0;
    }

    Irp->IoStatus.Status = status;
    IoCompleteRequest(Irp, IO_NO_INCREMENT);
    return status;
}

NTSTATUS CreateClose(PDEVICE_OBJECT DeviceObject, PIRP Irp) {
    UNREFERENCED_PARAMETER(DeviceObject);
    Irp->IoStatus.Status = STATUS_SUCCESS;
    Irp->IoStatus.Information = 0;
    IoCompleteRequest(Irp, IO_NO_INCREMENT);
    return STATUS_SUCCESS;
}

NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
    UNREFERENCED_PARAMETER(RegistryPath);

    UNICODE_STRING deviceName = RTL_CONSTANT_STRING(DEVICE_NAME);
    UNICODE_STRING symLink = RTL_CONSTANT_STRING(SYMLINK_NAME);
    PDEVICE_OBJECT deviceObject = NULL;

    NTSTATUS status = IoCreateDevice(
        DriverObject,
        0,
        &deviceName,
        FILE_DEVICE_UNKNOWN,
        FILE_DEVICE_SECURE_OPEN,
        FALSE,
        &deviceObject
    );
    if (!NT_SUCCESS(status)) {
        return status;
    }

    status = IoCreateSymbolicLink(&symLink, &deviceName);
    if (!NT_SUCCESS(status)) {
        IoDeleteDevice(deviceObject);
        return status;
    }

    DriverObject->MajorFunction[IRP_MJ_CREATE] = CreateClose;
    DriverObject->MajorFunction[IRP_MJ_CLOSE] = CreateClose;
    DriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = DeviceControl;
    DriverObject->DriverUnload = DriverUnload;

    return STATUS_SUCCESS;
}
