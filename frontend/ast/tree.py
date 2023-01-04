"""
Module that defines all AST nodes.
Reading this file to grasp the basic method of defining a new AST node is recommended.
Modify this file if you want to add a new AST node.
"""

from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar, Union

from frontend.type import INT, DecafType, ArrayType
from utils import T, U

from .node import NULL, BinaryOp, Node, UnaryOp
from .visitor import Visitor, accept

_T = TypeVar("_T", bound=Node)
U = TypeVar("U", covariant=True)


def _index_len_err(i: int, node: Node):
    return IndexError(
        f"you are trying to index the #{i} child of node {node.name}, which has only {len(node)} children"
    )


class ListNode(Node, Generic[_T]):
    """
    Abstract node type that represents a node sequence.
    E.g. `Block` (sequence of statements).
    """

    def __init__(self, name: str, children: list[_T]) -> None:
        super().__init__(name)
        self.children = children

    def __getitem__(self, key: int) -> Node:
        return self.children.__getitem__(key)

    def __len__(self) -> int:
        return len(self.children)

    def accept(self, v: Visitor[T, U], ctx: T):
        ret = tuple(map(accept(v, ctx), self))
        return None if ret.count(None) == len(ret) else ret


class Program(ListNode[Union["Function", "Declaration"]]):
    """
    AST root. It should have only one children before step9.
    """

    def __init__(self, *children: Union[Function, Declaration]) -> None:
        super().__init__("program", list(children))

    def functions(self) -> dict[str, Function]:
        return {func.ident.value: func for func in self if isinstance(func, Function)}

    def globalvars(self) -> dict[str, Declaration]:
        return {var.ident.value: var for var in self if isinstance(var, Declaration)}

    def hasMainFunc(self) -> bool:
        return "main" in self.functions()

    def mainFunc(self) -> Function:
        return self.functions()["main"]

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitProgram(self, ctx)


# * Step 9
# ? body = NULL
class Function(Node):
    """
    AST node that represents a function.
    """

    def __init__(
        self,
        ret_t: TypeLiteral,
        ident: Identifier,
        params: Parameter_list,
        body: Block,
    ) -> None:
        super().__init__("function")
        self.ret_t = ret_t
        self.ident = ident
        self.params = params
        self.body = body

    def __getitem__(self, key: int) -> Node:
        return (
            self.ret_t,
            self.ident,
            self.params,
            self.body,
        )[key]

    def __len__(self) -> int:
        return 4

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitFunction(self, ctx)


class Statement(Node):
    """
    Abstract type that represents a statement.
    """

    def is_block(self) -> bool:
        """
        Determine if this type of statement is `Block`.
        """
        return False


class Return(Statement):
    """
    AST node of return statement.
    """

    def __init__(self, expr: Expression) -> None:
        super().__init__("return")
        self.expr = expr

    def __getitem__(self, key: Union[int, str]) -> Node:
        if isinstance(key, int):
            return (self.expr,)[key]
        return self.__dict__[key]

    def __len__(self) -> int:
        return 1

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitReturn(self, ctx)


class If(Statement):
    """
    AST node of if statement.
    """

    def __init__(
        self, cond: Expression, then: Statement, otherwise: Optional[Statement] = None
    ) -> None:
        super().__init__("if")
        self.cond = cond
        self.then = then
        self.otherwise = otherwise or NULL

    def __getitem__(self, key: int) -> Node:
        return (self.cond, self.then, self.otherwise)[key]

    def __len__(self) -> int:
        return 3

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIf(self, ctx)


class While(Statement):
    """
    AST node of while statement.
    """

    def __init__(self, cond: Expression, body: Statement) -> None:
        super().__init__("while")
        self.cond = cond
        self.body = body

    def __getitem__(self, key: int) -> Node:
        return (self.cond, self.body)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitWhile(self, ctx)


class Break(Statement):
    """
    AST node of break statement.
    """

    def __init__(self) -> None:
        super().__init__("break")

    def __getitem__(self, key: int) -> Node:
        raise _index_len_err(key, self)

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitBreak(self, ctx)

    def is_leaf(self):
        return True


