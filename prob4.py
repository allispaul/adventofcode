import re

test = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".split("\n")

input = open("input4.txt", 'r').read().split("\n")[:-1]

def count_inclusions(pairs):
    count = 0
    for pair in pairs:
        bounds = list(map(int, re.match(r"(\d+)-(\d+),(\d+)-(\d+)", pair).groups()))
        if (bounds[0] >= bounds[2] and bounds[1] <= bounds[3] or
            bounds[2] >= bounds[0] and bounds[3] <= bounds[1]):
            count += 1
    return count

def count_overlaps(pairs):
    count = 0
    for pair in pairs:
        bounds = list(map(int, re.match(r"(\d+)-(\d+),(\d+)-(\d+)", pair).groups()))
        if bounds[1] >= bounds[2] and bounds[0] <= bounds[3]:
            count += 1
    return count

# idk idk
def count_inclusions_one_line(p):
    return sum((b[0]>=b[2] and b[1]<=b[3]) or (b[2]>=b[0] and b[3]<=b[1]) for a in p for b in [list(map(int, re.match(r"(\d+)-(\d+),(\d+)-(\d+)", a).groups()))])

def count_overlaps_one_line(p):
    return sum((b[1]>=b[2] and b[0]<=b[3]) for a in p for b in [list(map(int, re.match(r"(\d+)-(\d+),(\d+)-(\d+)", a).groups()))])

if __name__ == "__main__":
    assert count_inclusions(test) == 2
    print(count_inclusions(input))
    assert count_inclusions_one_line(test) == 2
    print(count_inclusions_one_line(input))
    print(count_overlaps(input))
    assert count_overlaps_one_line(test) == 4
    print(count_overlaps_one_line(input))


