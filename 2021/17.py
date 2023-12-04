import math

xmin, xmax = 211, 232
ymin, ymax = -124, -69
# xmin, xmax = 20, 30
# ymin, ymax = -10, -5
assert ymax < 0 # Out of laziness

# Part A
# Find biggest y velocity that lands in target area
# If launched with y velocity vy > 0, then when the probe crosses y = 0 on the
# way down, its next y coordinate will be -(vy + 1)
# Thus, the greatest velocity landing in the target area is vy = -ymin - 1

vy = -ymin - 1

# Find maximum height reached by this velocity
ypeak = vy*(vy + 1) // 2
print(f"Maximum y velocity: {vy}, maximum height reached: {ypeak}")

# Part B
# Find all velocities that land in the target area
velocities = []
# First iterate through all y velocities
for vy in range(ymin, -ymin):
    step = 0
    y = 0
    while y > ymin:
        y += (vy - step)
        step += 1
        if ymin <= y and y <= ymax:
            # Iterate through all x velocities
            for vx in range(1, xmax+1):
                if step <= vx:
                    x = (step*(1-step) // 2) + step*vx
                else:
                    x = vx*(vx+1) // 2
                if x <= 0:
                    raise ValueError(f"{x=}, {y=}, {vx=}, {vy=}, {step=}")
                if xmin <= x and x <= xmax:
                    velocities.append((vx, vy))
print(len(set(velocities)))
# print(velocities)

# their_results = open("test17.txt", 'r').read().split()
# their_velocities = [(int(v.split(',')[0]), int(v.split(',')[1]))
#                     for v in their_results]
# print(len(their_velocities))
# print(set(velocities) - set(their_velocities))
# print(set(their_velocities) - set(velocities))

