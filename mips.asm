.data
array:      .space 400
promptN:    .asciiz "Enter array size: "
promptVal:  .asciiz "Enter element: "
promptTar:  .asciiz "Enter target: "
resultMsg:  .asciiz "Number of pairs: "

.text
.globl main

main:

    li $v0, 4
    la $a0, promptN
    syscall

    li $v0, 5
    syscall
    move $s1, $v0

    la $t0, array
    li $t1, 0

input_loop:
    beq $t1, $s1, input_done

    li $v0, 4
    la $a0, promptVal
    syscall

    li $v0, 5
    syscall

    sll $t2, $t1, 2
    add $t3, $t0, $t2
    sw  $v0, 0($t3)

    addi $t1, $t1, 1
    j input_loop

input_done:

    li $v0, 4
    la $a0, promptTar
    syscall

    li $v0, 5
    syscall
    move $s0, $v0

    li $t1, 0
    li $t9, 0

loop1:
    beq $t1, $s1, print_result
    addi $t2, $t1, 1

loop2:
    beq $t2, $s1, next_i

    sll $t3, $t1, 2
    add $t4, $t0, $t3
    lw  $t5, 0($t4)

    sll $t6, $t2, 2
    add $t7, $t0, $t6
    lw  $t8, 0($t7)

    add $t3, $t5, $t8
    bne $t3, $s0, skip

    addi $t9, $t9, 1

skip:
    addi $t2, $t2, 1
    j loop2

next_i:
    addi $t1, $t1, 1
    j loop1

print_result:
    li $v0, 4
    la $a0, resultMsg
    syscall

    li $v0, 1
    move $a0, $t9
    syscall

    li $v0, 10
    syscall