from curses.ascii import SUB
from typing import Sequence, Tuple

from backend.asmemitter import AsmEmitter
from utils.error import IllegalArgumentException
from utils.label.label import Label, LabelKind
from utils.riscv import Riscv
from utils.tac.reg import Reg
from utils.tac.tacfunc import TACFunc
from utils.tac.tacinstr import *
from utils.tac.tacvisitor import TACVisitor
from frontend.symbol.varsymbol import VarSymbol
from ..subroutineemitter import SubroutineEmitter
from ..subroutineinfo import SubroutineInfo

"""
RiscvAsmEmitter: an AsmEmitter for RiscV
"""


class RiscvAsmEmitter(AsmEmitter):
    def __init__(
        self,
        allocatableRegs: list[Reg],
        callerSaveRegs: list[Reg],
        global_vars: list[VarSymbol]
    ) -> None:
        super().__init__(allocatableRegs, callerSaveRegs)

        # * Step 10 done
        # * Step 11 done
        # ? data 段为已初始化的全局变量（不包括全局数组）
        # ? bss 段为未初始化的全局变量
        _data = []
        _bss = []

        for var in global_vars:
            if not var.isArray and var.initValue != 0:
                _data.append(var)
            else:
                _bss.append(var)

        if len(_data) > 0:
            self.printer.println(".data")
            globl_vars = ','.join([var.name for var in _data])
            self.printer.println(f".globl {globl_vars}")
            for var in _data:
                self.printer.println(f"{var.name}: ")
                self.printer.println(f".word {var.initValue}")
            self.printer.println("")

        if len(_bss) > 0:
            self.printer.println(".bss")
            globl_vars = ','.join([var.name for var in _bss])
            self.printer.println(f".globl {globl_vars}")
            for var in _bss:
                self.printer.println(f"{var.name}: ")
                self.printer.println(f".space {var.type.type.size}")
            self.printer.println("")

        # the start of the asm code
        # int step10, you need to add the declaration of global var here
        self.printer.println(".text")
        self.printer.println(".global main")
        self.printer.println("")

    # ? transform tac instrs to RiscV instrs
    # ? collect some info which is saved in SubroutineInfo for SubroutineEmitter
    def selectInstr(self, func: TACFunc) -> tuple[list[str], SubroutineInfo]:

        selector: RiscvAsmEmitter.RiscvInstrSelector = (
            RiscvAsmEmitter.RiscvInstrSelector(func.entry)
        )

        for i in range(len(func.params)):
            temp = func.params[i]
            if i <= 7:
                selector.seq.append(Riscv.LoadReg(
                    temp, Riscv.ArgRegs[i]
                ))
            else:
                selector.seq.append(Riscv.LoadOffsetReg(
                    temp, Riscv.FP, i * 4
                ))

        for instr in func.getInstrSeq():
            instr.accept(selector)

        info = SubroutineInfo(func.entry)

        return (selector.seq, info)

    # use info to construct a RiscvSubroutineEmitter
    def emitSubroutine(self, info: SubroutineInfo):
        return RiscvSubroutineEmitter(self, info)

    # return all the string stored in asmcodeprinter
    def emitEnd(self):
        return self.printer.close()

    class RiscvInstrSelector(TACVisitor):
        def __init__(self, entry: Label) -> None:
            self.entry = entry
            self.seq = []

        # in step11, you need to think about how to deal with globalTemp in almost all the visit functions.
        def visitReturn(self, instr: Return) -> None:
            if instr.value is not None:
                self.seq.append(Riscv.Move(Riscv.A0, instr.value))
            else:
                self.seq.append(Riscv.LoadImm(Riscv.A0, 0))
            self.seq.append(Riscv.JumpToEpilogue(self.entry))

        def visitMark(self, instr: Mark) -> None:
            self.seq.append(Riscv.RiscvLabel(instr.label))

        def visitLoadImm4(self, instr: LoadImm4) -> None:
            self.seq.append(Riscv.LoadImm(instr.dst, instr.value))

        def visitUnary(self, instr: Unary) -> None:
            self.seq.append(Riscv.Unary(instr.op, instr.dst, instr.operand))

        # 这里需要根据不同的指令码添加不同长度的汇编
        def visitBinary(self, instr: Binary) -> None:
            op = instr.op

            if op == BinaryOp.EQU:
                self.seq.append(Riscv.Binary(
                    BinaryOp.SUB, instr.dst, instr.lhs, instr.rhs
                ))
                self.seq.append(Riscv.Unary(
                    UnaryOp.SEQZ, instr.dst, instr.dst
                ))
            elif op == BinaryOp.NEQ:
                self.seq.append(Riscv.Binary(
                    BinaryOp.SUB, instr.dst, instr.lhs, instr.rhs
                ))
                self.seq.append(Riscv.Unary(
                    UnaryOp.SNEZ, instr.dst, instr.dst
                ))
            elif op == BinaryOp.LEQ:
                self.seq.append(Riscv.Binary(
                    BinaryOp.SGT, instr.dst, instr.lhs, instr.rhs
                ))
                self.seq.append(Riscv.Unary(
                    UnaryOp.SEQZ, instr.dst, instr.dst
                ))
            elif op == BinaryOp.GEQ:
                self.seq.append(Riscv.Binary(
                    BinaryOp.SLT, instr.dst, instr.lhs, instr.rhs
                ))
                self.seq.append(Riscv.Unary(
                    UnaryOp.SEQZ, instr.dst, instr.dst
                ))
            elif op == BinaryOp.LOR:
                self.seq.append(Riscv.Binary(
                    BinaryOp.OR, instr.dst, instr.lhs, instr.rhs
                ))
                self.seq.append(Riscv.Unary(
                    UnaryOp.SNEZ, instr.dst, instr.dst
                ))
            elif op == BinaryOp.LAND:
                self.seq.append(Riscv.Unary(
                    UnaryOp.SNEZ, instr.dst, instr.lhs
                ))
                self.seq.append(Riscv.Binary(
                    BinaryOp.SUB, instr.dst, Riscv.ZERO, instr.dst
                ))
                self.seq.append(Riscv.Binary(
                    BinaryOp.AND, instr.dst, instr.dst, instr.rhs
                ))
                self.seq.append(Riscv.Unary(
                    UnaryOp.SNEZ, instr.dst, instr.dst
                ))
            else:
                self.seq.append(Riscv.Binary(
                    instr.op, instr.dst, instr.lhs, instr.rhs))

        def visitCondBranch(self, instr: CondBranch) -> None:
            self.seq.append(Riscv.Branch(instr.cond, instr.label))

        def visitBranch(self, instr: Branch) -> None:
            self.seq.append(Riscv.Jump(instr.target))

        def visitAssign(self, instr: Assign) -> None:
            self.seq.append(Riscv.Move(instr.dst, instr.src))

        # in step9, you need to think about how to pass the parameters and how to store and restore callerSave regs
        # * Step 9
        def visitParam(self, instr: Param) -> None:
            self.seq.append(Riscv.Param(instr.param))

        # * Step 9
        def visitCall(self, instr: Call) -> None:
            self.seq.append(Riscv.Call(instr.dst, instr.func, instr.args))

        # * Step 10
        def visitLoadSymbol(self, instr: LoadSymbol) -> None:
            self.seq.append(Riscv.LoadSymbol(instr.dst, instr.symbol))

        # * Step 10
        def visitLoadW(self, instr: LoadW) -> None:
            self.seq.append(Riscv.LoadW(instr.dst, instr.src, instr.offset))

        # * Step 10
        def visitStoreW(self, instr: StoreW) -> None:
            self.seq.append(Riscv.StoreW(instr.dst, instr.src, instr.offset))

        # in step11, you need to think about how to store the array
        def visitAlloc(self, instr: Alloc) -> None:
            self.seq.append(Riscv.Alloc(instr.dst, instr.size))


