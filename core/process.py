from __future__ import annotations

import platform
from dataclasses import dataclass
from typing import Iterable, Optional

from .models import ProcessInfo

try:
    import psutil
except ImportError:  # pragma: no cover - handled with helpful error
    psutil = None


@dataclass
class ProcessHandle:
    pid: int
    name: str
    path: Optional[str]


class ProcessLister:
    def list_processes(self) -> Iterable[ProcessInfo]:
        if psutil is None:
            raise RuntimeError("psutil is required for process enumeration.")
        for proc in psutil.process_iter(attrs=["pid", "name", "exe"]):
            info = proc.info
            yield ProcessInfo(pid=info["pid"], name=info.get("name") or "?", path=info.get("exe"))


class ProcessAttacher:
    def attach(self, pid: int) -> ProcessHandle:
        if psutil is None:
            raise RuntimeError("psutil is required for process attach.")
        proc = psutil.Process(pid)
        return ProcessHandle(pid=pid, name=proc.name(), path=proc.exe() if proc.exe() else None)

    @property
    def platform(self) -> str:
        return platform.system().lower()
