beqz $t0, L1
# string Please enter a valid number between 1 and 20.
move $a0, $t0
li $v0,1
syscall
j L2
L1:
move $t1, $t0
li $t0, 1
seq $t0, $t1, $t0
beqz $t0, L3
move $a0, $t0
li $v0,1
syscall
j L4
L3:
move $t1, $t0
li $t0, 2
seq $t0, $t1, $t0
beqz $t0, L5
move $a0, $t0
li $v0,1
syscall
j L6
L5:
L6:
L4:
L2:
