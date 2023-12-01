def run_program(prog, a=0, b=0):
    counter = 0
    reg = {'a': a, 'b': b}
    while counter >= 0 and counter < len(prog):
        inst_str = prog[counter]
        inst = inst_str.split()
        print(f"{inst_str}\t a={reg['a']} b={reg['b']} {counter=}")
        if inst[0] == 'hlf':
            if reg[inst[1]] % 2 != 0:
                raise ValueError("Undefined behavior: tried to halve an odd number.")
            reg[inst[1]] //= 2
        elif inst[0] == 'tpl':
            reg[inst[1]] *= 3
        elif inst[0] == 'inc':
            reg[inst[1]] += 1
        elif inst[0] == 'jmp':
            counter += int(inst[1])-1
        elif inst[0] == 'jio':
            if reg[inst[1][0]] == 1:
                counter += int(inst[2])-1
        elif inst[0] == 'jie':
            if reg[inst[1][0]] % 2 == 0:
                counter += int(inst[2])-1
        counter += 1
    return reg

if __name__ == "__main__":
    # print(run_program(["inc a", "jio a, +2", "tpl a", "inc a"]))
    prog = open("input23.txt", 'r').read().split("\n")[:-1]
    print(run_program(prog))
    print(run_program(prog, a=1, b=0))


