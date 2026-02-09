from __future__ import annotations

import ctypes
import platform
from dataclasses import dataclass
from typing import Iterable, Protocol

from .models import MemoryRegion
from .write_audit import UndoSnapshot, UndoStack, WriteAuditLog, WriteEvent


class MemoryBackend(Protocol):
    def regions(self) -> Iterable[MemoryRegion]:
        ...

    def read(self, address: int, size: int) -> bytes:
        ...

    def write(self, address: int, data: bytes) -> None:
        ...


@dataclass
class WindowsMemoryBackend:
    handle: int
    pid: int
    audit_log: WriteAuditLog
    undo_stack: UndoStack

    def regions(self) -> Iterable[MemoryRegion]:
        raise NotImplementedError("Region enumeration requires platform bindings.")

    def read(self, address: int, size: int) -> bytes:
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t(0)
        result = ctypes.windll.kernel32.ReadProcessMemory(
            self.handle,
            ctypes.c_void_p(address),
            buffer,
            size,
            ctypes.byref(bytes_read),
        )
        if not result:
            raise OSError("ReadProcessMemory failed.")
        return buffer.raw[: bytes_read.value]

    def write(self, address: int, data: bytes) -> None:
        before = self.read(address, len(data))
        bytes_written = ctypes.c_size_t(0)
        result = ctypes.windll.kernel32.WriteProcessMemory(
            self.handle,
            ctypes.c_void_p(address),
            data,
            len(data),
            ctypes.byref(bytes_written),
        )
        if not result:
            raise OSError("WriteProcessMemory failed.")
        self.undo_stack.push(UndoSnapshot(pid=self.pid, address=address, data=before))
        self.audit_log.record(
            WriteEvent(
                timestamp=self.audit_log.now(),
                pid=self.pid,
                address=address,
                before=before,
                after=data,
                reason="user_write",
            )
        )


@dataclass
class MockMemoryBackend:
    buffer: bytearray

    def regions(self) -> Iterable[MemoryRegion]:
        return [MemoryRegion(base=0, size=len(self.buffer), readable=True, writable=True, executable=False)]

    def read(self, address: int, size: int) -> bytes:
        return bytes(self.buffer[address : address + size])

    def write(self, address: int, data: bytes) -> None:
        self.buffer[address : address + len(data)] = data


class MemoryBackendFactory:
    @staticmethod
    def for_platform(handle: int | None = None, pid: int | None = None) -> MemoryBackend:
        if platform.system().lower() == "windows":
            if handle is None:
                raise ValueError("Windows backend requires a process handle.")
            if pid is None:
                raise ValueError("Windows backend requires a pid for auditing.")
            return WindowsMemoryBackend(handle=handle, pid=pid, audit_log=WriteAuditLog(), undo_stack=UndoStack())
        raise NotImplementedError("Memory backend only implemented for Windows; use MockMemoryBackend in tests.")
