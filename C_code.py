#!/usr/bin/env python

# -----------------------------------------------------------------------------
# C_code.py
#Author: Ariana Meatchem and Jessica Douthit
# Created 4/2/2025
# Course: CSC 486
# Purpose: Create a compiler that creates an AST using C grammar and emits code to MIPS assembly
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
        """Runs an input test """
        sourcefile = "Source.py"
        with open(sourcefile, "r") as f:
            source = f.read()
        a = """
        if (9 >5) print("BESTIE");
        if (5 >4) print("Hello");
        """
        runline = yacc.parse(a)
        AST.render_tree(runline)
        temp = yacc.parse(source)
        AST.render_tree(temp)

        emitter = self.emit_mips()
        emitter.generate(temp)

        outname = "output.asm"
        with open(outname, "w") as f:
            for instr in emitter.output:
                f.write(instr + "\n")

        print("Wrote output to " + outname)
        # emitter = self.emit_mips()
        # emitter.generate(temp)
        # while True:
        #     try:
        #         s = input('calc > ')
        #     except EOFError:
        #         break
        #     if not s:
        #         continue
        #     yacc.parse(s)


# Reserve = {Print}
class Calc(Parser):
    def __init__(self, repl_prompt: str = "Ready >"):
        super().__init__(debug=1)  # add debug=1 to get .dbg file with grammar
    # noinspection SpellCheckingInspection
    reserved = {
        'print': 'PRINT', 'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'equals': 'EQUALS', 'equal to': 'EQUALTO',
        'writeln': 'PRINT', 'readint': 'READINT',
    }
    tokens = (
        'NAME', 'NUMBER', 'STRING',
        'PLUS', 'MINUS', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN', 'SEMICOLON', 'LBRACE', 'RBRACE', 'IF', 'ELSE', 'WHILE', 'PRINT',
        'LESSTHAN', 'GREATERTHAN', 'EQUALTO', 'READINT',
    )

    # Token Rules/Regular Expressions
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
    t_SEMICOLON = r';'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_IF = r'if'
    t_ELSE = r'else'
    t_WHILE = r'while'
    t_LESSTHAN = r'<'
    t_GREATERTHAN = r'>'
    t_EQUALTO = r'=='
   # t_QUOTE = r'\"'

    # noinspection PyPep8Naming
    # noinspection PyMethodMayBeStatic

    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'NAME')  # Reserved word check
        return t
    def t_NUMBER(self, t):
        r"""\d+"""
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %s" % t.value)
            t.value = 0
        # print "parsed number %s" % repr(t.value)
        return t
    def t_STRING(self, t):
        r'"([^"\\]*(\\.[^"\\]*)*)"'
        t.value = t.value[1:-1] # strips the quotes
        return t

    t_ignore = " \t"

    # noinspection PyMethodMayBeStatic
    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += t.value.count("\n")

    # noinspection PyMethodMayBeStatic
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    # noinspection SpellCheckingInspection

    # Grammar Rules/Precedence (Order of Operations)
    precedence = (
        ('nonassoc', 'IF'),
        ('nonassoc', 'ELSE'),
        ('left', 'EQUALTO', 'LESSTHAN', 'GREATERTHAN'), #Comparisons take place after operations
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EXP'),
        ('right', 'UMINUS'), #Highest Precedence
    )
    start = "statement_list"
    # Grammar rules
    def p_statement_assign(self, p):
        """statement : NAME EQUALS expression SEMICOLON"""
        #self.names[p[1]] = p[3]
        p[0] = AST("val_assign", value=p[3])
    # noinspection PyMethodMayBeStatie]c

    def p_expression_string(self, p):
        """expression : STRING"""
        p[0] = AST("STRING", value=p[1])

    def p_statement_expr(self, p):
        """statement : expression SEMICOLON"""
        p[0] = p[1]
       # print(p[1])

    def p_statement_block(self, p):
        """statement : LBRACE statement_list RBRACE"""
        p[0] = AST("BLOCK", value=p[2])

    def p_block_rule(self, p):
        """block : LBRACE statement_list RBRACE"""
        p[0] = AST("BLOCK", children=[p[2]])


    def p_expression_readint(self, p):
        """expression : READINT LPAREN RPAREN"""
        p[0] = AST("READINT")

    def p_statement_if(self, p):
        """statement : IF LPAREN expression RPAREN statement
                     | IF LPAREN expression RPAREN statement ELSE statement
                     | IF LPAREN expression RPAREN block
                     | IF LPAREN expression RPAREN block ELSE block
                      """
        if len(p) == 6:
            p[0] = AST("IF", children=[p[3], p[5]])
        elif len(p) == 8:
            p[0] = AST("IF_ELSE", children=[p[3], p[5], p[7]])



    def p_statement_while(self, p):
        """statement : WHILE LPAREN expression RPAREN"""
        p[0] = AST("WHILE", children=[3])

    def p_statement_list(self, p):
        """statement_list : statement SEMICOLON statement_list
                                | statement"""
        if len(p) == 4:
            p[0] = AST("LIST", children=[p[1], p[3]])
        else:
            p[0] = p[1]

    def p_statement_print(self,p):
        """statement : PRINT LPAREN expression RPAREN SEMICOLON"""
        p[0] = AST("PRINT", children =[p[3]])

    # def p_statement_lessthan(self, p):
    #     """statement : IF statement LESSTHAN statement"""
    #     p[0] = AST("LESSTHAN", children=[p[2], p[4]])
    #
    # def p_statement_greatthan(self, p):
    #     """statement : IF statement GREATERTHAN statement"""
    #     p[0] = AST("GREATERTHAN", children=[p[2], p[4]])

    def p_expression_comparison(self,p):
        """expression : expression LESSTHAN expression
                    | expression GREATERTHAN expression
                    | expression EQUALTO expression"""
        comp_map = {
            '<': "LESSTHAN",
            '>': "GREATERTHAN",
            '==': "EQUALTO"
        }
        p[0] = AST(comp_map[p[2]], children=[p[1],p[3]])


    # def p_statement_multiline(self, p):
    #     """statement_multiline : statement SEMICOLON statement"""
    #     if len(p) == 4:
    #         p[0] = AST("multiline", children=[p[1], p[3]])
    #     else:
    #         p[0] = p[1]


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

        operation_map = {
            '+': "PLUS",
            '-': "MINUS",
            '*': "TIMES",
            '/': "DIVIDE",
            '**': "EXP"
        }
        p[0] = AST(operation_map[p[2]], children=[p[1], p[3]])

    # noinspection PyMethodMayBeStatic
    # noinspection SpellCheckingInspection
    def p_expression_uminus(self, p):
        """expression : MINUS expression %prec UMINUS"""
        #p[0] = -p[2]
        p[0] = AST("UMINUS", children=[p[2]])
    # noinspection SpellCheckingInspection
    # noinspection PyMethodMayBeStatic
    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = AST("LPAREN", children=[p[2]])

    # noinspection PyMethodMayBeStatic
    def p_expression_number(self, p):
        """expression : NUMBER"""
        p[0] = AST("NUMBER", value=p[1])

    def p_expression_name(self, p):
        """expression : NAME"""
        try:
            p[0] = AST("NAME", value=self.names[p[1]])
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = AST("NAME", value=p[1])



    # noinspection PyMethodMayBeStatic
    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    class emit_mips:
        def __init__(self):
            self.output = []
            self.var_count = 0
            self.label_count = 0

        def new_label(self):
            self.label_count += 1
            return f"L{self.label_count}"

        def generate(self, node):
            if node is None:
                print("Error: Cannot generate code from None")
                return
            if node.name == 'program':
                self.generate(node.children[0])
            elif node.name == 'function':
                self.output.append(f".text")
                self.output.append(f".globl {node.children[0].value}")
                self.output.append(f"{node.children[0].value}:")
                self.generate(node.children[1])
            elif node.name == 'return':
                self.generate(node.children[0])
                self.output.append("move $v0, $t0")
                self.output.append("jr $ra")
            elif node.name == 'binop':
                self.generate(node.children[0])
                self.output.append("move $t1, $t0")
                self.generate(node.children[1])
                if node.value == '+':
                    self.output.append("add $t0, $t1, $t0")
                elif node.value == '-':
                    self.output.append("sub $t0, $t1, $t0")
                elif node.value == '*':
                    self.output.append("mult $t0, $t1, $t0")
                elif node.value == '/':
                    self.output.append("div $t0, $t1, $t0")
                # elif node.value == '**':
                #     self.output.append("")
                elif node.value == '<':
                   self.output.append("blt $t0, $t1, $t0")
                elif node.value == '>':
                   self.output.append("bgt $t0, $t1, $t0")
                elif node.value == '==':
                   self.output.append("beq $t0, $t1, $t0")
                #Create a syscall outside the loop so that after it finds any output it prints it?
                # elif node.value == '**':
                #     self.output.append()
                elif node.name == "READINT":
                    self.output.append("load $v0,5")
                    self.output.append("syscall")
                    self.output.append("move $t0, $v0")
                elif node.name == "PRINT":
                    self.generate(node.children[0])
                    self.output.append("move $a0, $t0")
                    self.output.append("li $v0, 1")
                    self.output.append("syscall")


                # Idea: # create an output file that will hold all of the MIPS instructions
                # If node.value == 'program':
                # open("file.txt", "w") as f: #create a new file and write down instructions created based on input
                # f.write(emit_mips)


if __name__ == '__main__':
    calc = Calc()
    calc.run()
