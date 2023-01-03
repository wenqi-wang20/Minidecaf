from typing import Any, Optional, Union

from .tacfunc import TACFunc
from frontend.symbol.varsymbol import VarSymbol


# A TAC program consists of several TAC functions.
class TACProg:
    def __init__(self, funcs: list[TACFunc], global_vars: list[VarSymbol]) -> None:
        self.funcs = funcs
        self.global_vars = global_vars

    def printTo(self) -> None:
        for func in self.funcs:
            func.printTo()
