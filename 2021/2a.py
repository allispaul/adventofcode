# Read input
INPUT = "input2a.txt"
commands = open(INPUT, "r").read().split("\n")[:-1] # remove trailing empty string

# initial position (0, 0)
x = 0
depth = 0

# execute commands
for order in commands:
    dir, num = order.split()
    num = int(num)
    if dir == "down":
        depth = depth + num
    elif dir == "up":
        depth = depth - num
    elif dir == "forward":
        x = x + num
    else:
        raise ValueError("I don't recognize the command", order)

    print("Ran command '", order, "'. Now at x =", x, " depth =", depth)

print("x * depth =", x * depth)
