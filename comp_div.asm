.section .data
    a: .long 9
    b: .long 4
    z: .long 0
    newline: .asciz "\n"

.section .bss
    buffer: .space 12

.section .text
.global _start
_start:
    # Calculate (a - b)
    mov a(%rip), %eax
    sub b(%rip), %eax
    mov %eax, %r8d          # r8d = (a - b)

    # Calculate (a + b)
    mov a(%rip), %eax
    add b(%rip), %eax
    cmp $0, %eax            # prevent division by zero
    je .error
    mov %eax, %r9d          # r9d = (a + b)

    # Perform division: (a - b) / (a + b)
    mov %r8d, %eax          # eax = numerator
    cdq                     # sign-extend eax to edx:eax
    idiv %r9d               # eax = eax / r9d
    mov %eax, z(%rip)

    # Convert result to string
    lea buffer(%rip), %rsi
    mov %eax, %edi
    call int_to_str

    # Print buffer
    mov $1, %rax
    mov $1, %rdi
    lea buffer(%rip), %rsi
    mov $12, %rdx
    syscall

    # Print newline
    mov $1, %rax
    mov $1, %rdi
    lea newline(%rip), %rsi
    mov $1, %rdx
    syscall

    # Exit
    mov $60, %rax
    xor %rdi, %rdi
    syscall

.error:
    mov $60, %rax
    mov $1, %rdi   # Exit with error code 1
    syscall

int_to_str:
    mov %rsi, %rcx
    add $11, %rcx
    movb $0, (%rcx)
    dec %rcx

    mov %edi, %eax
    cmp $0, %eax
    jge .convert

    neg %eax
    movb $'-', (%rsi)
    inc %rsi

.convert:
    xor %edx, %edx
    mov $10, %ebx

.loop:
    xor %edx, %edx
    div %ebx
    add $'0', %edx
    mov %dl, (%rcx)
    dec %rcx
    test %eax, %eax
    jnz .loop

    inc %rcx
    mov %rcx, %rsi
    ret