# * Step 8
class For(Statement):
    """
    AST node of for statement.
    """

    def __init__(
        self,
        body: Statement,
        init: Optional[Union[Expression, Declaration]] = None,
        cond: Optional[Expression] = None,
        step: Optional[Expression] = None
    ) -> None:
        super().__init__("for")
        self.init = init or NULL
        self.cond = cond or NULL
        self.step = step or NULL
        self.body = body

    def __getitem__(self, key: int) -> Node:
        return (self.init, self.cond, self.step, self.body)[key]

    def __len__(self) -> int:
        return 4

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitFor(self, ctx)


class DoWhile(Statement):
    """
    AST node of do-while statement.
    """

    def __init__(self, cond: Expression, body: Statement) -> None:
        super().__init__("do-while")
        self.cond = cond
        self.body = body

    def __getitem__(self, key: int) -> Node:
        return (self.cond, self.body)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitDoWhile(self, ctx)


class Continue(Statement):
    """
    AST node of continue statement.
    """

    def __init__(self) -> None:
        super().__init__("continue")

    def __getitem__(self, key: int) -> Node:
        raise _index_len_err(key, self)

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitContinue(self, ctx)

    def is_leaf(self):
        return True


# * Step 7
# block is actually block item list with statement or declaration
class Block(Statement, ListNode[Union["Statement", "Declaration"]]):
    """
    AST node of block "statement".
    """

    def __init__(self, *children: Union[Statement, Declaration]) -> None:
        super().__init__("block", list(children))

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitBlock(self, ctx)

    def is_block(self) -> bool:
        return True


class Declaration(Node):
    """
    AST node of declaration.
    """

    def __init__(
        self,
        var_t: TypeLiteral,
        ident: Identifier,
        init_expr: Optional[Expression] = None,
    ) -> None:
        super().__init__("declaration")
        self.var_t = var_t
        self.ident = ident
        self.isArray = False
        self.dims = []
        self.init_expr = init_expr or NULL

    def __getitem__(self, key: int) -> Node:
        return (self.var_t, self.ident, self.init_expr)[key]

    def __len__(self) -> int:
        return 3

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitDeclaration(self, ctx)


