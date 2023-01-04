from __future__ import annotations

from typing import Any, Optional, Union
from frontend.ast.tree import Declaration
from frontend.symbol.varsymbol import VarSymbol

from utils.label.funclabel import *
from utils.label.label import Label, LabelKind

from .context import Context
from .funcvisitor import FuncVisitor
from .tacprog import TACProg


# * Step 10
# ? 添加全局变量并且传递给 TACProg
class ProgramWriter:
    def __init__(self, funcs: list[str], global_vars: list[VarSymbol]) -> None:
        self.funcs = []
        self.global_vars = global_vars
        self.global_init = []
        self.ctx = Context()
        for func in funcs:
            # 已经将所有函数的入口标签加入到上下文中
            self.funcs.append(func)
            self.ctx.putFuncLabel(func)

    # * Step 12
    def visitMainFunc(self) -> FuncVisitor:
        entry = MAIN_LABEL
        mv = FuncVisitor(entry, 0, self.ctx)
        mv.initglobal_vars(self.global_init)
        return mv

    def visitFunc(self, name: str, numArgs: int) -> FuncVisitor:
        entry = self.ctx.getFuncLabel(name)
        return FuncVisitor(entry, numArgs, self.ctx)

    def visitEnd(self) -> TACProg:
        return TACProg(self.ctx.funcs, self.global_vars)
