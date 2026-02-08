from __future__ import annotations

import ctypes
import platform
from dataclasses import dataclass
from typing import Iterable, Protocol

from .models import MemoryRegion


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
    def for_platform(handle: int | None = None) -> MemoryBackend:
        if platform.system().lower() == "windows":
            if handle is None:
                raise ValueError("Windows backend requires a process handle.")
            return WindowsMemoryBackend(handle=handle)
        raise NotImplementedError("Memory backend only implemented for Windows; use MockMemoryBackend in tests.")
