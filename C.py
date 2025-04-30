#!/usr/bin/env python

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
#
# Class-based example contributed to PLY by David McNab
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Updates by Deanna M. Wilborne
#   2024-04-29
#       * # noinspection PyMethodMayBeStatic added to methods that look static
#       * renamed debugfile to debug_file
#       * # noinspection SpellCheckingInspection added where needed
#       * # noqa added to __init__() for exception handling to supress warning
#       * # noinspection PyPep8Naming added where needed
#       * single quoted document strings converted to triple quoted
# -----------------------------------------------------------------------------

from AST import AST, NodeMixin
from anytree import NodeMixin
import ply.lex as lex
import ply.yacc as yacc
import os
import sys


class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                1] + "_" + self.__class__.__name__
        # 2024-04-29, DMW, TODO: figure out the appropriate exceptions to handle and narrow
        except:  # noqa
            modname = "parser" + "_" + self.__class__.__name__
        self.debug_file = modname + ".dbg"
        # print self.debug_file

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debug_file)

    # noinspection PyMethodMayBeStatic
    def run(self):
        a = """
        a =
        """
        # while True:
        #     try:
        #         s = input('calc > ')
        #     except EOFError:
        #         break
        #     if not s:
        #         continue
        temp = yacc.parse(a)
        AST.render_tree(temp)

        # def emit_mips(self,f,node):
        #     if node.name == 'EQUALS':
        #         var_name = node.children[0].value
        #         expr_node = node.children[1]




class Calc(Parser):

    # noinspection SpellCheckingInspection
    tokens = (
        'NAME', 'NUMBER',
        'PLUS', 'MINUS', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN',
    )

    # Tokens

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_EXP = r'\*\*'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS = r'\='
    # noinspection SpellCheckingInspection
    t_LPAREN = r'\('
    # noinspection SpellCheckingInspection
    t_RPAREN = r'\)'
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # noinspection PyPep8Naming
    # noinspection PyMethodMayBeStatic
    def t_NUMBER(self, t):
        r"""\d+"""
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        # print "parsed number %s" % repr(t.value)


    t_ignore = " \t"

    # noinspection PyMethodMayBeStatic
    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += t.value.count("\n+")
        return t
        #fun-definition ::= void t_newline(t) compound-statement
       # fun-signature ::= void t_newline(t) '('t')'
        #compound-stmt ::= '{'statement-list'}'
        #statement-list ::= expression-stmt
        #expression-stmt ::= t.lexer.lineno += t.value.count("\n")
        #str-const ::= '"\n+"'
    # noinspection PyMethodMayBeStatic
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    # noinspection SpellCheckingInspection
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EXP'),
        ('right', 'UMINUS'),
    )

    def p_statement_assign(self, p):
        """statement : NAME '=' expression"""
        #self.names[p[1]] = p[3]
        p[0] = AST("var_assign", value=p[3])
        # fun-definition::= void p_statement_assign(p) compound-statement
        # statement ::= primary EQUALS expression
        #p[0] = AST("NAME", value=self.names[p[1]])
    # noinspection PyMethodMayBeStatic

    def p_statement_expr(self, p):
        """statement : expression"""
        p[0] = p[1]
       # print(p[1])
    # fun-definition::= void p_statement_expr(p) compound-statement
    # statement ::= PRIMARY is Secondary- Check!!!!! or convert to AST for better conversion

    # noinspection SpellCheckingInspection
    # noinspection PyMethodMayBeStatic
    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXP expression
        """
        # print [repr(p[i]) for i in range(0,4)]
        if p[2] == '+':
            p[0] = AST("PLUS", children=[p[1], p[3]])
            #if (p[2] == '+') { p[0] = AST("PLUS", children=[p[1], p[3]])}
        elif p[2] == '-':
            p[0] = AST("MINUS", children=[p[1], p[3]])
            # if (p[2] == '-') { p[0] = AST("MIINUS", children=[p[1], p[3]])}
        elif p[2] == '*':
            p[0] = AST("TIMES", children=[p[1], p[3]])
            # if (p[2] == '*') { p[0] = AST("TIMES", children=[p[1], p[3]])}
        elif p[2] == '/':
            p[0] = AST("DIVIDE", children=[p[1], p[3]])
            # if (p[2] == '/') { p[0] = AST("DIVIDE", children=[p[1], p[3]])}
        elif p[2] == '**':
            p[0] = AST("EXP", children=[p[1], p[3]])
            # if (p[2] == '**') { p[0] = AST("EXP", children=[p[1], p[3]])}

    # noinspection PyMethodMayBeStatic
    # noinspection SpellCheckingInspection

    def p_expression_uminus(self, p):
        """expression : MINUS expression %prec UMINUS"""
        #p[0] = -p[2]
        p[0] = AST("UMINUS", children=[p[2]])
        # fun-definition::= void p_expression_uminus(p) compound-statement
        # statement ::= primary UMINUS expression
        #figure out how to turn AST into negative

        # fun-definition::=


    # noinspection SpellCheckingInspection
    # noinspection PyMethodMayBeStatic
    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = AST("LPAREN", children=[p[2]])
        # fun-definition::= void p_expression_group(p) compound-statement
        # statement ::= primary LPAREN expression
    # noinspection PyMethodMayBeStatic
    def p_expression_number(self, p):
        """expression : NUMBER"""
        p[0] = AST("NUMBER", value=p[1])
        # fun-definition::= void p_expression_number(p) compound-statement
        #AST("Number", value =p[1]) {return value;} ?-Look at grammar explaination!
        # statement ::= primary NUMBER expression

    def p_expression_name(self, p):
        """expression : NAME"""
        try:
            p[0] = AST("NAME", value=self.names[p[1]])
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = AST("NAME", value=p[2])

    # noinspection PyMethodMayBeStatic
    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':

    # if len(sys.argv) < 2:
    #     print("Usage:C c.py<source_file>")
    # else:
    #     input_file = sys.argv[1]
    #     output_file = input_file.replace(".py", ".asm")
    #
    # with open(C,"r") as f:
    #     code = f.read()
    calc = Calc()
    calc.run()
