import string

test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".split("\n")

def priority(item):
    if item in string.ascii_lowercase:
        return ord(item) - 96  # a -> 1, ...
    elif item in string.ascii_uppercase:
        return ord(item) - 38  # A -> 27, ...
    else:
        raise ValueError(f"Found the common item {item}, which was not a letter.")


def sum_priorities(rucksack_list):
    sum = 0
    for sack in rucksack_list:
        size = len(sack)
        assert size % 2 == 0
        first_half = sack[:size//2]
        second_half = sack[size//2:]
        common_items = set(first_half).intersection(set(second_half))
        # print(sack, first_half, second_half, common_items)
        assert len(common_items) == 1
        sum += priority(next(x for x in common_items))
        # print(sum)
    return sum

def badge_priorities(rucksack_list):
    sum = 0
    for i in range(0, len(rucksack_list), 3):
        common_items = (set(rucksack_list[i]).intersection(set(rucksack_list[i+1])))\
                          .intersection(set(rucksack_list[i+2]))
        assert len(common_items) == 1
        # print(common_items)
        sum += priority(next(x for x in common_items))
    return sum



if __name__ == "__main__":
    assert sum_priorities(test_input) == 157
    real_input = open("input3.txt", 'r').read().split("\n")[:-1]
    print(sum_priorities(real_input))
    assert badge_priorities(test_input) == 70
    print(badge_priorities(real_input))

