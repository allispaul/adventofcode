import random

def run_program(program, *args, verbose=False):
    vars = {"w": 0, "x": 0, "y": 0, "z": 0}

    explanation = [f"{args[0]} + 12 = {args[0]+12}",
                   f"{args[1]} + 6 = {args[1]+6}",
                   f"{args[2]} + 4 = {args[2]+4}",
                   f"{args[3]} + 5 = {args[3]+5}",
                   f"{args[4]}",
                   f"If {args[4]} - 7 != {args[5]}, replace with {args[5]} + 4",
                   f"Replace with {args[6]} + 15 = {args[6]+15}",
                   f"{args[7]} + 14 = {args[7]+14}",
                   f"If {args[7]} + 7 != {args[8]}, replace with {args[8]} + 6",
                   f"{args[9]} + 14 = {args[9]+14}",
                   f"If {args[9]} + 5 != {args[10]}, replace with {args[10]} + 8",
                   f"Maybe replace with {args[11]} + 5 = {args[11]+5}",
                   f"Maybe replace with {args[12]} + 14 = {args[12]+14}",
                   f"Maybe replace with {args[13]} + 4 = {args[13]+4}"]
    input_counter = 0
    for line_num, line in enumerate(program):
        words = line.split()
        if words[0] == "inp":
            if verbose:
                print(f"INPUT # {input_counter+1}")
            vars[words[1]] = args[input_counter]
            input_counter += 1
        elif words[0] == "add":
            if words[2] in "wxyz":
                vars[words[1]] += vars[words[2]]
            else:
                vars[words[1]] += int(words[2])
            if words[1] == "z":
                z = vars["z"]
                print(f"{line_num}\t\tz={decode26(z)}\t {explanation[input_counter-1]}")
        elif words[0] == "mul":
            if words[2] in "wxyz":
                vars[words[1]] *= vars[words[2]]
            else:
                vars[words[1]] *= int(words[2])
        elif words[0] == "div":
            if words[2] in "wxyz":
                vars[words[1]] //= vars[words[2]]
            else:
                vars[words[1]] //= int(words[2])
        elif words[0] == "mod":
            if words[2] in "wxyz":
                vars[words[1]] %= vars[words[2]]
            else:
                vars[words[1]] %= int(words[2])
        elif words[0] == "eql":
            if words[2] in "wxyz":
                vars[words[1]] = int(vars[words[1]] == vars[words[2]])
            else:
                vars[words[1]] = int(vars[words[1]] == int(words[2]))
        w, x, y, z = vars["w"], vars["x"], vars["y"], vars["z"]
        if verbose:
            print(f"{line}\t\t{w=} {x=} {y=} z={decode26(z)}")
    return w, x, y, z


def test():
    prog1 = ["inp x", "mul x -1"]
    w, x, y, z = run_program(prog1, 3)
    assert x == -3

    prog2 = ["inp z", "inp x", "mul z 3", "eql z x"]
    w, x, y, z = run_program(prog2, 2, 6)
    assert z == 1
    w, x, y, z = run_program(prog2, 3, 6)
    assert z == 0

    prog3 = ["inp w", "add z w", "mod z 2", "div w 2", "add y w", "mod y 2",
             "div w 2", "add x w", "mod x 2", "div w 2", "mod w 2"]
    w, x, y, z = run_program(prog3, 15)
    assert w == x == y == z == 1
    w, x, y, z = run_program(prog3, 126)
    assert w == x == y == 1
    assert z == 0


prog = open("input24.txt", "r").read().split("\n")[:-1]


def decode26(num):
    if num < 0:
        raise ValueError(f"{num} must be positive")
    if num == 0:
        return []
    return decode26(num // 26) + [num % 26]


def prob24a():
    for place1 in range(14):
        for place2 in range(place1, 14):
            for digit1 in range(1, 10):
                for digit2 in range(1, 10):
                    for rest in range(1, 10):
                        model_num = [rest for _ in range(14)]
                        model_num[place1] = digit1
                        model_num[place2] = digit2
                        w, x, y, z = run_program(prog, *model_num)
                        print(f"number = {''.join(str(x) for x in model_num)}, {z = }")
                        if z == 0:
                            return model_num


if __name__ == "__main__":
    for counter in range(1000):
        digits = [random.randrange(1, 10) for _ in range(3)] + [9]
        digits.append(random.randrange(8, 10))
        digits.append(digits[-1]-7)
        digits.append(1)
        digits.append(random.randrange(1, 3))
        digits.append(digits[-1]+7)
        digits.append(random.randrange(1, 5))
        digits.append(digits[-1]+5)
        digits += [random.randrange(1, 10) for _ in range(3)]
        assert all(1 <= digit <= 9 for digit in digits)
        assert len(digits) == 14
        print(digits)
        w, x, y, z = run_program(prog, *digits)
        z_list = decode26(z)
        assert z_list[0] == digits[0]+12
        assert z_list[1] == digits[1]+6
        # assert z_list[2] == digits[2]+4
        assert len(decode26(z)) >= 3
