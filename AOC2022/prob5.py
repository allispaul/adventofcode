import re


def crates_from_diagram(diagram):
    lines = diagram.split("\n")
    num_stacks = max(x == ' ' or int(x) for x in lines[-1])
    lists = [[line[4*i+1] for line in lines[-2::-1] if line[4*i+1] != ' ']
             for i in range(num_stacks)]
    return lists


def move_stack(n, list_a, list_b):
    if n > len(list_a):
        raise IndexError(f"Could not move {n} from {list_a} to {list_b}.")
    return list_a[:-n], list_b + list_a[:-n-1:-1]


def rearrange_crates(lists, instructions):
    for inst in instructions:
        # parse instruction
        m = re.match(r"move (\d+) from (\d+) to (\d+)", inst)
        n, fro, to = map(int, m.groups())
        # move crates
        lists[fro-1], lists[to-1] = lists[fro-1][:-n], lists[to-1] + lists[fro-1][:-n-1:-1]
    return lists

def rearrange_9001(lists, instrucitons):
    for inst in instructions:
        # parse instruction
        m = re.match(r"move (\d+) from (\d+) to (\d+)", inst)
        n, fro, to = map(int, m.groups())
        # move crates
        lists[fro-1], lists[to-1] = lists[fro-1][:-n], lists[to-1] + lists[fro-1][-n:]
    return lists


def top_crates(lists):
    return ''.join([L[-1] for L in lists])


if __name__ == "__main__":
    instructions = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".split("\n")
    diagram = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 """
    lists = crates_from_diagram(diagram)
    lists = rearrange_crates(lists, instructions)
    assert top_crates(lists) == 'CMZ'
    lists = crates_from_diagram(diagram)
    lists = rearrange_9001(lists, instructions)
    assert top_crates(lists) == 'MCD'

    diagram, instructions = open("input5.txt", "r").read().split("\n\n")
    instructions = instructions.split("\n")[:-1]
    lists = crates_from_diagram(diagram)
    lists = rearrange_crates(lists, instructions)
    print(top_crates(lists))
    lists = crates_from_diagram(diagram)
    lists = rearrange_9001(lists, instructions)
    print(top_crates(lists))


