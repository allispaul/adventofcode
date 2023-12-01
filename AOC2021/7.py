def parse_input(filename):
    return [int(x) for x in open(filename).read().split(",")]

def fuel_cost(positions, goal, method):
    if method == "a":
        return sum([abs(pos-goal) for pos in positions])
    elif method == "b":
        costs = []
        for pos in positions:
            distance = abs(pos-goal)
            costs.append((distance*(distance+1))/2)
        return sum(costs)

def min_cost(positions, method):
    costs = [fuel_cost(positions, goal, method) for goal in range(max(positions)+1)]
    return min(costs)

def cheapest_goal(positions, method):
    costs = [fuel_cost(positions, goal, method) for goal in range(max(positions)+1)]
    return [goal for goal, cost in enumerate(costs)
            if cost == min_cost(positions, method)]

def test():
    positions = parse_input("test7.txt")
    print(fuel_cost(positions, 5, "b"))
    print(cheapest_goal(positions, "a"), min_cost(positions, "a"))
    print(cheapest_goal(positions, "b"), min_cost(positions, "b"))

def prob7a():
    positions = parse_input("input7.txt")
    print(min_cost(positions, "a"))

def prob7b():
    positions = parse_input("input7.txt")
    print(min_cost(positions, "b"))

prob7b()
