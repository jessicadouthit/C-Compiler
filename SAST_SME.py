"""
Author:    Deanna M. Wilborne
Created:    2025-04-08
Purpose:    Test SAST and SME
Course:    25SP.CSC486 - Compiler Design & Interpretation
History:
           2025-04-08, DMW, created
"""

from SAST import SAST
from SME import SME


def main() -> None:
    # Team members: Yin Kyay, Diliara, Ariana
    #
    # Test 1: writeln with a static string
    writeln_str_test = SAST("writeln", value={
        'value': 'Hello, \"Yin Kyay\"', 'type': 'str'
    })
    sme1 = SME(writeln_str_test)
    sme1.emit_mips32()
    print("Test 1: writeln string")
    print(sme1.asm_text)
    print("-" * 40)

    # Test 2: writeln with a static integer
    writeln_int_test = SAST("writeln", value={
        'value': 1234, 'type': 'int'
    })
    sme2 = SME(writeln_int_test)
    sme2.emit_mips32()
    print("Test 2: writeln int")
    print(sme2.asm_text)
    print("-" * 40)

    # Test 3: write with a static string
    write_str_test = SAST("write", value={
        'value': 'No newline', 'type': 'str'
    })
    sme3 = SME(write_str_test)
    sme3.emit_mips32()
    print("Test 3: write string")
    print(sme3.asm_text)
    print("-" * 40)

    # Test 4: write with a static integer
    write_int_test = SAST("write", value={
        'value': 42, 'type': 'int'
    })
    sme4 = SME(write_int_test)
    sme4.emit_mips32()
    print("Test 4: write int")
    print(sme4.asm_text)
    print("-" * 40)


if __name__ == "__main__":
    main()