"""
RiscvAsmEmitter: an SubroutineEmitter for RiscV
"""


class RiscvSubroutineEmitter(SubroutineEmitter):
    def __init__(self, emitter: RiscvAsmEmitter, info: SubroutineInfo) -> None:
        super().__init__(emitter, info)

        # + 4 is for the RA reg
        # + 4 is for the SP reg
        self.nextLocalOffset = 4 * len(Riscv.CalleeSaved) + 8

        # the buf which stored all the NativeInstrs in this function
        self.buf: list[NativeInstr] = []

        # from temp to int
        # record where a temp is stored in the stack
        self.offsets = {}

        self.printer.printLabel(info.funcLabel)

        # in step9, step11 you can compute the offset of local array and parameters here

    def emitComment(self, comment: str) -> None:
        # you can add some log here to help you debug
        pass

    # store some temp to stack
    # usually happen when reaching the end of a basicblock
    # in step9, you need to think about the fuction parameters here
    def emitStoreToStack(self, src: Reg) -> None:
        if src.temp.index not in self.offsets:
            self.offsets[src.temp.index] = self.nextLocalOffset - 8
            self.nextLocalOffset += 4
        self.buf.append(
            Riscv.NativeStoreWord(src, Riscv.SP, self.offsets[src.temp.index])
        )

    # load some temp from stack
    # usually happen when using a temp which is stored to stack before
    # in step9, you need to think about the fuction parameters here
    def emitLoadFromStack(self, dst: Reg, src: Temp):
        # print(self.offsets)
        # print(src.index)
        if src.index not in self.offsets:
            raise IllegalArgumentException()
        else:
            self.buf.append(
                Riscv.NativeLoadWord(dst, Riscv.SP, self.offsets[src.index])
            )

    # add a NativeInstr to buf
    # when calling the fuction emitEnd, all the instr in buf will be transformed to RiscV code
    def emitNative(self, instr: NativeInstr):
        self.buf.append(instr)

    def emitLabel(self, label: Label):
        self.buf.append(Riscv.RiscvLabel(label).toNative([], []))

    # * Step 11 done
    def emitAllocOnStack(self, dst: Reg, size: int):
        # ? 在栈上为数组分配空间
        self.buf.append(Riscv.CalLocation(
            dst, Riscv.SP, self.nextLocalOffset-8))
        self.nextLocalOffset += size

    # * Step 9 done
    def emitEnd(self):
        self.printer.printComment("start of prologue")
        self.printer.printInstr(Riscv.NativeStoreWord(Riscv.RA, Riscv.SP, -4))
        self.printer.printInstr(Riscv.NativeStoreWord(Riscv.FP, Riscv.SP, -8))
        self.printer.printInstr(Riscv.NativeMoveWord(Riscv.FP, Riscv.SP))
        self.printer.printInstr(Riscv.SPAdd(-self.nextLocalOffset))

        # in step9, you need to think about how to store RA here
        # you can get some ideas from how to save CalleeSaved regs
        for i in range(len(Riscv.CalleeSaved)):
            if Riscv.CalleeSaved[i].isUsed():
                self.printer.printInstr(
                    Riscv.NativeStoreWord(
                        Riscv.CalleeSaved[i], Riscv.SP, 4 * i)
                )

        self.printer.printComment("end of prologue")
        self.printer.println("")

        self.printer.printComment("start of body")

        # in step9, you need to think about how to pass the parameters here
        # you can use the stack or regs

        # using asmcodeprinter to output the RiscV code
        for instr in self.buf:
            self.printer.printInstr(instr)

        self.printer.printComment("end of body")
        self.printer.println("")

        self.printer.printLabel(
            Label(LabelKind.TEMP, self.info.funcLabel.name + Riscv.EPILOGUE_SUFFIX)
        )
        self.printer.printComment("start of epilogue")

        for i in range(len(Riscv.CalleeSaved)):
            if Riscv.CalleeSaved[i].isUsed():
                self.printer.printInstr(
                    Riscv.NativeLoadWord(Riscv.CalleeSaved[i], Riscv.SP, 4 * i)
                )

        self.printer.printInstr(Riscv.SPAdd(self.nextLocalOffset))
        self.printer.printInstr(Riscv.NativeLoadWord(Riscv.RA, Riscv.SP, -4))
        self.printer.printInstr(Riscv.NativeLoadWord(Riscv.FP, Riscv.SP, -8))
        self.printer.printComment("end of epilogue")
        self.printer.println("")

        self.printer.printInstr(Riscv.NativeReturn())
        self.printer.println("")
