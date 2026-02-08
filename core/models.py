from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional


class ScanType(str, Enum):
    EXACT = "exact"
    UNKNOWN = "unknown"
    INCREASED = "increased"
    DECREASED = "decreased"
    UNCHANGED = "unchanged"
    CHANGED = "changed"


class ValueType(str, Enum):
    INT32 = "int32"
    INT64 = "int64"
    FLOAT = "float"
    DOUBLE = "double"
    STRING_UTF8 = "string_utf8"
    STRING_UTF16 = "string_utf16"
    AOB = "aob"


@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    name: str
    path: Optional[str]


@dataclass(frozen=True)
class MemoryRegion:
    base: int
    size: int
    readable: bool
    writable: bool
    executable: bool


@dataclass(frozen=True)
class ScanResult:
    address: int
    value: bytes
    region: MemoryRegion


@dataclass
class Snapshot:
    results: list[ScanResult]

    def addresses(self) -> Iterable[int]:
        return (result.address for result in self.results)
