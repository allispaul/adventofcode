INPUT = "input1a.txt"
depths = open(INPUT, "r").read().split("\n")[:-1]
depths = [int(d) for d in depths]
moving_sums = [depths[i] + depths[i+1] + depths[i+2]
               for i in range(len(depths)-2)]
drops = 0

for i in range(1,len(moving_sums)):
    drops = drops + (moving_sums[i] > moving_sums[i-1])

print(drops)
