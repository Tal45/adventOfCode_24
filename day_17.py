# question & input can be found @ https://adventofcode.com/2024/day/17
import re

operand = {
    4: 0,
    5: 1,
    6: 2
}


def adv(op2, regs):
    a, b, c = regs
    tmp = op2 if op2 <= 3 else regs[operand[op2]]
    a = int(a / pow(2, tmp))
    return (a, b, c), None


def bxl(op2, regs):
    a, b, c = regs
    b = b ^ op2
    return (a, b, c), None


def bst(op2, regs):
    a, b, c = regs
    b = op2 % 8 if op2 <= 3 else regs[operand[op2]] % 8
    return (a, b, c), None


def bxc(op2, regs):
    a, b, c = regs
    b = b ^ c
    return (a, b, c), None


def out(op2, regs):
    a, b, c = regs
    return (a, b, c), [op2 % 8 if op2 <= 3 else regs[operand[op2]] % 8]


def bdv(op2, regs):
    a, b, c = regs
    tmp = op2 if op2 <= 3 else regs[operand[op2]]
    b = int(a / pow(2, tmp))
    return (a, b, c), None


def cdv(op2, regs):
    a, b, c = regs
    tmp = op2 if op2 <= 3 else regs[operand[op2]]
    c = int(a / pow(2, tmp))
    return (a, b, c), None


opcode = {
    0: adv,
    1: bxl,
    2: bst,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}


def parse_input(dir):
    pattern = r'(\d+)'
    with open(dir, "r") as file:
        inp = file.read()
    x = [int(y) for y in re.findall(pattern, inp)]
    reg_a = x.pop(0)
    reg_b = x.pop(0)
    reg_c = x.pop(0)

    return (reg_a, reg_b, reg_c), x


def run_program(ins, regs):
    out = []
    ic = 0
    while ic < len(ins):
        if ic % 2 == 0:
            op1, op2 = ins[ic], ins[ic + 1]
            ic += 2
        else:
            op1, op2 = ins[ic - 1], ins[ic]
            ic += 1
        if op1 == 3:
            if regs[0]:
                ic = op2
        else:
            regs, out_tmp = opcode[op1](op2, regs)
            if out_tmp:
                out += out_tmp

    return out


def find_a_value(ins):
    a = 0
    for idx in range(len(ins) - 1, -1, -1):
        a <<= 3
        while run_program(ins, (a, 0, 0)) != ins[idx:]:
            a += 1
    return a


if __name__ == '__main__':
    input_dir = "inputfiles/day17.txt"
    regs, ins = parse_input(input_dir)
    regs_copy = regs
    o1 = run_program(ins, regs_copy)
    print(o1)
    print(find_a_value(ins))
