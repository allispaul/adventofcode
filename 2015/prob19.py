import re
import time


def find_replacements(input, rules):
    replacements = set()
    for rule in rules:
        reactant, product = rule.split()[0], rule.split()[2]
        for match in re.finditer(reactant, input):
            replacement = input[:match.start()] + product + input[match.end():]
            replacements.add(replacement)
    return replacements


def count_replacements(input, rules):
    return len(find_replacements(input, rules))


def reverse_replacements(input, rules):
    replacements = set()
    for rule in rules:
        reactant, product = rule.split()[0], rule.split()[2]
        for match in re.finditer(product, input):
            replacement = input[:match.start()] + reactant + input[match.end():]
            replacements.add(replacement)
    return replacements


# All rules weakly increase length.
# Thus, we can throw out any nodes which are at least as long as the goal.
def shortest_path(goal, rules, start="e"):
    distances = {goal: 0}
    to_explore = [goal]
    print(goal, len(goal))
    input("Press ENTER when ready: ")
    while start not in distances:
        node = to_explore.pop()
        replacements = reverse_replacements(node, rules)
        for next_node in replacements:
            if next_node not in distances or distances[next_node] > distances[node]+1:
                distances[next_node] = distances[node]+1
                if len(next_node) < len(goal):
                    to_explore.append(next_node)
        to_explore.sort(key=len, reverse=True)
        print(len(to_explore), len(to_explore[-1]))
    return distances[start]


def prob19a():
    lines = open("input19.txt").read().split("\n")[:-1]

    input = lines[-1]
    rules = lines[:-2]
    print(count_replacements(input, rules))


def test():
    rules = ["H => HO", "H => OH", "O => HH"]
    input = "HOHOHO"
    print(count_replacements(input, rules))


def testb():
    rules = ["H => HO", "H => OH", "O => HH", "e => H", "e => O"]
    print(shortest_path("HOHOHO", rules))


def prob19b():
    lines = open("input19.txt").read().split("\n")[:-1]

    goal = lines[-1]
    rules = lines[:-2]
    tic = time.perf_counter()
    dist = shortest_path(goal, rules)
    toc = time.perf_counter()
    print(dist)
    print(f"Finished in {toc-tic:.04}s.")


if __name__ == "__main__":
    test()
    prob19a()
    testb()
    prob19b()
