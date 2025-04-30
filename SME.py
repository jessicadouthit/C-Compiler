
"""
Author:    Deanna M. Wilborne
Created:    2025-04-08
Purpose:    Simple MIPS 32 Emitter
Course:    25SP.CSC486 - Compiler Design & Interpretation
History:
           2025-04-08, DMW, created
"""


from SAST import SAST
class SME:


   def __init__(self, ast: SAST = None) -> None:
       self.ast = ast
       self.asm_text = None
       self.uniq_counter: int = 0


   def emit_mips32(self) -> None:
       self.asm_text = ""


       def asm_out(code: str) -> None:
           self.asm_text = self.asm_text + code + "\n"


       def exit_asm() -> None:
           asm_out("exit:")
           asm_out("li $v0, 10")  # exit syscall. number
           asm_out("syscall")


       def prt_lf() -> None:
           asm_out("li $v0, 11")  # print character syscall number
           asm_out("li $a0, 10")  # linefeed character
           asm_out("syscall")


       def prt_str(label: str) -> None:
           asm_out("li $v0, 4")  # print string syscall number
           asm_out("la $a0, {}".format(label))  # $a0 = the pointer to the string
           asm_out("syscall")


       def get_uniq_counter(label: str = "") -> str:
           out_label = "{}_{:06d}".format(label, self.uniq_counter)
           self.uniq_counter = self.uniq_counter + 1
           return out_label


       def store_string(data_label: str, out_str: str) -> None:
           asm_out(".data")
           if '"' in out_str:
               # if true, write out string as bytes when it has nested " characters
               out_bytes = ""
               for ch in out_str:
                   out_bytes = out_bytes + str(ord(ch)) + " "
               out_bytes = out_bytes + "0 # " + out_str
               asm_out(data_label + ": .byte " + out_bytes)
           else:  # write string without nested " characters
               asm_out(data_label + ": .asciiz \"" + out_str + '"')
           asm_out(".text")


       def emit(node: SAST = None) -> None:
           if node is None:
               return


           match node.name:
               case "writeln":
                   match node.value['type']:
                       case "str":
                           data_label = get_uniq_counter("static_str") # create a pointer to use with the string
                           store_string(data_label, node.value['value']) # store the string in the data segment
                           prt_str(data_label)  # print the string stored in the data segment
                           prt_lf()
                       case "int":
                           pass
                       case "float":
                           pass
                       case _:
                           pass # unknown type, not implemented
               case "write":
                   pass
               case _:
                   pass # unknown node, not implemented


       asm_out(".text")  # start of a MIPS 32 program
       emit(self.ast)
       exit_asm()  # end of a MIPS 32 program



