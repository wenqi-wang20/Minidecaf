from typing import Protocol, TypeVar, cast

from frontend.ast.node import Node, NullType
from frontend.ast.tree import *
from frontend.ast.visitor import RecursiveVisitor, Visitor
from frontend.scope.globalscope import GlobalScope
from frontend.scope.scope import Scope, ScopeKind
from frontend.scope.scopestack import ScopeStack
from frontend.symbol.funcsymbol import FuncSymbol
from frontend.symbol.symbol import Symbol
from frontend.symbol.varsymbol import VarSymbol
from frontend.type.array import ArrayType
from frontend.type.type import DecafType
from utils.error import *
from utils.riscv import MAX_INT

"""
The namer phase: resolve all symbols defined in the abstract syntax tree and store them in symbol tables (i.e. scopes).
"""


class Namer(Visitor[ScopeStack, None]):
    def __init__(self) -> None:
        pass

    # * Step 7
    # * Entry of this phase
    def transform(self, program: Program) -> Program:
        # Global scope. You don't have to consider it until Step 9.
        program.globalScope = GlobalScope
        ctx = ScopeStack(program.globalScope)

        program.accept(self, ctx)
        return program

    # * Step 9 done
    def visitProgram(self, program: Program, ctx: ScopeStack) -> None:

        # Check if the 'main' function is missing
        if not program.hasMainFunc():
            raise DecafNoMainFuncError

        # * Step 10
        # 遍历所有全局变量，注意这里不能够使用 program.globalvars()，因为这个函数会返回一个 dict，自动去重
        for child in program:
            if isinstance(child, Declaration):
                global_var = child
            else:
                continue
            # ? 重复定义
            if ctx.findConflict(global_var.ident.value) is not None:
                raise DecafGlobalVarDefinedTwiceError(global_var.ident.value)
            var_symbol = VarSymbol(
                global_var.ident.value, global_var.var_t, isGlobal=True)

            if global_var.isArray == True:
                # ? 如果为数组，检查数组大小是否合法
                for dim in global_var.dims:
                    if dim <= 0 or dim > MAX_INT:
                        raise DecafBadArraySizeError()
                var_symbol.setDims(global_var.dims)

                # ? 全局数组初始化
                if global_var.init_expr is NULL:
                    global_var.init_expr = Integer_list()
            else:
                # ? 如果不是数组，有初始化表达式，则设置全局变量的初值
                if global_var.init_expr is not NULL:
                    global_var.init_expr.accept(self, ctx)
                    var_symbol.setInitValue(global_var.init_expr.value)

            ctx.declare(var_symbol)
            global_var.setattr("symbol", var_symbol)

        # program.mainFunc().accept(self, ctx)
        # 遍历 program 中所有的函数
        for child in program:
            if isinstance(child, Function):
                func = child
            else:
                continue
            func.accept(self, ctx)

    # * Step 11 done
    def visitIndexExpression(self, indexExpr: IndexExpression, ctx: ScopeStack) -> None:
        # ? 检查数组是否被定义
        array_symbol: VarSymbol = ctx.lookup(indexExpr.ident.value)
        if array_symbol is None:
            raise DecafUndefinedVarError(indexExpr.ident.value)
        # ? 检查数组是否为数组类型
        if array_symbol.isArray == False:
            raise DecafTypeMismatchError()
        # ? 检查参数维度是否一致
        if len(indexExpr.indexes) != len(array_symbol.dims):
            raise DecafBadArraySizeError()
        for index in indexExpr.indexes:
            index.accept(self, ctx)
        indexExpr.setattr("symbol", array_symbol)
        # print(indexExpr.getattr("symbol"))

    # * Step 9 done
    def visitFunction(self, func: Function, ctx: ScopeStack) -> None:
        # ? 不允许函数定义在局部作用域
        if not ctx.isGlobalScope():
            raise DecafSyntaxError()

        # 声明函数符号
        func_symbol = FuncSymbol(
            func.ident.value, func.ret_t, GlobalScope)

        # 检查函数是否重复定义
        if ctx.findConflict(func_symbol.name) is not None:
            conflict_symbol = ctx.findConflict(func_symbol.name)

            # ? 如果符号被定义为其他类型，则报错
            if not isinstance(conflict_symbol, FuncSymbol):
                raise DecafDeclConflictError(conflict_symbol.name)
            # ? 如果函数被定义过两次，则报错
            if GlobalScope.isDefined(conflict_symbol) and func.body is not None:
                raise DecafDeclConflictError(conflict_symbol.name)
            # ? 参数个数不同，报错
            if conflict_symbol.parameterNum != len(func.params):
                raise DecafDeclConflictError(conflict_symbol.name)
            # ? 依次检查参数类型是否相同
            if func.params is not None:
                for i in range(len(func.params)):
                    if func.params[i].var_t.__str__() != conflict_symbol.getParaType(i).__str__():
                        raise DecafDeclConflictError(conflict_symbol.name)
            # ? 如果函数已经声明过，并且此处有定义，则定义该函数
            if func.body is not None:
                # 新增函数作用域
                func.setattr("symbol", conflict_symbol)
                ctx.open(Scope(ScopeKind.LOCAL))
                func.params.accept(self, ctx)
                # 无需再开启 block 作用域
                for child in func.body:
                    child.accept(self, ctx)
                ctx.close()
                GlobalScope.define(conflict_symbol)
        else:
            # print(f"fisrt declare: {func.ident.value}")
            # 说明没有重复定义
            func.setattr("symbol", func_symbol)
            # 如果函数有参数，则依次加入到函数符号中
            if func.params is not None:
                for param in func.params:
                    # 将参数类型加入到函数符号中
                    func_symbol.addParaType(param.var_t.type)
            GlobalScope.declare(func_symbol)

            # 如果函数体不为空，说明是函数定义
            if func.body is not None:
                # 新增函数作用域
                ctx.open(Scope(ScopeKind.LOCAL))
                func.params.accept(self, ctx)
                # 无需再开启 block 作用域
                for child in func.body:
                    child.accept(self, ctx)
                ctx.close()
                GlobalScope.define(func_symbol)

    # * Step 9 done
    def visitParameterList(self, parameter_list: Parameter_list, ctx: ScopeStack) -> None:
        for param in parameter_list:
            param.accept(self, ctx)

    # * Step 9 done
    def visitParameterItem(self, param: Parameter_item, ctx: ScopeStack) -> Optional[U]:
        # 检查参数的重复定义
        if ctx.findConflict(param.ident.value) is not None:
            raise DecafDeclConflictError(param.ident.value)

        # 为函数定义中的参数创建符号，并且加入到当前作用域中
        var_symbol = VarSymbol(param.ident.value, param.var_t)
        # * Step 12
        # ? 如果是数组类型，需要设置
        if param.isArray:
            var_symbol.setDims(param.dims)
        ctx.declare(var_symbol)
        param.setattr("symbol", var_symbol)

    # * Step 9 done
    def visitCall(self, func_call: Call, ctx: ScopeStack) -> Optional[U]:
        # ? 先检查函数符号是否存在
        if not GlobalScope.containsKey(func_call.ident.value):
            raise DecafUndefinedVarError(func_call.ident.value)
        # ? 检查函数符号是否冲突
        if ctx.findConflict(func_call.ident.value) is not None:
            raise DecafDeclConflictError

        # 根据 lookup 函数的返回值，挨个检查参数类型是否匹配
        # ? 检查参数个数是否匹配
        call_symbol = cast(FuncSymbol, GlobalScope.get(func_call.ident.value))
        if len(func_call.args) != call_symbol.parameterNum:
            raise DecafBadFuncCallError
        for arg in func_call.args:
            arg.accept(self, ctx)
        # ? 检查参数类型是否匹配
        # ? 实际不需要检查，因为都是 INT 类型
        # * Step 12
        # ? 在 step 12 中需要检查，因为加入了数组类型的参数
        for i in range(len(func_call.args)):
            arg = func_call.args[i]
            paramtype = call_symbol.getParaType(i)
            arg_symbol = arg.getattr("symbol")
            if arg_symbol is not None:
                if arg_symbol.type.type != paramtype:
                    raise DecafTypeMismatchError()
            else:
                if isinstance(paramtype, ArrayType):
                    raise DecafTypeMismatchError()

    # * Step 7 done
    # open a new scope for the block before visiting the block
    # and close the scope after visiting the block
    def visitBlock(self, block: Block, ctx: ScopeStack) -> None:
        ctx.open(Scope(ScopeKind.LOCAL))
        for child in block:
            child.accept(self, ctx)
        ctx.close()

    def visitReturn(self, stmt: Return, ctx: ScopeStack) -> None:
        stmt.expr.accept(self, ctx)

        """
        def visitFor(self, stmt: For, ctx: ScopeStack) -> None:

        1. Open a local scope for stmt.init.
        2. Visit stmt.init, stmt.cond, stmt.update.
        3. Open a loop in ctx (for validity checking of break/continue)
        4. Visit body of the loop.
        5. Close the loop and the local scope.
        """

    def visitIf(self, stmt: If, ctx: ScopeStack) -> None:
        stmt.cond.accept(self, ctx)
        stmt.then.accept(self, ctx)

        # * check if the else branch exists
        if not stmt.otherwise is NULL:
            stmt.otherwise.accept(self, ctx)

    def visitWhile(self, stmt: While, ctx: ScopeStack) -> None:
        stmt.cond.accept(self, ctx)
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()

        """
        def visitDoWhile(self, stmt: DoWhile, ctx: ScopeStack) -> None:

        1. Open a loop in ctx (for validity checking of break/continue)
        2. Visit body of the loop.
        3. Close the loop.
        4. Visit the condition of the loop.
        """

    def visitBreak(self, stmt: Break, ctx: ScopeStack) -> None:
        if not ctx.inLoop():
            raise DecafBreakOutsideLoopError()

        # def visitContinue(self, stmt: Continue, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBreak.
        """
        # stmt.accept(self, ctx)

    # * Step 11 done
    def visitDeclaration(self, decl: Declaration, ctx: ScopeStack) -> None:
        """
        1. Use ctx.findConflict to find if a variable with the same name has been declared.
        2. If not, build a new VarSymbol, and put it into the current scope using ctx.declare.
        3. Set the 'symbol' attribute of decl.
        4. If there is an initial value, visit it.
        """
        # * Step 5 done
        # ? 定义冲突
        if ctx.findConflict(decl.ident.value):
            raise DecafDeclConflictError(decl.ident.value)
        symbol = VarSymbol(decl.ident.value, decl.var_t)
        # ? 如果是数组，检查数组下标是否合法
        if decl.isArray == True:
            for dim in decl.dims:
                if dim <= 0 or dim > MAX_INT:
                    raise DecafBadArraySizeError()
            symbol.setDims(decl.dims)

        ctx.declare(symbol)
        # * use the setattr to set the symbol attribute of decl
        decl.setattr("symbol", symbol)

        # ? 检查初值
        if decl.init_expr is not NULL:
            if decl.isArray:
                if len(decl.init_expr.children) > decl.var_t.type.size // 4:
                    raise DecafGlobalVarBadInitValueError(decl.ident.value)
            else:
                # * Step 12
                # ? 检查是否给 int 赋值了数组
                if isinstance(decl.init_expr, Integer_list):
                    raise DecafBadAssignTypeError()
                if isinstance(decl.init_expr, Identifier):
                    init_symbol = ctx.lookup(decl.init_expr.value)
                    if init_symbol.isArray:
                        raise DecafBadAssignTypeError()
                # * in this case,  we use the namer visitor the visit the init expression, like visitBinary, VisitUnary etc.
                decl.init_expr.accept(self, ctx)

    def visitAssignment(self, expr: Assignment, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBinary.
        """
        # * Step 5
        lhs_symbol = ctx.lookup(expr.lhs.value)
        if lhs_symbol is None:
            raise DecafUndefinedVarError(expr.lhs.value)
        else:
            expr.lhs.accept(self, ctx)
            expr.rhs.accept(self, ctx)

            # * Step 12
            # ? 对非法的赋值进行检查
            if isinstance(expr.rhs, Identifier):
                rhs_symbol = ctx.lookup(expr.rhs.value)
                if rhs_symbol.isArray:
                    raise DecafBadAssignTypeError()
            expr.lhs.setattr("symbol", ctx.lookup(expr.lhs.value))
            expr.setattr("symbol", ctx.lookup(expr.lhs.value))

    # * Step 11 done
    def visitUnary(self, expr: Unary, ctx: ScopeStack) -> None:
        # ? 需要排除对数组进行四则运算等操作
        if isinstance(expr.operand, Identifier) and ctx.lookup(expr.operand.value).isArray == True:
            raise DecafTypeMismatchError()
        expr.operand.accept(self, ctx)

    # * Step 11 done
    def visitBinary(self, expr: Binary, ctx: ScopeStack) -> None:
        # ? 需要排除对数组进行四则运算等操作
        if (isinstance(expr.lhs, Identifier) and ctx.lookup(expr.lhs.value).isArray == True) or \
                (isinstance(expr.rhs, Identifier) and ctx.lookup(expr.rhs.value).isArray == True):
            raise DecafTypeMismatchError()
        expr.lhs.accept(self, ctx)
        expr.rhs.accept(self, ctx)

    def visitCondExpr(self, expr: ConditionExpression, ctx: ScopeStack) -> None:
        """
        1. Refer to the implementation of visitBinary.
        """
        # * Step 6
        expr.cond.accept(self, ctx)
        expr.then.accept(self, ctx)
        expr.otherwise.accept(self, ctx)

    def visitIdentifier(self, ident: Identifier, ctx: ScopeStack) -> None:
        """
        1. Use ctx.lookup to find the symbol corresponding to ident.
        2. If it has not been declared, raise a DecafUndefinedVarError.
        3. Set the 'symbol' attribute of ident.
        """
        # * Step 5
        if ctx.lookup(ident.value) is None:
            raise DecafUndefinedVarError(ident.value)
        else:
            ident.setattr("symbol", ctx.lookup(ident.value))

    def visitIntLiteral(self, expr: IntLiteral, ctx: ScopeStack) -> None:
        value = expr.value
        if value > MAX_INT:
            raise DecafBadIntValueError(value)

    # * Step 8 done
    def visitFor(self, stmt: For, ctx: ScopeStack) -> None:
        # for 语句内部的变量声明，需要在 for 语句的作用域内
        ctx.open(Scope(ScopeKind.LOCAL))
        stmt.init.accept(self, ctx)
        stmt.cond.accept(self, ctx)
        stmt.step.accept(self, ctx)

        # for 语句的循环体也会有新的作用域
        ctx.open(Scope(ScopeKind.LOCAL))
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()
        ctx.close()
        ctx.close()

    def visitDoWhile(self, stmt: DoWhile, ctx: ScopeStack) -> None:
        ctx.open(Scope(ScopeKind.LOCAL))
        ctx.openLoop()
        stmt.body.accept(self, ctx)
        ctx.closeLoop()
        ctx.close()
        stmt.cond.accept(self, ctx)

    def visitContinue(self, stmt: Continue, ctx: ScopeStack) -> None:
        if not ctx.inLoop():
            raise DecafContinueOutsideLoopError()
        # stmt.accept(self, ctx)
