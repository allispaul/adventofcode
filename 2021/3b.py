# Read input
INPUT = "input3.txt"
diagnostic = open(INPUT, "r").read().split("\n")[:-1] # remove trailing empty string

# all entries in diagnostic should be strings of 1s and 0s of the same length
entry_length = len(diagnostic[0])

# initially, all diagnostic entries are possible oxygen generator
# and CO2 scrubber ratings
O2_choices = diagnostic
CO2_choices = diagnostic

# find oxygen generator rating
for pos in range(entry_length):
    # find most common bit at pos
    bits_at_pos = [entry[pos] for entry in O2_choices]
    num_zeroes = bits_at_pos.count("0")
    num_ones = bits_at_pos.count("1")
    # filter O2_choices to those with the most common bit at pos
    # or 1 at pos, if both bits are equally common
    O2_choices = [entry for entry in O2_choices
                  if int(entry[pos]) == (num_ones >= num_zeroes)]
    # if there's a single choice left, save it and exit the loop
    if len(O2_choices) == 1:
        O2_generator_rating = int(O2_choices[0], 2)
        break

# find CO2 generator rating
for pos in range(entry_length):
    # find most common bit at pos
    bits_at_pos = [entry[pos] for entry in CO2_choices]
    num_zeroes = bits_at_pos.count("0")
    num_ones = bits_at_pos.count("1")
    # filter CO2_choices to those with the least common bit at pos
    # or 0 at pos, if both bits are equally common
    CO2_choices = [entry for entry in CO2_choices
                  if int(entry[pos]) == (num_ones < num_zeroes)]
    # if there's a single choice left, save it and exit the loop
    if len(CO2_choices) == 1:
        CO2_scrubber_rating = int(CO2_choices[0], 2)
        break

print("Oxygen generator rating:", O2_generator_rating)
print("CO2 scrubber rating:", CO2_scrubber_rating)
print("Life support rating:", O2_generator_rating * CO2_scrubber_rating)
