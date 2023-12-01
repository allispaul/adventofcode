def visit_houses(route):
    houses_visited = {(0,0)}
    pos = (0,0)
    for char in route:
        if char == "^":
            pos = (pos[0], pos[1]-1)
        elif char == ">":
            pos = (pos[0]+1, pos[1])
        elif char == "v":
            pos = (pos[0], pos[1]+1)
        elif char == "<":
            pos = (pos[0]-1, pos[1])
        elif char == "\n":
            continue
        else:
            raise ValueError(f"Unrecognized character {char}")
        houses_visited.add(pos)
    return(houses_visited)


if __name__ == "__main__":
    assert len(visit_houses(">")) == 2
    assert len(visit_houses("^>v<")) == 4
    assert len(visit_houses("^v^v^v^v^v")) == 2
    route = open("input3.txt", 'r').read()
    print(len(visit_houses(route)))
    bio_houses = visit_houses(route[0::2])
    robo_houses = visit_houses(route[1::2])
    print(len(bio_houses | robo_houses))


