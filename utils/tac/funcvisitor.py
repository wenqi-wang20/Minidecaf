from __future__ import annotations

from typing import Any, Optional, Union

from utils.label.funclabel import FuncLabel
from utils.label.label import Label
from frontend.symbol.varsymbol import VarSymbol
from frontend.ast.node import NULL
from frontend.ast.tree import Declaration

from .context import Context
from .tacfunc import TACFunc
from .tacinstr import *
from .tacop import *
from .temp import Temp


class FuncVisitor:
    def __init__(self, entry: FuncLabel, numArgs: int, ctx: Context) -> None:
        self.ctx = ctx
        self.func = TACFunc(entry, numArgs)
        self.visitLabel(entry)
        self.nextTempId = 0
        self.global_init = None

        self.continueLabelStack = []
        self.breakLabelStack = []

    # * Step 12
    def initglobal_vars(self, global_init: list[Declaration]) -> None:
        self.global_init = global_init
        # * Step 12
        # ? 在这里需要初始化全局数组变量
        if self.global_init is not None:
            for arr_init in self.global_init:
                if arr_init.isArray:
                    # ? 加载 fill_n 指令的参数
                    addr_tmp = self.freshTemp()
                    self.visitLoadSymbol(addr_tmp, arr_init.ident.value)
                    self.visitParam(addr_tmp)
                    num_tmp = self.visitLoad(0)
                    self.visitParam(num_tmp)
                    len_tmp = self.visitLoad(arr_init.var_t.type.size)
                    self.visitParam(len_tmp)

                    # ? 加载 fill_n 指令
                    val_tmp = self.freshTemp()
                    self.visitCall(val_tmp, FuncLabel('fill_n'),
                                   [addr_tmp, num_tmp, len_tmp])

                    if arr_init.init_expr is not NULL:
                        # ? 逐个赋值
                        init_vars = arr_init.init_expr.children
                        for i in range(len(init_vars)):
                            var_tmp = self.visitLoad(init_vars[i])
                            self.visitStoreW(var_tmp, addr_tmp, i * 4)

    # To get a fresh new temporary variable.
    def freshTemp(self) -> Temp:
        temp = Temp(self.nextTempId)
        self.nextTempId += 1
        return temp

    # To get a fresh new label (for jumping and branching, etc).
    def freshLabel(self) -> Label:
        return self.ctx.freshLabel()

    # To count how many temporary variables have been used.
    def getUsedTemp(self) -> int:
        return self.nextTempId

    # In fact, the following methods can be named 'appendXXX' rather than 'visitXXX'. E.g., by calling 'visitAssignment', you add an assignment instruction at the end of current function.
    def visitAssignment(self, dst: Temp, src: Temp) -> Temp:
        self.func.add(Assign(dst, src))
        return src

    def visitLoad(self, value: Union[int, str]) -> Temp:
        temp = self.freshTemp()
        if isinstance(value, int):
            self.func.add(LoadImm4(temp, value))
        else:
            self.func.add(LoadStrConst(temp, value))
        return temp

    def visitUnary(self, op: UnaryOp, operand: Temp) -> Temp:
        temp = self.freshTemp()
        self.func.add(Unary(op, temp, operand))
        return temp

    def visitUnarySelf(self, op: UnaryOp, operand: Temp) -> None:
        self.func.add(Unary(op, operand, operand))

    def visitBinary(self, op: BinaryOp, lhs: Temp, rhs: Temp) -> Temp:
        temp = self.freshTemp()
        self.func.add(Binary(op, temp, lhs, rhs))
        return temp

    def visitBinarySelf(self, op: BinaryOp, lhs: Temp, rhs: Temp) -> None:
        self.func.add(Binary(op, lhs, lhs, rhs))

    def visitBranch(self, target: Label) -> None:
        self.func.add(Branch(target))

    def visitCondBranch(self, op: CondBranchOp, cond: Temp, target: Label) -> None:
        self.func.add(CondBranch(op, cond, target))

    def visitReturn(self, value: Optional[Temp]) -> None:
        self.func.add(Return(value))

    def visitLabel(self, label: Label) -> None:
        self.func.add(Mark(label))

    def visitMemo(self, content: str) -> None:
        self.func.add(Memo(content))

    def visitRaw(self, instr: TACInstr) -> None:
        self.func.add(instr)

    def visitEnd(self, paras_tmp_list: list[Temp]) -> None:
        if (len(self.func.instrSeq) == 0) or (not self.func.instrSeq[-1].isReturn()):
            self.func.add(Return(None))
        self.func.params = paras_tmp_list
        self.func.tempUsed = self.getUsedTemp()
        self.ctx.funcs.append(self.func)

    # * Step 9 done
    def visitParam(self, arg: Temp) -> None:
        self.func.add(Param(arg))

    # * Step 9 done
    def visitCall(self, ret_val: Temp, func: FuncLabel, argument_list: list[Temp]) -> None:
        self.func.add(Call(ret_val, func, argument_list))

    # * Step 10 done
    def visitLoadSymbol(self, dst: Temp, symbol: str) -> None:
        self.func.add(LoadSymbol(dst, symbol))

    # * Step 10 done
    def visitLoadW(self, dst: Temp, src: Temp, offset: int) -> None:
        self.func.add(LoadW(dst, src, offset))

    # * Step 10 done
    def visitStoreW(self, dst: Temp, src: Temp, offset: int) -> None:
        self.func.add(StoreW(dst, src, offset))

    # * Step 11 done
    def visitAlloc(self, dst: Temp, size: int) -> None:
        self.func.add(Alloc(dst, size))

    # * Step 11 done
    def visitArrayLoc(self, addr: Temp, index: Temp, size: int) -> None:
        # ? 记住这里不能使用 index 作为中间传递值，这样可能会改变 Index 的值，导致外部的值也被改变
        size_temp = self.visitLoad(size)
        self.visitBinarySelf(BinaryOp.MUL, size_temp, index)
        self.visitBinarySelf(BinaryOp.ADD, addr, size_temp)

    # To open a new loop (for break/continue statements)
    def openLoop(self, breakLabel: Label, continueLabel: Label) -> None:
        self.breakLabelStack.append(breakLabel)
        self.continueLabelStack.append(continueLabel)

    # To close the current loop.
    def closeLoop(self) -> None:
        self.breakLabelStack.pop()
        self.continueLabelStack.pop()

    # To get the label for 'break' in the current loop.
    def getBreakLabel(self) -> Label:
        return self.breakLabelStack[-1]

    # To get the label for 'continue' in the current loop.
    def getContinueLabel(self) -> Label:
        return self.continueLabelStack[-1]
