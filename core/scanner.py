from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Iterable, Optional

from .memory import MemoryBackend
from .models import MemoryRegion, ScanResult, ScanType, Snapshot, ValueType


@dataclass
class ScanConfig:
    scan_type: ScanType
    value_type: ValueType
    value: Optional[str] = None
    alignment: int = 1


class MemoryScanner:
    def __init__(self, backend: MemoryBackend) -> None:
        self.backend = backend
        self._previous_snapshot: Optional[Snapshot] = None

    def scan(self, config: ScanConfig) -> Snapshot:
        regions = [region for region in self.backend.regions() if region.readable]
        results: list[ScanResult] = []

        for region in regions:
            data = self.backend.read(region.base, region.size)
            results.extend(self._scan_region(region, data, config))

        snapshot = Snapshot(results=results)
        self._previous_snapshot = snapshot
        return snapshot

    def next_scan(self, config: ScanConfig) -> Snapshot:
        if self._previous_snapshot is None:
            raise RuntimeError("No previous snapshot to compare.")
        previous = self._previous_snapshot
        results: list[ScanResult] = []

        for result in previous.results:
            current = self.backend.read(result.address, len(result.value))
            if self._matches_transition(result.value, current, config.scan_type):
                results.append(ScanResult(address=result.address, value=current, region=result.region))

        snapshot = Snapshot(results=results)
        self._previous_snapshot = snapshot
        return snapshot

    def _scan_region(self, region: MemoryRegion, data: bytes, config: ScanConfig) -> Iterable[ScanResult]:
        step = max(1, config.alignment)
        if config.scan_type == ScanType.UNKNOWN:
            for offset in range(0, len(data), step):
                chunk = data[offset : offset + step]
                if chunk:
                    yield ScanResult(address=region.base + offset, value=chunk, region=region)
            return

        if config.value is None:
            raise ValueError("Value required for this scan type.")
        pattern = self._encode_value(config.value_type, config.value)
        for offset in range(0, len(data) - len(pattern) + 1, step):
            chunk = data[offset : offset + len(pattern)]
            if self._matches_value(chunk, pattern, config.scan_type):
                yield ScanResult(address=region.base + offset, value=chunk, region=region)

    def _matches_value(self, chunk: bytes, pattern: bytes, scan_type: ScanType) -> bool:
        if scan_type == ScanType.EXACT:
            return chunk == pattern
        return False

    def _matches_transition(self, before: bytes, after: bytes, scan_type: ScanType) -> bool:
        if scan_type == ScanType.UNCHANGED:
            return before == after
        if scan_type == ScanType.CHANGED:
            return before != after
        if len(before) == len(after) == 4:
            before_val = int.from_bytes(before, "little", signed=True)
            after_val = int.from_bytes(after, "little", signed=True)
            if scan_type == ScanType.INCREASED:
                return after_val > before_val
            if scan_type == ScanType.DECREASED:
                return after_val < before_val
        return False

    def _encode_value(self, value_type: ValueType, value: str) -> bytes:
        if value_type == ValueType.INT32:
            return int(value).to_bytes(4, "little", signed=True)
        if value_type == ValueType.INT64:
            return int(value).to_bytes(8, "little", signed=True)
        if value_type == ValueType.FLOAT:
            return struct.pack("<f", float(value))
        if value_type == ValueType.DOUBLE:
            return struct.pack("<d", float(value))
        if value_type == ValueType.STRING_UTF8:
            return value.encode("utf-8")
        if value_type == ValueType.STRING_UTF16:
            return value.encode("utf-16-le")
        if value_type == ValueType.AOB:
            clean = value.replace(" ", "")
            return bytes.fromhex(clean)
        raise ValueError(f"Unsupported value type: {value_type}")
