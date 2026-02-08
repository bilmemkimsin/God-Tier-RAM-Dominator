from core.memory import MockMemoryBackend
from core.models import ScanType, ValueType
from core.scanner import MemoryScanner, ScanConfig


def test_exact_scan_int32() -> None:
    buffer = bytearray(b"\x00" * 32)
    buffer[8:12] = (1337).to_bytes(4, "little", signed=True)
    backend = MockMemoryBackend(buffer)
    scanner = MemoryScanner(backend)

    snapshot = scanner.scan(ScanConfig(scan_type=ScanType.EXACT, value_type=ValueType.INT32, value="1337"))
    assert [result.address for result in snapshot.results] == [8]


def test_next_scan_increased() -> None:
    buffer = bytearray(b"\x00" * 32)
    buffer[4:8] = (10).to_bytes(4, "little", signed=True)
    backend = MockMemoryBackend(buffer)
    scanner = MemoryScanner(backend)

    scanner.scan(ScanConfig(scan_type=ScanType.EXACT, value_type=ValueType.INT32, value="10"))
    backend.write(4, (20).to_bytes(4, "little", signed=True))

    snapshot = scanner.next_scan(ScanConfig(scan_type=ScanType.INCREASED, value_type=ValueType.INT32, value="20"))
    assert [result.address for result in snapshot.results] == [4]
