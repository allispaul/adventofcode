def parse_input(filename):
    lines = open(filename).read().split("\n")[:-1]
    allnums = [line.split("|")[0].split() for line in lines]
    ciphertext = [line.split("|")[1].split() for line in lines]
    return (allnums, ciphertext)

# This converts plaintext seven-segment outputs to the numbers they represent.
plain_to_nums = {"CF": 1,
                 "ACDEG": 2,
                 "ACDFG": 3,
                 "BCDF": 4,
                 "ABDFG": 5,
                 "ABDEFG": 6,
                 "ACF": 7,
                 "ABCDEFG": 8,
                 "ABCDFG": 9,
                 "ABCEFG": 0}

def prob8a():
    allnums, ciphertext = parse_input("input8.txt")
    counter = 0
    for line in ciphertext:
        for word in line:
            if len(word) in {2, 3, 4, 7}:
                counter += 1
    print(counter)
    pass

def decode(ciphertext, key):
    """key a dict mapping lowercase cipher letters to uppercase plaintext letters,
    ciphertext a lowercase string. Returns a number."""
    plaintext = ""
    for char in ciphertext:
        plaintext += key[char]
    # sorted returns a list, join back to get a string
    plaintext = "".join(sorted(plaintext))
    return plain_to_nums[plaintext]

def count_appearances(char, list_of_strings):
    """Counts how many of the strings in list_of_strings contain char."""
    counter = 0
    for string in list_of_strings:
        if char in string:
            counter += 1
    return counter

def find_cipher(allnums):
    """Takes a list of 10 ciphered seven-segment digits, returns a dict
    mapping lowercase cipher letters to uppercase plaintext letters.
    """
    key = dict()
    # sort nums by length
    # only lengths 2 through 6 are relevant, but might as well make index match length
    sorted_by_length = [[] for _ in range(7)]
    for num in allnums:
        if len(num) == 7:
            continue
        sorted_by_length[len(num)].append(num)
    for char in "abcdefg":
        count_vector = [count_appearances(char, sorted_by_length[_])
                        for _ in range(7)]
        if count_vector[2:4] == [0, 1]:
            key[char] = "A"
        elif count_vector[5:] == [3, 3]:
            key[char] = "G"
        elif count_vector[5:] == [1, 3]:
            key[char] = "B"
        elif count_vector[6] == 3:
            key[char] = "F"
        elif count_vector[2] == 1:
            key[char] = "C"
        elif count_vector[5] == 1:
            key[char] = "E"
        else:
            key[char] = "D"
    return key




def test():
    allnums, ciphertext = parse_input("test8.txt")
    counter = 0
    for line_num, line in enumerate(allnums):
        key = find_cipher(line)
        decoded = [str(decode(word, key)) for word in ciphertext[line_num]]
        answer_num = int(''.join(decoded))
        counter += answer_num
    print(counter)

def prob8b():
    pass
    allnums, ciphertext = parse_input("input8.txt")
    counter = 0
    for line_num, line in enumerate(allnums):
        key = find_cipher(line)
        decoded = [str(decode(word, key)) for word in ciphertext[line_num]]
        answer_num = int(''.join(decoded))
        counter += answer_num
    print(counter)


test()
prob8a()
prob8b()

