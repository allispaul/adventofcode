import itertools
import time

def parse_distances(filename):
    lines = open(filename, 'r').read().split("\n")[:-1]
    distances = dict()
    cities = set()
    for line in lines:
        words = line.split()
        city1 = words[0]
        city2 = words[2]
        distance = int(words[4])
        distances[(city1, city2)] = distance
        distances[(city2, city1)] = distance
        cities.add(city1)
        cities.add(city2)
    return cities, distances


def brute_force(cities, distances):
    best_path = []
    min_dist = sum(distances.values())
    for path in itertools.permutations(cities):
        total_dist = 0
        for i in range(len(path)-1):
            total_dist += distances[(path[i], path[i+1])]
        if total_dist < min_dist:
            best_path = path
            min_dist = total_dist
    return min_dist, best_path

def brute_force_max(cities, distances):
    best_path = []
    max_dist = 0
    for path in itertools.permutations(cities):
        total_dist = 0
        for i in range(len(path)-1):
            total_dist += distances[(path[i], path[i+1])]
        if total_dist > max_dist:
            best_path = path
            max_dist = total_dist
    return max_dist, best_path

if __name__ == "__main__":
    # cities, distances = parse_distances("test9.txt")
    # # print(cities)
    # # print(distances)
    # tick = time.perf_counter()
    # best = brute_force(cities, distances)
    # tock = time.perf_counter()
    # print(f"Found {best} in {tock-tick:.6}s.")

    cities, distances = parse_distances("input9.txt")
    tick = time.perf_counter()
    best = brute_force(cities, distances)
    tock = time.perf_counter()
    print(f"Found {best} in {tock-tick:.6}s.")

    cities, distances = parse_distances("input9.txt")
    tick = time.perf_counter()
    best = brute_force_max(cities, distances)
    tock = time.perf_counter()
    print(f"Found {best} in {tock-tick:.6}s.")

