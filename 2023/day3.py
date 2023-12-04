from collections import defaultdict

test = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

def is_symbol(char):
    return char != "." and not char.isnumeric()

def is_part_num(lines, i, start, end):
    """Check if the number on row i from start to end is touching a symbol."""
    row = lines[i]
    if start >= 1 and is_symbol(row[start-1]):
        return True
    if end < len(row)-1 and is_symbol(row[end+1]):
        return True
    adj_start = max(0, start-1)
    adj_end = min(len(row)+1, end+2)
    if i > 0 and any(is_symbol(char) for char in lines[i-1][adj_start:adj_end]):
        return True
    if i+1 < len(lines) and any(is_symbol(char) for char in lines[i+1][adj_start:adj_end]):
        return True
    return False

def prob3a(text):
    lines = text.split("\n")
    total = 0
    for i, line in enumerate(lines):
        # iterate through line
        j = 0
        while j < len(line):
            if line[j].isnumeric():
                # found a number!
                start = j
                while j < len(line) and line[j].isnumeric():
                    j += 1
                end = j-1
                if is_part_num(lines, i, start, end):
                    total += int(line[start:end+1])
            j += 1
    return total

def find_adjacent_gears(lines, i, start, end):
    """Find the gears touching the number on row i from start to end."""
    row = lines[i]
    adjacent_gears = []
    if start >= 1 and row[start-1] == "*":
        adjacent_gears.append((i, start-1))
    if end < len(row)-1 and row[end+1] == "*":
        adjacent_gears.append((i, end+1))
    # what range do we have to search on adjacent lines?
    adj_start = max(0, start-1)
    adj_end = min(len(row), end+2)
    for j in range(adj_start, adj_end):
        if i > 0 and lines[i-1][j] == "*":
            adjacent_gears.append((i-1, j))
        if i+1 < len(lines) and lines[i+1][j] == "*":
            adjacent_gears.append((i+1, j))
    return adjacent_gears


def prob3b(text):
    lines = text.split("\n")
    gears = defaultdict(list)
    for i, line in enumerate(lines):
        j = 0
        while j < len(line):
            if line[j].isnumeric():
                start = j
                while j < len(line) and line[j].isnumeric():
                    j += 1
                end = j-1
                adjacent_gears = find_adjacent_gears(lines, i, start, end)
                for pos in adjacent_gears:
                    gears[pos].append(int(line[start:end+1]))
            j += 1
    total = 0
    for pos in gears:
        if len(gears[pos]) == 2:
            total += gears[pos][0] * gears[pos][1]
    return total

if __name__ == "__main__":
    inp = open("input3", "r").read()[:-1]
    print(prob3a(test))
    print(prob3a(inp))
    print(prob3b(test))
    print(prob3b(inp))
