from collections import defaultdict

test = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

def prob4a(text):
    return sum(
            2**len(
                {int(x) for x in line.split("|")[0].split()[2:]} &
                {int(x) for x in line.split("|")[1].split()}
                ) // 2
            for line in text.split("\n"))

def prob4b(text):
    lines = text.split("\n")
    copies = defaultdict(lambda: 1)
    total = 0
    for i, line in enumerate(lines):
        score = len(
                {int(x) for x in line.split("|")[0].split()[2:]} &
                {int(x) for x in line.split("|")[1].split()}
                )
        for j in range(i+1, i+1+score):
            copies[j] += copies[i]
        total += copies[i]
    return total


if __name__ == "__main__":
    print(prob4a(test))
    print(prob4a(open("input4", "r").read()[:-1]))
    print(prob4b(test))
    print(prob4b(open("input4", "r").read()[:-1]))
