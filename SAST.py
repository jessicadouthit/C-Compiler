"""
Author:    Deanna M. Wilborne
Created:    2025-04-08
Purpose:    Simple Abstract Syntax Tree Class
Course:    25SP.CSC486 - Compiler Design & Interpretation
History:
           2025-04-08, DMW, created
"""




# noinspection SpellCheckingInspection
class SAST:
   def __init__(self, name: str, value: {} = None, struct: {} = None, parent=None,
                children: [] = None, lineno: int = None, lexpos: int = None) -> None:
       self.name = name
       self.parent = parent


       if value is None:
           self.value = {'type': None}
       else:
           self.value = value


       if struct is None:
           self.struct = {'term': False}
       else:
           self.struct = struct


       # 2023-04-16, DWM, line and index is based on:
       # https://my.eng.utah.edu/~cs3100/lectures/l14/ply-3.4/doc/ply.html#ply_nn33
       self.lineno = lineno
       self.lexpos = lexpos


       if children is not None:
           self.children = children