"""
Module that defines a parser using `ply.yacc`.
Add your own parser rules on demand, which can be accomplished by:

1. Define a global function whose name starts with "p_".
2. Write the corresponding grammar rule(s) in its docstring.
3. Complete the function body, which is actually a syntax base translation process.
    We're using this technique to build up the AST.

Refer to https://www.dabeaz.com/ply/ply.html for more details.
"""


import ply.yacc as yacc

from frontend.ast.tree import *
from frontend.lexer import lex
from utils.error import DecafSyntaxError

tokens = lex.tokens
error_stack = list[DecafSyntaxError]()


# 根据算符来搜索相应的一元操作符
def unary(p):
    p[0] = Unary(UnaryOp.backward_search(p[1]), p[2])


def binary(p):
    if p[2] == BinaryOp.Assign.value:
        p[0] = Assignment(p[1], p[3])
    else:
        p[0] = Binary(BinaryOp.backward_search(p[2]), p[1], p[3])


def p_empty(p: yacc.YaccProduction):
    """
    empty :
    """
    pass


# * Step 9 done
def p_program(p):
    """
    program : program function
    """
    p[1].children.append(p[2])
    p[0] = p[1]


def p_program_single_function(p):
    """
    program : function
    """
    p[0] = Program(p[1])


# * Step 10 done
def p_global_var(p):
    """
    program : program declaration Semi
    """
    p[1].children.append(p[2])
    p[0] = p[1]


def p_global_var_single(p):
    """
    program : declaration Semi
    """
    p[0] = Program(p[1])


def p_type(p):
    """
    type : Int
    """
    p[0] = TInt()


# * Step 9
def p_function_def(p):
    """
    function : type Identifier LParen parameter_list RParen LBrace block RBrace
    """
    p[0] = Function(p[1], p[2], p[4], p[7])


def p_function_decl(p):
    """
    function : type Identifier LParen parameter_list RParen Semi
    """
    p[0] = Function(p[1], p[2], p[4], None)


def p_block(p):
    """
    block : block block_item
    """
    if p[2] is not NULL:
        p[1].children.append(p[2])
    p[0] = p[1]


def p_block_empty(p):
    """
    block : empty
    """
    p[0] = Block()


def p_block_item(p):
    """
    block_item : statement
        | declaration Semi
    """
    p[0] = p[1]


def p_statement(p):
    """
    statement : statement_matched
        | statement_unmatched
    """
    p[0] = p[1]


def p_if_else(p):
    """
    statement_matched : If LParen expression RParen statement_matched Else statement_matched
    statement_unmatched : If LParen expression RParen statement_matched Else statement_unmatched
    """
    p[0] = If(p[3], p[5], p[7])


def p_if(p):
    """
    statement_unmatched : If LParen expression RParen statement
    """
    p[0] = If(p[3], p[5])


def p_while(p):
    """
    statement_matched : While LParen expression RParen statement_matched
    statement_unmatched : While LParen expression RParen statement_unmatched
    """
    p[0] = While(p[3], p[5])


def p_return(p):
    """
    statement_matched : Return expression Semi
    """
    p[0] = Return(p[2])


def p_expression_statement(p):
    """
    statement_matched : opt_expression Semi
    """
    p[0] = p[1]


def p_block_statement(p):
    """
    statement_matched : LBrace block RBrace
    """
    p[0] = p[2]


def p_break(p):
    """
    statement_matched : Break Semi
    """
    p[0] = Break()


def p_opt_expression(p):
    """
    opt_expression : expression
    """
    p[0] = p[1]


def p_opt_expression_empty(p):
    """
    opt_expression : empty
    """
    p[0] = NULL


def p_declaration(p):
    """
    declaration : type Identifier
    """
    p[0] = Declaration(p[1], p[2])


def p_declaration_init(p):
    """
    declaration : type Identifier Assign expression
    """
    p[0] = Declaration(p[1], p[2], p[4])


def p_expression_precedence(p):
    """
    expression : assignment
    assignment : conditional
    conditional : logical_or
    logical_or : logical_and
    logical_and : bit_or
    bit_or : xor
    xor : bit_and
    bit_and : equality
    equality : relational
    relational : additive
    additive : multiplicative
    multiplicative : unary
    unary : postfix
    postfix : primary
    """
    p[0] = p[1]


def p_unary_expression(p):
    """
    unary : Minus unary
        | BitNot unary
        | Not unary
    """
    unary(p)


def p_binary_expression(p):
    """
    assignment : unary Assign expression
    logical_or : logical_or Or logical_and
    logical_and : logical_and And bit_or
    bit_or : bit_or BitOr xor
    xor : xor Xor bit_and
    bit_and : bit_and BitAnd equality
    equality : equality NotEqual relational
        | equality Equal relational
    relational : relational Less additive
        | relational Greater additive
        | relational LessEqual additive
        | relational GreaterEqual additive
    additive : additive Plus multiplicative
        | additive Minus multiplicative
    multiplicative : multiplicative Mul unary
        | multiplicative Div unary
        | multiplicative Mod unary
    """
    binary(p)


def p_conditional_expression(p):
    """
    conditional : logical_or Question expression Colon conditional
    """
    p[0] = ConditionExpression(p[1], p[3], p[5])


def p_int_literal_expression(p):
    """
    primary : Integer
    """
    p[0] = p[1]


def p_identifier_expression(p):
    """
    primary : Identifier
    """
    p[0] = p[1]


def p_brace_expression(p):
    """
    primary : LParen expression RParen
    """
    p[0] = p[2]


