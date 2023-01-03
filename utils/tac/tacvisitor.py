from __future__ import annotations
from .tacinstr import *


class TACVisitor:

    def visitOther(self, instr: TACInstr) -> None:
        pass

    # * Step 9
    def visitParam(self, instr: Param) -> None:
        self.visitOther(instr)

    # * Step 9
    def visitCall(self, instr: Call) -> None:
        self.visitOther(instr)

    # * Step 10
    def visitLoadSymbol(self, instr: LoadSymbol) -> None:
        self.visitOther(instr)

    # * Step 10
    def visitLoadW(self, instr: LoadW) -> None:
        self.visitOther(instr)

    # * Step 10
    def visitStoreW(self, instr: StoreW) -> None:
        self.visitOther(instr)

    def visitAssign(self, instr: Assign) -> None:
        self.visitOther(instr)

    def visitLoadImm4(self, instr: LoadImm4) -> None:
        self.visitOther(instr)

    def visitUnary(self, instr: Unary) -> None:
        self.visitOther(instr)

    def visitBinary(self, instr: Binary) -> None:
        self.visitOther(instr)

    def visitBranch(self, instr: Branch) -> None:
        self.visitOther(instr)

    def visitCondBranch(self, instr: CondBranch) -> None:
        self.visitOther(instr)

    def visitReturn(self, instr: Return) -> None:
        self.visitOther(instr)

    def visitMemo(self, instr: Memo) -> None:
        self.visitOther(instr)

    def visitMark(self, instr: Mark) -> None:
        self.visitOther(instr)
