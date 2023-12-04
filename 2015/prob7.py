def process(instructions):
    signals = dict()
    while instructions:
        unused_instructions = []
        # print(f"{signals=}")
        for inst in instructions:
            words = inst.split()
            # literal assignment
            if words[0].isnumeric():
                signals[words[2]] = int(words[0])
            # unary operators
            elif words[0] == "NOT":
                if words[1] in signals:
                    signals[words[3]] = ~signals[words[1]]
                else:
                    unused_instructions.append(inst)
            # binary operators
            elif words[1] in {"AND", "OR"}:
                if words[0] in signals and words[2] in signals:
                    if words[1] == "AND":
                        signals[words[4]] = signals[words[0]] & signals[words[2]]
                    elif words[1] == "OR":
                        signals[words[4]] = signals[words[0]] | signals[words[2]]
                    else:
                        raise ValueError("Unrecognized instruction", inst)
                else:
                    unused_instructions.append(inst)
            # shift operators
            elif words[1] in {"LSHIFT", "RSHIFT"}:
                if words[0] in signals:
                    if words[1] == "LSHIFT":
                        signals[words[4]] = signals[words[0]] << int(words[2])
                    elif words[1] == "RSHIFT":
                        signals[words[4]] = signals[words[0]] >> int(words[2])
                    else:
                        raise ValueError("Unrecognized instruction", inst)
                else:
                    unused_instructions.append(inst)
            # variable copy
            elif words[1] == "->":
                if words[0] in signals:
                    signals[words[2]] = signals[words[0]]
                else:
                    unused_instructions.append(inst)
            else:
                raise ValueError("Unrecognized instruction", inst)
        instructions = unused_instructions
        print(f"{signals=}, {unused_instructions=}")
    print(signals)


def signal_value(name, instructions, known_dict = dict()):
    # Check for literal value
    if name.isnumeric():
        return int(name), known_dict
    # Check if already known
    if name in known_dict:
        return known_dict[name], known_dict
    # Find relevant instructions
    relevant = []
    for inst in instructions:
        words = inst.split()
        # find instructions calculating the given signal
        if words[-1] == name:
            relevant.append(words)
    assert len(relevant) == 1
    words = relevant[0]
    print(len(known_dict))
    # assignment
    if words[1] == "->":
        value, known_dict = signal_value(words[0], instructions, known_dict)
    # unary operators
    elif words[0] == "NOT":
        input = signal_value(words[1], instructions, known_dict)
        value, known_dict = ~input[0], input[1]
    # binary operators
    elif words[1] == "AND":
        input1, known_dict = signal_value(words[0], instructions, known_dict)
        input2, known_dict = signal_value(words[2], instructions, known_dict)
        value = input1 & input2
    elif words[1] == "OR":
        input1, known_dict = signal_value(words[0], instructions, known_dict)
        input2, known_dict = signal_value(words[2], instructions, known_dict)
        value = input1 | input2
    # shift operators
    elif words[1] == "LSHIFT":
        input1, known_dict = signal_value(words[0], instructions, known_dict)
        input2, known_dict = signal_value(words[2], instructions, known_dict)
        value = input1 << input2
    elif words[1] == "RSHIFT":
        input1, known_dict = signal_value(words[0], instructions, known_dict)
        input2, known_dict = signal_value(words[2], instructions, known_dict)
        value = input1 >> input2
    else:
        raise ValueError("Unrecognized instruction", inst)
    if value < 0:
        value = value + 65536
    known_dict[name] = value
    return value, known_dict


def test():
    instructions = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""".split("\n")
    print(signal_value("d", instructions))
    print("\n\n")
    instructions = ["0 -> c", "14146 -> b", "b RSHIFT 2 -> d"]
    print(signal_value("d", instructions, dict()))


def prob7a():
    instructions = open("input7.txt").read().split("\n")[:-1]
    return signal_value("a", instructions)

def prob7b():
    instructions = open("input7.txt").read().split("\n")[:-1]
    return signal_value("a", instructions, {"b": 956})

if __name__ == "__main__":
    print(prob7b())
