import re

# def bonus_chars(strings):
#     count = 0
#     for s in strings:
#         new_chars = (2 + len(re.findall(r'\\\\', s))
#                      + len(re.findall(r'\\"', s))
#                      + 3*len(re.findall(r'\\x', s))
#                      - len(re.findall(r'\\\\\\', s)))
#         if re.findall(r'\\\\\\\\\\', s):
#             raise ValueError("Too many backslashes in", s)
#         print(s, new_chars)
#         count += new_chars
#     return count
def bonus_chars(strings):
    return sum(len(s) - len(eval(s)) for s in strings)

def malus_chars(strings):
    return sum(2 + s.count('\\') + s.count('"') for s in strings)

if __name__ == "__main__":
    strings = open("test8.txt", "r").read().split("\n")[:-1]
    print(bonus_chars(strings))
    print(malus_chars(strings))
    strings = open("input8.txt", "r").read().split("\n")[:-1]
    print(bonus_chars(strings))
    print(malus_chars(strings))
