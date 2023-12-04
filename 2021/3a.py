# Read input
INPUT = "input3.txt"
diagnostic = open(INPUT, "r").read().split("\n")[:-1] # remove trailing empty string

# all entries in diagnostic should be strings of 1s and 0s of the same length
entry_length = len(diagnostic[0])
num_entries = len(diagnostic)
print(num_entries, "entries of length", entry_length)

# initialize variables
# easiest to treat them as strings
gamma = ""
epsilon = ""

for pos in range(entry_length):
    num_zeroes = [entry[pos] for entry in diagnostic].count("0")
    num_ones = num_entries - num_zeroes
    if num_zeroes == num_ones:
        raise ValueError("Edge case: same number of zeroes as ones at position", pos)
    # Add 1 to gamma and 0 to epsilon if 1 is most common
    # Vice versa if 0 is most common
    gamma = gamma + str(int(num_ones > num_zeroes))
    epsilon = epsilon + str(int(num_zeroes > num_ones))

# Convert gamma and epsilon to integers using base 2
gamma = int(gamma, 2)
epsilon = int(epsilon, 2)
print("gamma =", gamma, "epsilon = ", epsilon)
power_consumption = gamma * epsilon
print("Power consumption:", power_consumption)
