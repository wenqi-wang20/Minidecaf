import random

from backend.dataflow.basicblock import BasicBlock, BlockKind
from backend.dataflow.cfg import CFG
from backend.dataflow.loc import Loc
from backend.reg.regalloc import RegAlloc
from backend.riscv.riscvasmemitter import RiscvAsmEmitter
from backend.subroutineemitter import SubroutineEmitter
from backend.subroutineinfo import SubroutineInfo
from utils.riscv import Riscv
from utils.tac.holeinstr import HoleInstr
from utils.tac.reg import Reg
from utils.tac.temp import Temp

"""
BruteRegAlloc: one kind of RegAlloc

bindings: map from temp.index to Reg

we don't need to take care of GlobalTemp here
because we can remove all the GlobalTemp in selectInstr process

1. accept：根据每个函数的 CFG 进行寄存器分配，寄存器分配结束后生成相应汇编代码
2. bind：将一个 Temp 与寄存器绑定
3. unbind：将一个 Temp 与相应寄存器解绑定
4. localAlloc：根据数据流对一个 BasicBlock 内的指令进行寄存器分配
5. allocForLoc：每一条指令进行寄存器分配
6. allocRegFor：根据数据流决定为当前 Temp 分配哪一个寄存器
"""


class BruteRegAlloc(RegAlloc):
    def __init__(self, emitter: RiscvAsmEmitter) -> None:
        super().__init__(emitter)
        self.bindings = {}
        for reg in emitter.allocatableRegs:
            reg.used = False

    def accept(self, graph: CFG, info: SubroutineInfo) -> None:
        subEmitter = self.emitter.emitSubroutine(info)
        id = 0
        for bb in graph.iterator():
            # you need to think more here
            # maybe we don't need to alloc regs for all the basic blocks
            if bb.label is not None:
                subEmitter.emitLabel(bb.label)
            if graph.unreachable(id) == False:
                self.localAlloc(bb, subEmitter)
            id += 1
        subEmitter.emitEnd()

    def bind(self, temp: Temp, reg: Reg):
        reg.used = True
        self.bindings[temp.index] = reg
        reg.occupied = True
        reg.temp = temp

    def unbind(self, temp: Temp):
        if temp.index in self.bindings:
            self.bindings[temp.index].occupied = False
            self.bindings.pop(temp.index)

    def localAlloc(self, bb: BasicBlock, subEmitter: SubroutineEmitter):
        self.bindings.clear()
        for reg in self.emitter.allocatableRegs:
            reg.occupied = False

        # * Step 9
        # in step9, you may need to think about how to store callersave regs here
        args_stack = []
        for loc in bb.allSeq():

            # 如果是分配函数参数的指令；
            if isinstance(loc.instr, Riscv.Param):
                # ? 遇到 param 指令不做处理，直接把参数压栈
                # ? 等到 call 指令时，再分配寄存器
                args_stack.append(loc.instr.srcs[0])
            # 如果是函数调用的指令
            elif isinstance(loc.instr, Riscv.Call):
                saved_args = []
                for caller_save_reg in Riscv.CallerSaved:
                    # 将 caller_save_reg 存到栈中
                    if caller_save_reg.occupied and caller_save_reg.temp.index in loc.liveIn:
                        subEmitter.emitStoreToStack(caller_save_reg)
                        saved_args.append(
                            (caller_save_reg, caller_save_reg.temp))
                        # 解开变量和寄存器的绑定
                        self.unbind(caller_save_reg.temp)

                # ? 将参数依次存入 A0-A7
                argnum = len(loc.instr.arguments_list)
                func_args_stack = args_stack[-argnum:]
                for i in range(argnum):
                    arg = func_args_stack[i]
                    if i < 8:
                        arg_tmp_reg = self.allocRegFor(
                            arg, True, loc.liveIn, subEmitter)
                        subEmitter.emitNative(Riscv.NativeMoveWord(
                            Riscv.ArgRegs[i], arg_tmp_reg))
                        self.unbind(arg)
                        self.bind(arg, Riscv.ArgRegs[i])
                    else:
                        subEmitter.emitNative(Riscv.NativeStoreWord(
                            self.allocRegFor(arg, True, loc.liveIn, subEmitter), Riscv.SP, 4 * (i - len(func_args_stack))))

                # ? sub sp
                if argnum >= 8:
                    subEmitter.emitNative(Riscv.SPAdd(
                        - 4 * (argnum - 8)))
                # ? call func
                subEmitter.emitNative(loc.instr.toNative([], []))
                self.bind(loc.instr.ret_val, Riscv.A0)

                # ? add sp
                if argnum >= 8:
                    subEmitter.emitNative(Riscv.SPAdd(
                        4 * (argnum - 8)))
                # ? pop func args
                args_stack = args_stack[:-argnum]
                # ? restore caller_save_reg
                for reg, temp in saved_args:
                    if reg.occupied:
                        subEmitter.emitStoreToStack(reg)
                        self.unbind(reg.temp)
                    subEmitter.emitLoadFromStack(reg, temp)
                    self.bind(temp, reg)
            elif isinstance(loc.instr, Riscv.Alloc):
                base_reg = self.allocRegFor(
                    loc.instr.dsts[0], False, loc.liveIn, subEmitter)
                subEmitter.emitAllocOnStack(base_reg, loc.instr.size)
            else:
                self.allocForLoc(loc, subEmitter)

        for tempindex in bb.liveOut:
            if tempindex in self.bindings:
                subEmitter.emitStoreToStack(self.bindings.get(tempindex))

        if (not bb.isEmpty()) and (bb.kind is not BlockKind.CONTINUOUS):
            self.allocForLoc(bb.locs[len(bb.locs) - 1], subEmitter)

    def allocForLoc(self, loc: Loc, subEmitter: SubroutineEmitter):
        instr = loc.instr
        srcRegs: list[Reg] = []
        dstRegs: list[Reg] = []

        for i in range(len(instr.srcs)):
            temp = instr.srcs[i]
            if isinstance(temp, Reg):
                srcRegs.append(temp)
            else:
                srcRegs.append(self.allocRegFor(
                    temp, True, loc.liveIn, subEmitter))

        for i in range(len(instr.dsts)):
            temp = instr.dsts[i]
            if isinstance(temp, Reg):
                dstRegs.append(temp)
            else:
                dstRegs.append(self.allocRegFor(
                    temp, False, loc.liveIn, subEmitter))

        subEmitter.emitNative(instr.toNative(dstRegs, srcRegs))

    def allocRegFor(
        self, temp: Temp, isRead: bool, live: set[int], subEmitter: SubroutineEmitter
    ):
        if temp.index in self.bindings:
            return self.bindings[temp.index]

        for reg in self.emitter.allocatableRegs:
            if (not reg.occupied) or (not reg.temp.index in live):
                subEmitter.emitComment(
                    "  allocate {} to {}  (read: {}):".format(
                        str(temp), str(reg), str(isRead)
                    )
                )
                if isRead:
                    subEmitter.emitLoadFromStack(reg, temp)
                if reg.occupied:
                    self.unbind(reg.temp)
                self.bind(temp, reg)
                return reg

        reg = self.emitter.allocatableRegs[
            random.randint(0, len(self.emitter.allocatableRegs))
        ]
        subEmitter.emitStoreToStack(reg)
        subEmitter.emitComment(
            "  spill {} ({})".format(str(reg), str(reg.temp)))
        self.unbind(reg.temp)
        self.bind(temp, reg)
        subEmitter.emitComment(
            "  allocate {} to {} (read: {})".format(
                str(temp), str(reg), str(isRead))
        )
        if isRead:
            subEmitter.emitLoadFromStack(reg, temp)
        return reg
