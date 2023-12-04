import itertools
import time


def parse(filename):
    lines = open(filename, 'r').read().split("\n")[:-1]
    people = set()
    utils = dict()
    for line in lines:
        words = line.split()
        person1 = words[0]
        person2 = words[-1][:-1] # delete final period
        utility = int(words[3])
        if words[2] == "lose":
            utility = -1*utility
        utils[(person1, person2)] = utility
        people.add(person1)
        people.add(person2)
    return people, utils


def brute_force(people, utils):
    best_path = []
    max_happiness = 0
    for path in itertools.permutations(people):
        total_happiness = 0
        for i in range(len(path)-1):
            total_happiness += utils[(path[i], path[i+1])]
            total_happiness += utils[(path[i+1], path[i])]
        total_happiness += utils[(path[0], path[-1])]
        total_happiness += utils[(path[-1], path[0])]
        if total_happiness > max_happiness:
            best_path = path
            max_happiness = total_happiness
    return max_happiness, best_path


if __name__ == "__main__":
    people, utils = parse("test13.txt")
    print(people)
    tick = time.perf_counter()
    print(brute_force(people, utils))
    tock = time.perf_counter()
    print(f"Finished in {tock-tick:.04}s.")

    people, utils = parse("input13.txt")
    print(people)
    tick = time.perf_counter()
    print(brute_force(people, utils))
    tock = time.perf_counter()
    print(f"Finished in {tock-tick:.04}s.")

    for p in people:
        utils[("Paul", p)] = 0
        utils[(p, "Paul")] = 0
    people.add("Paul")
    print(people)
    tick = time.perf_counter()
    print(brute_force(people, utils))
    tock = time.perf_counter()
    print(f"Finished in {tock-tick:.04}s.")

