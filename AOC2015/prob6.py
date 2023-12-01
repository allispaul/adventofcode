def prob6a(instructions):
    lights = [[False for _ in range(1000)] for _ in range(1000)]
    for inst in instructions:
        words = inst.split()
        if words[0] == "turn":
            corner1 = [int(x) for x in words[2].split(',')]
            corner2 = [int(x) for x in words[4].split(',')]
            if words[1] == "on":
                for x in range(corner1[0], corner2[0]+1):
                    for y in range(corner1[1], corner2[1]+1):
                        lights[x][y] = True
            elif words[1] == "off":
                for x in range(corner1[0], corner2[0]+1):
                    for y in range(corner1[1], corner2[1]+1):
                        lights[x][y] = False
            else:
                raise ValueError(f"Unrecognized instruction {inst}")
        elif words[0] == "toggle":
            corner1 = [int(x) for x in words[1].split(',')]
            corner2 = [int(x) for x in words[3].split(',')]
            for x in range(corner1[0], corner2[0]+1):
                for y in range(corner1[1], corner2[1]+1):
                    lights[x][y] = not lights[x][y]
    lights_on = 0
    for col in lights:
        lights_on += sum(col)
    return lights_on


def prob6b(instructions):
    lights = [[0 for _ in range(1000)] for _ in range(1000)]
    for inst in instructions:
        words = inst.split()
        if words[0] == "turn":
            corner1 = [int(x) for x in words[2].split(',')]
            corner2 = [int(x) for x in words[4].split(',')]
            if words[1] == "on":
                for x in range(corner1[0], corner2[0]+1):
                    for y in range(corner1[1], corner2[1]+1):
                        lights[x][y] += 1
            elif words[1] == "off":
                for x in range(corner1[0], corner2[0]+1):
                    for y in range(corner1[1], corner2[1]+1):
                        lights[x][y] = max(lights[x][y]-1, 0)
            else:
                raise ValueError(f"Unrecognized instruction {inst}")
        elif words[0] == "toggle":
            corner1 = [int(x) for x in words[1].split(',')]
            corner2 = [int(x) for x in words[3].split(',')]
            for x in range(corner1[0], corner2[0]+1):
                for y in range(corner1[1], corner2[1]+1):
                    lights[x][y] += 2
    lights_on = 0
    for col in lights:
        lights_on += sum(col)
    return lights_on


if __name__ == "__main__":
    assert prob6a(["turn on 0,0 through 999,999"]) == 1000*1000
    assert prob6a(["toggle 0,0 through 999,0"]) == 1000
    assert prob6a(["turn on 0,0 through 999,999",
                   "turn off 499,499 through 500,500"]) == 1000*1000 - 4
    assert prob6b(["turn on 0,0 through 0,0"]) == 1
    assert prob6b(["toggle 0,0 through 999,999"]) == 2*1000*1000
    instructions = open("input6.txt", 'r').read().split("\n")[:-1]
    print(prob6b(instructions))
