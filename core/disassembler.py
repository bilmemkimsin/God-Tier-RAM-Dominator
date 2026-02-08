from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
except ImportError:  # pragma: no cover
    Cs = None
    CS_ARCH_X86 = None
    CS_MODE_64 = None

try:
    from keystone import Ks, KS_ARCH_X86, KS_MODE_64
except ImportError:  # pragma: no cover
    Ks = None
    KS_ARCH_X86 = None
    KS_MODE_64 = None


@dataclass(frozen=True)
class Instruction:
    address: int
    mnemonic: str
    op_str: str


class Disassembler:
    def __init__(self) -> None:
        if Cs is None:
            raise RuntimeError("capstone is required for disassembly.")
        self.engine = Cs(CS_ARCH_X86, CS_MODE_64)

    def disassemble(self, code: bytes, address: int) -> Iterable[Instruction]:
        for insn in self.engine.disasm(code, address):
            yield Instruction(address=insn.address, mnemonic=insn.mnemonic, op_str=insn.op_str)


class Assembler:
    def __init__(self) -> None:
        if Ks is None:
            raise RuntimeError("keystone is required for assembly.")
        self.engine = Ks(KS_ARCH_X86, KS_MODE_64)

    def assemble(self, asm: str, address: int = 0) -> bytes:
        encoding, _ = self.engine.asm(asm, addr=address)
        return bytes(encoding)
