import utils.riscv as riscv
from frontend.ast import node
from frontend.ast.tree import *
from frontend.ast.visitor import Visitor
from frontend.symbol.varsymbol import VarSymbol
from frontend.type.array import ArrayType
from utils.tac import tacop
from utils.tac.funcvisitor import FuncVisitor
from utils.tac.programwriter import ProgramWriter
from utils.tac.tacprog import TACProg
from utils.tac.temp import Temp

"""
The TAC generation phase: translate the abstract syntax tree into three-address code.
"""


class TACGen(Visitor[FuncVisitor, None]):
    def __init__(self) -> None:
        pass

    # * Step 9 done
    # Entry of this phase
    def transform(self, program: Program) -> TACProg:
        func_names = [func_name for func_name in program.functions()]
        var_symbols = [program.globalvars()[var_name].getattr("symbol")
                       for var_name in program.globalvars()]

        # * Step 10
        pw = ProgramWriter(func_names, var_symbols)

        for func_name in program.functions():
            if func_name == "main":
                mainFunc = program.mainFunc()
                # The function visitor of 'main' is special.
                mv = pw.visitMainFunc()
                mainFunc.body.accept(self, mv)
                mv.visitEnd([])
            else:
                func = program.functions()[func_name]
                # ? 只当函数定义后再生成 TAC 码
                if func.body is not None:
                    numArgs = len(func.params.children)
                    mv = pw.visitFunc(func_name, numArgs)
                    # 为参数分配临时变量
                    params_tmp = []
                    for param in func.params:
                        param_symbol = param.getattr("symbol")
                        param_symbol.temp = mv.freshTemp()
                        params_tmp.append(param_symbol.temp)
                    # func.params.accept(self, mv)
                    func.body.accept(self, mv)
                    # Remember to call mv.visitEnd after the translation a function.
                    mv.visitEnd(params_tmp)
        # Remember to call pw.visitEnd before finishing the translation phase.
        return pw.visitEnd()

    # * Step 9 done
    # 在某个函数体中使用函数调用
    def visitCall(self, func_call: Call, mv: FuncVisitor) -> None:
        args_tmp = []
        # ? 先设置函数调用所需要的全部参数
        for param in func_call.args:
            param.accept(self, mv)
            temp = param.getattr("val")
            mv.visitParam(temp)
            args_tmp.append(temp)

        # ? 这里需要访问 CALL 指令，并且新建临时变量为函数设置返回值
        ret_val = mv.freshTemp()
        mv.visitCall(ret_val, mv.ctx.getFuncLabel(
            func_call.ident.value), args_tmp)
        func_call.setattr("val", ret_val)

    def visitBlock(self, block: Block, mv: FuncVisitor) -> None:
        for child in block:
            child.accept(self, mv)

    def visitReturn(self, stmt: Return, mv: FuncVisitor) -> None:
        stmt.expr.accept(self, mv)
        mv.visitReturn(stmt.expr.getattr("val"))

    def visitBreak(self, stmt: Break, mv: FuncVisitor) -> None:
        mv.visitBranch(mv.getBreakLabel())

    def visitIdentifier(self, ident: Identifier, mv: FuncVisitor) -> None:
        """
        1. Set the 'val' attribute of ident as the temp variable of the 'symbol' attribute of ident.
        """
        # * Step 10
        var_symbol: VarSymbol = ident.getattr("symbol")
        if var_symbol.isGlobal:
            # ? 全局变量的访问
            addr_tmp = mv.freshTemp()
            mv.visitLoadSymbol(addr_tmp, var_symbol.name)
            dst_tmp = mv.freshTemp()
            mv.visitLoadW(dst_tmp, addr_tmp, 0)
            ident.setattr("val", dst_tmp)
        else:
            # ? 局部变量的访问
            ident.setattr("val", var_symbol.temp)

    def visitDeclaration(self, decl: Declaration, mv: FuncVisitor) -> None:
        """
        1. Get the 'symbol' attribute of decl.
        2. Use mv.freshTemp to get a new temp variable for this symbol.
        3. If the declaration has an initial value, use mv.visitAssignment to set it.
        """
        # * Step 5
        symbol = decl.getattr("symbol")
        temp = mv.freshTemp()
        symbol.temp = temp
        if decl.init_expr is not NULL:
            decl.init_expr.accept(self, mv)
            mv.visitAssignment(temp, decl.init_expr.getattr("val"))

    def visitAssignment(self, expr: Assignment, mv: FuncVisitor) -> None:
        """
        1. Visit the right hand side of expr, and get the temp variable of left hand side.
        2. Use mv.visitAssignment to emit an assignment instruction.
        3. Set the 'val' attribute of expr as the value of assignment instruction.
        """
        # * Step 5
        # * Step 10
        lhs_symbol: VarSymbol = expr.lhs.getattr("symbol")
        expr.rhs.accept(self, mv)
        val_tmp = expr.rhs.getattr("val")
        if lhs_symbol.isGlobal:
            # ? 全局变量的赋值
            addr_tmp = mv.freshTemp()
            mv.visitLoadSymbol(addr_tmp, lhs_symbol.name)
            mv.visitStoreW(val_tmp, addr_tmp, 0)
            expr.setattr("val", val_tmp)
        else:
            # ? 局部变量的赋值
            lhs_temp = expr.lhs.getattr("symbol").temp
            val_tmp = mv.visitAssignment(lhs_temp, val_tmp)
            expr.setattr("val", val_tmp)

    def visitIf(self, stmt: If, mv: FuncVisitor) -> None:
        stmt.cond.accept(self, mv)

        if stmt.otherwise is NULL:
            skipLabel = mv.freshLabel()
            mv.visitCondBranch(
                tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), skipLabel
            )
            stmt.then.accept(self, mv)
            mv.visitLabel(skipLabel)
        else:
            skipLabel = mv.freshLabel()
            exitLabel = mv.freshLabel()
            mv.visitCondBranch(
                tacop.CondBranchOp.BEQ, stmt.cond.getattr("val"), skipLabel
            )
            stmt.then.accept(self, mv)
            mv.visitBranch(exitLabel)
            mv.visitLabel(skipLabel)
            stmt.otherwise.accept(self, mv)
            mv.visitLabel(exitLabel)

    def visitWhile(self, stmt: While, mv: FuncVisitor) -> None:
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()
        mv.openLoop(breakLabel, loopLabel)

        mv.visitLabel(beginLabel)
        stmt.cond.accept(self, mv)
        mv.visitCondBranch(tacop.CondBranchOp.BEQ,
                           stmt.cond.getattr("val"), breakLabel)

        stmt.body.accept(self, mv)
        mv.visitLabel(loopLabel)
        mv.visitBranch(beginLabel)
        mv.visitLabel(breakLabel)
        mv.closeLoop()

    def visitUnary(self, expr: Unary, mv: FuncVisitor) -> None:
        expr.operand.accept(self, mv)

        op = {
            node.UnaryOp.Neg: tacop.UnaryOp.NEG,
            # You can add unary operations here.
            # add the logicnot and bitnot operation
            node.UnaryOp.Not: tacop.UnaryOp.SEQZ,
            node.UnaryOp.BitNot: tacop.UnaryOp.NOT,
        }[expr.op]
        expr.setattr("val", mv.visitUnary(op, expr.operand.getattr("val")))

    def visitBinary(self, expr: Binary, mv: FuncVisitor) -> None:
        expr.lhs.accept(self, mv)
        expr.rhs.accept(self, mv)

        op = {
            node.BinaryOp.Add: tacop.BinaryOp.ADD,
            # TODO
            # You can add binary operations here.
            node.BinaryOp.Sub: tacop.BinaryOp.SUB,
            node.BinaryOp.Mul: tacop.BinaryOp.MUL,
            node.BinaryOp.Div: tacop.BinaryOp.DIV,
            node.BinaryOp.Mod: tacop.BinaryOp.REM,

            node.BinaryOp.LT: tacop.BinaryOp.SLT,
            node.BinaryOp.GT: tacop.BinaryOp.SGT,
            node.BinaryOp.LE: tacop.BinaryOp.LEQ,
            node.BinaryOp.GE: tacop.BinaryOp.GEQ,
            node.BinaryOp.EQ: tacop.BinaryOp.EQU,
            node.BinaryOp.NE: tacop.BinaryOp.NEQ,
            node.BinaryOp.LogicAnd: tacop.BinaryOp.LAND,
            node.BinaryOp.LogicOr: tacop.BinaryOp.LOR}[expr.op]
        expr.setattr(
            "val", mv.visitBinary(op, expr.lhs.getattr(
                "val"), expr.rhs.getattr("val"))
        )

    def visitCondExpr(self, expr: ConditionExpression, mv: FuncVisitor) -> None:
        """
        1. Refer to the implementation of visitIf and visitBinary.
        """
        # * Step 6
        # * assign the temp variable in conditional expression to the val attribute
        expr.cond.accept(self, mv)

        skipLabel = mv.freshLabel()
        exitLabel = mv.freshLabel()
        temp = mv.freshTemp()
        mv.visitCondBranch(
            tacop.CondBranchOp.BEQ, expr.cond.getattr("val"), skipLabel
        )
        expr.then.accept(self, mv)
        mv.visitAssignment(temp, expr.then.getattr("val"))
        expr.setattr("val", temp)
        mv.visitBranch(exitLabel)
        mv.visitLabel(skipLabel)
        expr.otherwise.accept(self, mv)
        mv.visitAssignment(
            temp, expr.otherwise.getattr("val"))
        expr.setattr("val", temp)
        mv.visitLabel(exitLabel)

    def visitIntLiteral(self, expr: IntLiteral, mv: FuncVisitor) -> None:
        expr.setattr("val", mv.visitLoad(expr.value))

    # * Step 8
    def visitFor(self, stmt: For, mv: FuncVisitor) -> None:
        # * initialize the for loop
        stmt.init.accept(self, mv) if stmt.init is not NULL else None
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()
        mv.openLoop(breakLabel, loopLabel)

        mv.visitLabel(beginLabel)
        if stmt.cond is not NULL:
            stmt.cond.accept(self, mv)
            mv.visitCondBranch(tacop.CondBranchOp.BEQ,
                               stmt.cond.getattr("val"), breakLabel)

        stmt.body.accept(self, mv)
        mv.visitLabel(loopLabel)
        stmt.step.accept(self, mv) if stmt.step is not NULL else None
        mv.visitBranch(beginLabel)
        mv.visitLabel(breakLabel)
        mv.closeLoop()

    def visitDoWhile(self, stmt: DoWhile, mv: FuncVisitor) -> None:
        beginLabel = mv.freshLabel()
        loopLabel = mv.freshLabel()
        breakLabel = mv.freshLabel()
        mv.openLoop(breakLabel, loopLabel)

        mv.visitLabel(beginLabel)
        stmt.body.accept(self, mv)

        mv.visitLabel(loopLabel)
        stmt.cond.accept(self, mv)
        mv.visitCondBranch(tacop.CondBranchOp.BEQ,
                           stmt.cond.getattr("val"), breakLabel)

        mv.visitBranch(beginLabel)
        mv.visitLabel(breakLabel)
        mv.closeLoop()

    def visitContinue(self, stmt: Continue, mv: FuncVisitor) -> None:
        mv.visitBranch(mv.getContinueLabel())
