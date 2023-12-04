def parse_input(filename):
    return [int(_) for _ in open(filename).read().split(",")]

def compile_timers(school):
    timers = [0]*9
    for fish in school:
        timers[fish] += 1
    return timers

def run_timers(init_timers, num_days):
    timers = init_timers
    for day in range(num_days):
        new_timers = []
        for pos in range(8):
            new_timers.append(timers[pos+1])
        new_timers.append(timers[0])
        new_timers[6] += timers[0]
        timers = new_timers
    return timers

def test():
    init_school = parse_input("test6.txt")
    timers = compile_timers(init_school)
    print(sum(run_timers(timers, 256)))

def prob6():
    init_school = parse_input("input6.txt")
    timers = compile_timers(init_school)
    print(sum(run_timers(timers, 80)))
    print(sum(run_timers(timers, 256)))

prob6()
