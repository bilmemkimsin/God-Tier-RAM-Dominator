from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .memory import MemoryBackend


@dataclass(frozen=True)
class PointerChain:
    base_address: int
    offsets: list[int]

    def to_expression(self) -> str:
        offsets = "+".join(hex(offset) for offset in self.offsets)
        return f"[0x{self.base_address:x}] + {offsets}" if offsets else f"[0x{self.base_address:x}]"


class PointerScanner:
    def __init__(self, backend: MemoryBackend) -> None:
        self.backend = backend

    def scan(self, target_address: int, max_depth: int = 5, step: int = 4) -> Iterable[PointerChain]:
        if max_depth < 1:
            return []
        chains: list[PointerChain] = []
        for region in self.backend.regions():
            data = self.backend.read(region.base, region.size)
            for offset in range(0, len(data) - step + 1, step):
                candidate = int.from_bytes(data[offset : offset + step], "little")
                if candidate == target_address:
                    chains.append(PointerChain(base_address=region.base + offset, offsets=[]))
        return chains
