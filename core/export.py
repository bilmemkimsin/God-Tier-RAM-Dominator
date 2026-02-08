from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CheatEntry:
    description: str
    address: int
    data_type: str


class CheatEngineExporter:
    def export(self, entries: Iterable[CheatEntry], output: Path) -> None:
        lines = [
            "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
            "<CheatTable>\n  <CheatEntries>",
        ]
        for entry in entries:
            lines.append(
                "    <CheatEntry>\n"
                f"      <Description>\"{entry.description}\"</Description>\n"
                f"      <Address>{hex(entry.address)}</Address>\n"
                f"      <Type>{entry.data_type}</Type>\n"
                "    </CheatEntry>"
            )
        lines.append("  </CheatEntries>\n</CheatTable>")
        output.write_text("\n".join(lines), encoding="utf-8")
