color = {"RED": "\033[31m", "END": "\033[0m"}

def parse_input(filename):
    return open(filename).read().split("\n")[:-1]
# This returns a list of strings of the same length

def find_low_points(heightmap):
    """Returns a list of ordered pairs giving the (x, y) coordinates of the low
    points in the heightmap.
    """
    # Find dimensions
    Y = len(heightmap)
    X = len(heightmap[0])
    # Find low points
    low_points = []
    for y in range(Y):
        for x in range(X):
            if y > 0:
                if heightmap[y][x] >= heightmap[y-1][x]:
                    continue
            if y < Y-1:
                if heightmap[y][x] >= heightmap[y+1][x]:
                    continue
            if x > 0:
                if heightmap[y][x] >= heightmap[y][x-1]:
                    continue
            if x < X-1:
                if heightmap[y][x] >= heightmap[y][x+1]:
                    continue
            low_points.append((x, y))
    return low_points

def risk_level(point, heightmap):
    return int(heightmap[point[1]][point[0]]) + 1

def color_nines(heightmap):
    colored_map = []
    for line in heightmap:
        colored_line = ""
        for char in line:
            # colored_line += "\033[3" + char + "m" + char + color["END"]
            if char == "9":
                colored_line += color["RED"] + char + color["END"]
            else:
                colored_line += char
        colored_map.append(colored_line)
    return colored_map

def find_basin(point, heightmap):
    """point an ordered pair (x, y). Returns the set of points upwards from (x, y)
    but of height less than 9. This is a recursive procedure.
    Note there is a possible error if there are large flat areas -- in this case,
    the procedure will never find points in the center of the area."""
    Y = len(heightmap)
    X = len(heightmap[0])
    x, y = point
    basin = {point}
    if y > 0:
        if heightmap[y][x] < heightmap[y-1][x] and heightmap[y-1][x] != "9":
            basin = basin.union(find_basin((x, y-1), heightmap))
    if y < Y-1:
        if heightmap[y][x] < heightmap[y+1][x] and heightmap[y+1][x] != "9":
            basin = basin.union(find_basin((x, y+1), heightmap))
    if x > 0:
        if heightmap[y][x] < heightmap[y][x-1] and heightmap[y][x-1] != "9":
            basin = basin.union(find_basin((x-1, y), heightmap))
    if x < X-1:
        if heightmap[y][x] < heightmap[y][x+1] and heightmap[y][x+1] != "9":
            basin = basin.union(find_basin((x+1, y), heightmap))
    return basin

def color_basin(basin, heightmap):
    colored_map = []
    X = len(heightmap[0])
    Y = len(heightmap)
    for y in range(Y):
        colored_line = ""
        for x in range(X):
            if (x, y) in basin:
                colored_line += color["RED"] + heightmap[y][x] + color["END"]
            else:
                colored_line += heightmap[y][x]
        colored_map.append(colored_line)
    return colored_map


def test():
    heightmap = parse_input("test9.txt")
    low_points = find_low_points(heightmap)
    counter = 0
    for point in low_points:
        counter += risk_level(point, heightmap)
        basin = find_basin(point, heightmap)
        colored_map = color_basin(basin, heightmap)
        for line in colored_map:
            print(line)
        print("\n")
    print(counter)

def prob9a():
    heightmap = parse_input("input9.txt")
    low_points = find_low_points(heightmap)
    counter = 0
    for point in low_points:
        counter += risk_level(point, heightmap)
    print(counter)

def prob9b():
    heightmap = parse_input("input9.txt")
    low_points = find_low_points(heightmap)
    basin_sizes = []
    for point in low_points:
        basin = find_basin(point, heightmap)
        basin_sizes.append(len(basin))
    basin_sizes.sort(reverse=True)
    print(basin_sizes)
    print(basin_sizes[0]*basin_sizes[1]*basin_sizes[2])
    colored_map = color_nines(heightmap)
    for line in colored_map:
        print(line)


test()
prob9a()
prob9b()