def p_error(t):
    """
    A naive (and possibly erroneous) implementation of error recovering.
    """
    if not t:
        error_stack.append(DecafSyntaxError(t, "EOF"))
        return

    inp = t.lexer.lexdata
    error_stack.append(DecafSyntaxError(
        t, f"\n{inp.splitlines()[t.lineno - 1]}"))

    parser.errok()
    return parser.token()


# * Step 8
def p_for(p):
    """
    statement_matched : For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_matched
    statement_unmatched : For LParen opt_expression Semi opt_expression Semi opt_expression RParen statement_unmatched
    statement_matched : For LParen declaration Semi opt_expression Semi opt_expression RParen statement_matched
    statement_unmatched : For LParen declaration Semi opt_expression Semi opt_expression RParen statement_unmatched
    """
    p[0] = For(p[9], p[3], p[5], p[7])


def p_dowhile(p):
    """
    statement_matched : Do statement_matched While LParen expression RParen Semi
    statement_unmatched : Do statement_unmatched While LParen expression RParen Semi
    """
    p[0] = DoWhile(p[5], p[2])


def p_continue(p):
    """
    statement_matched : Continue Semi
    """
    p[0] = Continue()


# * Step 12
def p_parameter(p):
    """
    parameter : parameter_item
        | parameter_arr_single
        | parameter_arr_multi
    """
    p[0] = p[1]


# * Step 12
def p_array_parameter_single_empty(p):
    """
    parameter_arr_single : parameter_item LBracket empty RBracket
    """
    p[1].dims.append(-1)
    p[1].var_t = TArray(p[1].var_t.type, p[1].dims)
    p[0] = p[1]


# * Step 12
def p_array_parameter_single(p):
    """
    parameter_arr_single : parameter_item LBracket Integer RBracket
    """
    p[1].dims.append(p[3].value)
    p[1].var_t = TArray(p[1].var_t.type, p[1].dims)
    p[0] = p[1]


# * Step 12
def p_array_parameter_multi(p):
    """
    parameter_arr_multi : parameter_arr_single LBracket Integer RBracket
    """
    p[1].dims.append(p[3].value)
    p[1].var_t = TArray(p[1].var_t.type.full_indexed, p[1].dims)
    p[0] = p[1]


# * Step 9 done
def p_parameter_item(p):
    """
    parameter_item : type Identifier
    """
    p[0] = Parameter_item(p[1], p[2])


# * Step 9 done
def p_parameter_list(p):
    """
    parameter_list : parameter_list Comma parameter
    """
    if p[3] is not NULL:
        p[1].children.append(p[3])
    p[0] = p[1]


# * Step 9 done
def p_parameter_single(p):
    """
    parameter_list : parameter
    """
    p[0] = Parameter_list()
    p[0].children.append(p[1])


# * Step 9 done
def p_parameter_empty(p):
    """
    parameter_list : empty
    """
    p[0] = Parameter_list()


# * Step 9 done
def p_expression_list(p):
    """
    expression_list : expression_list Comma expression
    """
    p[1].children.append(p[3])
    p[0] = p[1]


# * Step 9 done
def p_expression_single(p):
    """
    expression_list : expression
    """
    p[0] = Expression_list()
    p[0].children.append(p[1])


# * Step 9 done
def p_expression_empty(p):
    """
    expression_list : empty
    """
    p[0] = Expression_list()


# * Step 9 done
def p_call(p):
    """
    postfix : Identifier LParen expression_list RParen
    """
    p[0] = Call(p[1], p[3])


# * Step 11 done
def p_postfix_array(p):
    """
    postfix : multidim_arr 
        | singledim_arr
    """
    p[0] = p[1]


# * Step 11 done
def p_postfix_array_singledim(p):
    """
    singledim_arr : Identifier LBracket expression RBracket
    """
    p[0] = IndexExpression(p[1], p[3])


# * Step 11 done
def p_postfix_array_multidim(p):
    """
    multidim_arr : singledim_arr LBracket expression RBracket 
        | multidim_arr LBracket expression RBracket
    """
    p[1].indexes.append(p[3])
    p[0] = p[1]


# * Step 11 done
def p_decl_array(p):
    """
    declaration : multidim_decl 
        | singledim_decl
    """
    p[0] = p[1]


# * Step 11 done
def p_decl_array_singledim(p):
    """
    singledim_decl : type Identifier LBracket Integer RBracket
    """
    p[0] = Declaration(TArray(p[1].type, [p[4].value]), p[2])
    p[0].isArray = True
    p[0].dims.append(p[4].value)


# * Step 11 done
def p_decl_array_multidim(p):
    """
    multidim_decl : singledim_decl LBracket Integer RBracket
        | multidim_decl LBracket Integer RBracket
    """
    p[1].dims.append(p[3].value)
    p[1].var_t = TArray(p[1].var_t.type.full_indexed, p[1].dims)
    p[0] = p[1]


# * Step 12
def p_intlist_empty(p):
    """
    intlist : empty
    """
    p[0] = Integer_list()


# * Step 12
def p_intlist_single(p):
    """
    intlist : Integer
    """
    p[0] = Integer_list()
    p[0].children.append(p[1].value)


# * Step 12
def p_intlist_multi(p):
    """
    intlist : intlist Comma Integer
    """
    p[1].children.append(p[3].value)
    p[0] = p[1]


# * Step 12
def p_arrinit(p):
    """
    declaration : multidim_decl Assign LBrace intlist RBrace
        | singledim_decl Assign LBrace intlist RBrace
    """
    p[1].init_expr = p[4]
    p[0] = p[1]


parser = yacc.yacc(start="program")
parser.error_stack = error_stack  # type: ignore
