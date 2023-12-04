def parse_input(filename):
    lines = open(filename).read().split("\n")[:-1]
    output = []
    for line in lines:
        output.append([int(n) for n in line.split("x")])
    return output

def surface_area(dims):
    return 2*(dims[0]*dims[1] + dims[1]*dims[2] + dims[0]*dims[2])

def smallest_side(dims):
    sorted_dims = sorted(dims)
    return sorted_dims[0]*sorted_dims[1]

def paper_needed(dims):
    return surface_area(dims) + smallest_side(dims)

def smallest_perimeter(dims):
    sorted_dims = sorted(dims)
    return 2*sorted_dims[0] + 2*sorted_dims[1]

def volume(dims):
    return dims[0]*dims[1]*dims[2]

def ribbon_needed(dims):
    return smallest_perimeter(dims) + volume(dims)

def prob2a(filename):
    dims_list = parse_input(filename)
    total_paper = 0
    for dims in dims_list:
        total_paper += paper_needed(dims)
    print(total_paper)

def prob2b(filename):
    dims_list = parse_input(filename)
    total_ribbon = 0
    for dims in dims_list:
        total_ribbon += ribbon_needed(dims)
    print(total_ribbon)

prob2a("input2.txt")
prob2b("test2.txt")
prob2b("input2.txt")
