from utils.tac.temp import Temp

from .symbol import *

"""
Variable symbol, representing a variable definition.
"""


class VarSymbol(Symbol):
    def __init__(self, name: str, type: DecafType, isGlobal: bool = False) -> None:
        super().__init__(name, type)
        self.temp: Temp
        self.isGlobal = isGlobal
        self.initValue = 0
        self.isArray = False
        self.dims = []

    def __str__(self) -> str:
        return "variable %s : %s" % (self.name, str(self.type))

    # @property
    # self.isArray(self) -> bool:

    # * To set the initial value of a variable symbol (used for global variable).

    def setInitValue(self, value: int) -> None:
        self.initValue = value

    # * To set the dimensions of an array variable symbol (used for global variable).
    def setDims(self, dims: list[int]) -> None:
        self.dims = dims
        self.isArray = True
