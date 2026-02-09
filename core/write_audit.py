from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class WriteEvent:
    timestamp: str
    pid: int
    address: int
    before: bytes
    after: bytes
    reason: str


@dataclass
class WriteAuditLog:
    path: Path = field(default_factory=lambda: Path("logs/write_audit.jsonl"))

    def record(self, event: WriteEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "timestamp": event.timestamp,
            "pid": event.pid,
            "address": hex(event.address),
            "before": event.before.hex(),
            "after": event.after.hex(),
            "reason": event.reason,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")

    @staticmethod
    def now() -> str:
        return datetime.now(tz=timezone.utc).isoformat()


@dataclass
class UndoSnapshot:
    pid: int
    address: int
    data: bytes


@dataclass
class UndoStack:
    _items: list[UndoSnapshot] = field(default_factory=list)

    def push(self, snapshot: UndoSnapshot) -> None:
        self._items.append(snapshot)

    def pop(self) -> UndoSnapshot | None:
        if not self._items:
            return None
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)

    def items(self) -> Iterable[UndoSnapshot]:
        return list(self._items)
