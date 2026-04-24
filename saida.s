.data

const_zero: .double 0.0
const_um: .double 1.0
const_2: .double 5
const_3: .double 3
const_4: .double 4
const_5: .double 2
const_6: .double 10
const_7: .double 7
const_8: .double 1
const_9: .double 9
const_10: .double 0
const_11: .double 8

mem_X: .double 0.0
mem_Y: .double 0.0
mem_Z: .double 0.0

res_1: .double 0.0
res_2: .double 0.0
res_3: .double 0.0
res_4: .double 0.0
res_5: .double 0.0
res_6: .double 0.0
res_7: .double 0.0
res_8: .double 0.0
res_9: .double 0.0
res_10: .double 0.0
res_11: .double 0.0
res_12: .double 0.0

pilha: .space 8192

.text
.global _start

_start:
    LDR r10, =pilha

    LDR r0, =const_2
    VLDR d0, [r0]
    LDR r0, =mem_X
    VSTR d0, [r0]
    LDR r0, =res_1
    VSTR d0, [r0]

    LDR r0, =mem_X
    VLDR d0, [r0]
    LDR r0, =res_2
    VSTR d0, [r0]

    LDR r0, =const_3
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_4
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    VADD.F64 d0, d0, d1
    LDR r0, =res_3
    VSTR d0, [r0]

    LDR r0, =res_3
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_5
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    VMUL.F64 d0, d0, d1
    LDR r0, =res_4
    VSTR d0, [r0]

    LDR r0, =const_6
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_4
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    VSUB.F64 d0, d0, d1
    LDR r0, =res_5
    VSTR d0, [r0]

    LDR r0, =const_7
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_5
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    BL op_div_inteira
    LDR r0, =res_6
    VSTR d0, [r0]

    LDR r0, =const_7
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_5
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    VDIV.F64 d0, d0, d1
    LDR r0, =res_7
    VSTR d0, [r0]

    LDR r0, =const_7
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_3
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    BL op_resto
    LDR r0, =res_8
    VSTR d0, [r0]

    LDR r0, =const_5
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_3
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    BL op_potencia
    LDR r0, =res_9
    VSTR d0, [r0]

    LDR r0, =const_8
    VLDR d0, [r0]
    LDR r0, =const_zero
    VLDR d1, [r0]
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ fim_if_1
    LDR r0, =const_9
    VLDR d0, [r0]
    LDR r0, =mem_Y
    VSTR d0, [r0]
fim_if_1:
    LDR r0, =res_10
    VSTR d0, [r0]

    LDR r0, =const_10
    VLDR d0, [r0]
    LDR r0, =const_zero
    VLDR d1, [r0]
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ senao_2
    LDR r0, =const_8
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_5
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    VADD.F64 d0, d0, d1
    B fim_ifelse_3
senao_2:
    LDR r0, =const_3
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    LDR r0, =const_4
    VLDR d0, [r0]
    VSTR d0, [r10]
    ADD r10, r10, #8
    SUB r10, r10, #8
    VLDR d1, [r10]
    SUB r10, r10, #8
    VLDR d0, [r10]
    VADD.F64 d0, d0, d1
fim_ifelse_3:
    LDR r0, =res_11
    VSTR d0, [r0]

    LDR r0, =const_zero
    VLDR d0, [r0]
inicio_while_4:
    LDR r0, =const_10
    VLDR d0, [r0]
    LDR r0, =const_zero
    VLDR d1, [r0]
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ fim_while_5
    LDR r0, =const_11
    VLDR d0, [r0]
    LDR r0, =mem_Z
    VSTR d0, [r0]
    B inicio_while_4
fim_while_5:
    LDR r0, =res_12
    VSTR d0, [r0]

fim:
    B fim

op_div_inteira:
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    CMP r1, #0
    BEQ op_div_zero
    MOV r2, #0
    MOV r3, #0
    CMP r0, #0
    BGE op_div_a_ok
    RSB r0, r0, #0
    EOR r3, r3, #1
op_div_a_ok:
    CMP r1, #0
    BGE op_div_b_ok
    RSB r1, r1, #0
    EOR r3, r3, #1
op_div_b_ok:
op_div_loop:
    CMP r0, r1
    BLT op_div_fim_loop
    SUB r0, r0, r1
    ADD r2, r2, #1
    B op_div_loop
op_div_fim_loop:
    CMP r3, #0
    BEQ op_div_sinal_ok
    RSB r2, r2, #0
op_div_sinal_ok:
    VMOV s0, r2
    VCVT.F64.S32 d0, s0
    BX lr

op_resto:
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    CMP r1, #0
    BEQ op_div_zero
    MOV r3, #0
    CMP r0, #0
    BGE op_rest_a_ok
    RSB r0, r0, #0
    MOV r3, #1
op_rest_a_ok:
    CMP r1, #0
    BGE op_rest_b_ok
    RSB r1, r1, #0
op_rest_b_ok:
op_rest_loop:
    CMP r0, r1
    BLT op_rest_fim_loop
    SUB r0, r0, r1
    B op_rest_loop
op_rest_fim_loop:
    CMP r3, #0
    BEQ op_rest_sinal_ok
    RSB r0, r0, #0
op_rest_sinal_ok:
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    BX lr

op_potencia:
    VMOV.F64 d2, d0
    VCVT.S32.F64 s1, d1
    VMOV r1, s1
    LDR r0, =const_um
    VLDR d0, [r0]
    CMP r1, #0
    BEQ op_pot_fim
    MOV r2, #0
    CMP r1, #0
    BGE op_pot_exp_ok
    RSB r1, r1, #0
    MOV r2, #1
op_pot_exp_ok:
op_pot_loop:
    CMP r1, #0
    BEQ op_pot_loop_fim
    VMUL.F64 d0, d0, d2
    SUB r1, r1, #1
    B op_pot_loop
op_pot_loop_fim:
    CMP r2, #0
    BEQ op_pot_fim
    LDR r0, =const_um
    VLDR d1, [r0]
    VDIV.F64 d0, d1, d0
op_pot_fim:
    BX lr

op_div_zero:
    LDR r0, =const_zero
    VLDR d0, [r0]
    BX lr