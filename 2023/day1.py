import re
def first_digit(s):
    return int(re.search(r"(\d)", s).groups()[0])

def last_digit(s):
    return int(re.search(r"(\d)", s[::-1]).groups()[0])

numerizer = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
             '6': 6, '7': 7, '8': 8, '9': 9,
             'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
             'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

def first_digit_b(s):
    match = re.search(
            r"(\d|one|two|three|four|five|six|seven|eight|nine)", s
    ).groups()[0]
    return numerizer[match]

def last_digit_b(s):
    match = re.search(
            r"(\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)", s[::-1]
    ).groups()[0]
    return numerizer[match[::-1]]

def prob1a(text):
    sum = 0
    for line in text.split('\n'):
        sum += 10*first_digit(line)
        sum += last_digit(line)
    return sum

def prob1b(text):
    sum = 0
    for line in text.split('\n'):
        sum += 10*first_digit_b(line)
        sum += last_digit_b(line)
    return sum

test = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

testb = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

if __name__ == "__main__":
    print(prob1a(test))
    print(prob1a(open("input1", "r").read()[:-1]))
    print(prob1b(testb))
    print(prob1b(open("input1", "r").read()[:-1]))
