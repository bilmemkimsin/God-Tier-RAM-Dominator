from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KernelReadRequest:
    pid: int
    address: int
    size: int


@dataclass(frozen=True)
class KernelWriteRequest:
    pid: int
    address: int
    data: bytes


class KernelDriverClient:
    """User-mode client placeholder for kernel RW driver IOCTLs."""

    def __init__(self, device_path: str = r"\\.\TitanRW") -> None:
        self.device_path = device_path

    def read(self, request: KernelReadRequest) -> bytes:
        raise NotImplementedError("Kernel driver communication not implemented in this sample.")

    def write(self, request: KernelWriteRequest) -> None:
        raise NotImplementedError("Kernel driver communication not implemented in this sample.")
