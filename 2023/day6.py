def ways_to_beat(time, distance):
    # Hold button for t ms: travel t*(T-t) mm, where T = max time
    # By symmetry, if the minimum time you can beat the record is t0, 
    # the max time is T-t0. The number of ways to beat the record is T-2*t0+1.
    for t0 in range(time//2):
        if t0*(time-t0) > distance:
            return time - 2*t0 + 1
    return 0

def parse_races(text):
    lines = text.split("\n")
    times = map(int, lines[0].split()[1:])
    dists = map(int, lines[1].split()[1:])
    return zip(times, dists)

def prob6a(text):
    total = 1
    for time, distance in parse_races(text):
        total *= ways_to_beat(time, distance)
    return total

def parse_races_b(text):
    lines = text.split("\n")
    time = int("".join(lines[0].split()[1:]))
    dist = int("".join(lines[1].split()[1:]))
    return time, dist

def prob6b(text):
    return ways_to_beat(*parse_races_b(text))

if __name__ == "__main__":
    test = """Time:      7  15   30
Distance:  9  40  200"""
    print(prob6a(test))
    print(prob6a(open("input6", "r").read()[:-1]))
    print(prob6b(test))
    print(prob6b(open("input6", "r").read()[:-1]))
