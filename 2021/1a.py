INPUT = "input1a.txt"
depths = open(INPUT, "r").read().split("\n")[:-1]
depths = [int(d) for d in depths]
drops = 0

for i in range(1,len(depths)):
    drops = drops + (depths[i] > depths[i-1])

print(drops)
