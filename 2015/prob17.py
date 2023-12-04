from itertools import chain, combinations

def find_all_combos(jars, vol):
    count = 0
    for r in range(1, len(jars)+1):
        for subset in combinations(jars, r):
            if sum(x for x in subset) == vol:
                print(subset)
                count += 1
    return count

jars = [33, 14, 18, 20, 45, 35, 16, 35, 1, 13, 18, 13, 50, 44, 48, 6, 24, 41, 30, 42]


if __name__ == "__main__":
    print(find_all_combos([20, 15, 10, 5, 5], 25))
    print("")
    print(find_all_combos(jars, 150))
