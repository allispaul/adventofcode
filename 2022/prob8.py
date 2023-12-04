def generate_array(filename):
    array = []
    for line in open(filename, 'r'):
        array.append([int(x) for x in line[:-1]])
    return array


def visible_trees(array):
    # We just have to count the trees visible in each direction
    # that we can look in from the outside
    xmax = len(array[0])
    ymax = len(array)
    visible = set()
    for x in range(xmax):
        # Looking from top
        highest = -1
        for y in range(ymax):
            if array[x][y] > highest:
                visible.add((x, y))
                highest = array[x][y]
        # Looking from bottom
        highest = -1
        for y in range(ymax-1, -1, -1):
            if array[x][y] > highest:
                visible.add((x, y))
                highest = array[x][y]
    for y in range(ymax):
        # Looking from left
        highest = -1
        for x in range(xmax):
            if array[x][y] > highest:
                visible.add((x, y))
                highest = array[x][y]
        # Looking from right
        highest = -1
        for x in range(xmax-1, -1, -1):
            if array[x][y] > highest:
                visible.add((x, y))
                highest = array[x][y]
    return len(visible)


def scenic_score(array, x, y):
    # Trees on the edge have score 0
    xmax = len(array[0])
    ymax = len(array)
    for x0 in range(x-1, -1, -1):
        if array[y][x0] >= array[y][x]:
            left_score = x-x0
            break
    else:
        left_score = x
    for x0 in range(x+1, xmax):
        if array[y][x0] >= array[y][x]:
            right_score = x0-x
            break
    else:
        right_score = xmax-x-1
    for y0 in range(y-1, -1, -1):
        if array[y0][x] >= array[y][x]:
            up_score = y-y0
            break
    else:
        up_score = y
    for y0 in range(y+1, xmax):
        if array[y0][x] >= array[y][x]:
            down_score = y0-y
            break
    else:
        down_score = ymax-y-1
    return left_score * right_score * up_score * down_score


def highest_scenic_score(array):
    highest = 0
    for y in range(len(array)):
        for x in range(len(array[0])):
            score = scenic_score(array, x, y)
            if score > highest:
                highest = score
    return highest


if __name__ == "__main__":
    array1 = generate_array("test8.txt")
    print(visible_trees(array1))
    print(highest_scenic_score(array1))

    array2 = generate_array("input8.txt")
    print(visible_trees(array2))
    print(highest_scenic_score(array2))


