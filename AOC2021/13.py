def parse_input(filename):
    lines = open(filename).read().split("\n")[:-1]
    lines_with_points = lines[:lines.index('')]
    points = set()
    instructions = []
    for line in lines_with_points:
        coords = line.split(',')
        points.add(tuple(int(x) for x in coords))
    instruction_lines = lines[lines.index('')+1:]
    for line in instruction_lines:
        instructions.append([line[11], int(line[13:])])
    return (points, instructions)

def fold(points, line):
    points_out = set()
    if line[0] == 'x':
        for point in points:
            if point[0] > line[1]:
                points_out.add((2*line[1] - point[0], point[1]))
            else:
                points_out.add(point)
    elif line[0] == 'y':
        for point in points:
            if point[1] > line[1]:
                points_out.add((point[0], 2*line[1] - point[1]))
            else:
                points_out.add(point)
    return points_out

def print_points(points):
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)
    print(max_x, max_y)
    for y in range(max_y+1):
        row = ""
        for x in range(max_x+1):
            if (x, y) in points:
                row += ("#")
            else:
                row += (".")
        print(row)

def test():
    points, instructions = parse_input("test13.txt")
    print(points)
    print(len(points))
    new_points = fold(points, instructions[0])
    print(new_points)
    print(len(new_points))

def prob13a():
    points, instructions = parse_input("input13.txt")
    new_points = fold(points, instructions[0])
    print(len(new_points))

def prob13b():
    points, instructions = parse_input("input13.txt")
    for instruction in instructions:
        points = fold(points, instruction)
    print(points)
    print_points(points)

test()
prob13a()
prob13b()



