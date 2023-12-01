# Read input
INPUT = "input2a.txt"
commands = open(INPUT, "r").read().split("\n")[:-1] # remove trailing empty string

# initial position (0, 0)
x = 0
depth = 0
# initial aim 0
aim = 0

# execute commands
for order in commands:
    dir, num = order.split()
    num = int(num)
    if dir == "down":
        aim = aim + num
    elif dir == "up":
        aim = aim - num
    elif dir == "forward":
        x = x + num
        depth = depth + (aim * num)
    else:
        raise ValueError("I don't recognize the command", order)

    print("Ran command '", order, "'. Now at x =", x, "depth =", depth, "aim =", aim)

print("x * depth =", x * depth)