class Expression(Node):
    """
    Abstract type that represents an evaluable expression.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.type: Optional[DecafType] = None


class Unary(Expression):
    """
    AST node of unary expression.
    Note that the operation type (like negative) is not among its children.
    """

    def __init__(self, op: UnaryOp, operand: Expression) -> None:
        super().__init__(f"unary({op.value})")

        self.op = op
        self.operand = operand

    def __getitem__(self, key: int) -> Node:
        return (self.operand,)[key]

    def __len__(self) -> int:
        return 1

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitUnary(self, ctx)

    def __str__(self) -> str:
        return "{}({})".format(
            self.op.value,
            self.operand,
        )


class Binary(Expression):
    """
    AST node of binary expression.
    Note that the operation type (like plus or subtract) is not among its children.
    """

    def __init__(self, op: BinaryOp, lhs: Expression, rhs: Expression) -> None:
        super().__init__(f"binary({op.value})")
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __getitem__(self, key: int) -> Node:
        return (self.lhs, self.rhs)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitBinary(self, ctx)

    def __str__(self) -> str:
        return "({}){}({})".format(
            self.lhs,
            self.op.value,
            self.rhs,
        )


class Assignment(Binary):
    """
    AST node of assignment expression.
    It's actually a kind of binary expression, but it'll make things easier if we use another accept method to handle it.
    """

    def __init__(self, lhs: Identifier, rhs: Expression) -> None:
        super().__init__(BinaryOp.Assign, lhs, rhs)

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitAssignment(self, ctx)


class ConditionExpression(Expression):
    """
    AST node of condition expression (`?:`).
    """

    def __init__(
        self, cond: Expression, then: Expression, otherwise: Expression
    ) -> None:
        super().__init__("cond_expr")
        self.cond = cond
        self.then = then
        self.otherwise = otherwise

    def __getitem__(self, key: Union[int, str]) -> Node:
        if isinstance(key, int):
            return (self.cond, self.then, self.otherwise)[key]
        return self.__dict__[key]

    def __len__(self) -> int:
        return 3

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitCondExpr(self, ctx)

    def __str__(self) -> str:
        return "({})?({}):({})".format(
            self.cond,
            self.then,
            self.otherwise,
        )


class Identifier(Expression):
    """
    AST node of identifier "expression".
    """

    def __init__(self, value: str) -> None:
        super().__init__("identifier")
        self.value = value

    def __getitem__(self, key: int) -> Node:
        raise _index_len_err(key, self)

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIdentifier(self, ctx)

    def __str__(self) -> str:
        return f"identifier({self.value})"

    def is_leaf(self):
        return True


class IntLiteral(Expression):
    """
    AST node of int literal like `0`.
    """

    def __init__(self, value: Union[int, str]) -> None:
        super().__init__("int_literal")
        self.value = int(value)

    def __getitem__(self, key: int) -> Node:
        raise _index_len_err(key, self)

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIntLiteral(self, ctx)

    def __str__(self) -> str:
        return f"int({self.value})"

    def is_leaf(self):
        return True


class TypeLiteral(Node):
    """
    Abstract node type that represents a type literal like `int`.
    """

    def __init__(self, name: str, _type: DecafType) -> None:
        super().__init__(name)
        self.type = _type

    def __str__(self) -> str:
        return f"type({self.type})"

    def is_leaf(self):
        return True


class TInt(TypeLiteral):
    "AST node of type `int`."

    def __init__(self) -> None:
        super().__init__("type_int", INT)

    def __getitem__(self, key: int) -> Node:
        raise _index_len_err(key, self)

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitTInt(self, ctx)


# * Step 11 done
class TArray(TypeLiteral):
    "AST node of type `int[]`."

    def __init__(self, type: DecafType, dims: list[int]) -> None:
        super().__init__("type_array", ArrayType.multidim(type, dims))

    def __getitem__(self, key: int) -> Node:
        raise _index_len_err(key, self)

    def __len__(self) -> int:
        return 0

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitTArray(self, ctx)


# * Step 9 done
class Parameter_item(Node):
    """
    AST node of parameter.
    """

    def __init__(self, var_type: TypeLiteral, ident: Identifier) -> None:
        super().__init__("parameter")
        self.var_t = var_type
        self.ident = ident
        self.dims = []

    @property
    def isArray(self) -> bool:
        return len(self.dims) != 0

    def __getitem__(self, key: int) -> Node:
        return (self.var_type, self.name, self.dims)[key]

    def __len__(self) -> int:
        return 3

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitParameterItem(self, ctx)


# * Step 9 done
class Parameter_list(ListNode["Parameter_item"]):
    """
    AST node of parameter.
    """

    def __init__(self, *children: Parameter_item) -> None:
        super().__init__("parameter_list", list(children))

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitParameterList(self, ctx)


# * Step 9 done
class Expression_list(ListNode["Expression"]):
    """
    AST node of parameter.
    """

    def __init__(self, *children: Expression) -> None:
        super().__init__("expression_list", list(children))

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitExpressionList(self, ctx)


# * Step 9 done
class Call(Node):
    """
    AST node of function call.
    """

    def __init__(self, ident: Identifier, argument_list: Expression_list) -> None:
        super().__init__("call")
        self.ident = ident
        self.args = argument_list

    def __getitem__(self, key: int) -> Node:
        return (self.ident, self.args)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitCall(self, ctx)


# * Step 11 done
class IndexExpression(Expression):
    """
    AST node of index expression.
    """

    def __init__(self, ident: Identifier, *indexes: Expression) -> None:
        super().__init__("index_expr")
        self.ident = ident
        self.indexes = list(indexes)
        self.value = ident.value

    def __getitem__(self, key: int) -> Node:
        return (self.ident, self.indexes)[key]

    def __len__(self) -> int:
        return 2

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIndexExpression(self, ctx)

    def __str__(self) -> str:
        return str(self.ident) + ''.join(f"[{i}]" for i in self.indexes)


# * Step 12
class Integer_list(Expression):
    """
    AST node of integer list.
    """

    def __init__(self) -> None:
        super().__init__("integer_list")
        self.children = []

    def __getitem__(self, key: int) -> Node:
        return self.children[key]

    def __len__(self) -> int:
        return len(self.children)

    def accept(self, v: Visitor[T, U], ctx: T):
        return v.visitIntegerList(self, ctx)