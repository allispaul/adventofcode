def count_floors(filename):
    string = open(filename).read()
    return string.count("(") - string.count(")")

def first_negative_char(filename):
    string = open(filename).read()
    counter = 0
    for n, char in enumerate(string):
        if char == "(":
            counter += 1
        if char == ")":
            counter -= 1
        if counter < 0:
            return n+1


print(count_floors("input1.txt"))
print(first_negative_char("test1.txt"))
print(first_negative_char("input1.txt"))
