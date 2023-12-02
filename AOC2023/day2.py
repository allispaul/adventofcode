import re
test = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

def part1(text):
    total = 0
    for i, line in enumerate(text.split("\n")):
        blue = map(int, re.findall(r"\d+(?= blue)", line))
        green = map(int, re.findall(r"\d+(?= green)", line))
        red = map(int, re.findall(r"\d+(?= red)", line))
        if (all(x <= 12 for x in red)
            and all(x <= 13 for x in green)
            and all(x <= 14 for x in blue)):
            total += i+1
    return total

def part2(text):
    total = 0
    for line in text.split("\n"):
        blue = map(int, re.findall(r"\d+(?= blue)", line))
        green = map(int, re.findall(r"\d+(?= green)", line))
        red = map(int, re.findall(r"\d+(?= red)", line))
        power = max(blue) * max(green) * max(red)
        total += power
    return total


if __name__ == "__main__":
    print(part1(test))
    print(part1(open("input2", "r").read()[:-1]))
    print(part2(test))
    print(part2(open("input2", "r").read()[:-1]))


