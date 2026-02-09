"""Example script showing how a cheat might look using TitanRAM APIs."""

from core.memory import MockMemoryBackend
from core.scanner import MemoryScanner, ScanConfig
from core.models import ScanType, ValueType


buffer = bytearray(b"\x00" * 64)
buffer[16:20] = (100).to_bytes(4, "little", signed=True)
backend = MockMemoryBackend(buffer)
scanner = MemoryScanner(backend)

snapshot = scanner.scan(ScanConfig(scan_type=ScanType.EXACT, value_type=ValueType.INT32, value="100"))
print("Found:", [hex(result.address) for result in snapshot.results])
