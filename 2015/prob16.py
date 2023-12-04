def find_sue(info, sues):
    for sue in sues:
        for key in sue.keys():
            if key == "index":
                continue
            elif key == "cats" or key == "trees":
                if sue[key] <= info[key]:
                    break
            elif key == "pomeranians" or key == "goldfish":
                if sue[key] >= info[key]:
                    break
            else:
                if info[key] != sue[key]:
                    break
        else:
            return sue


def parse_sue(line):
    words = line.split()
    sue = dict()
    sue["index"] = int(words[1][:-1])
    for i in range(3):
        count = words[2*i+3]
        if count[-1] == ",":
            count = count[:-1]
        sue[words[2*i+2][:-1]] = int(count)
    return sue


def prob16a():
    lines = open("input16.txt", 'r').read().split("\n")[:-1]
    sues = [parse_sue(line) for line in lines]
    info = {"children": 3,
            "cats": 7,
            "samoyeds": 2,
            "pomeranians": 3,
            "akitas": 0,
            "vizslas": 0,
            "goldfish": 5,
            "trees": 3,
            "cars": 2,
            "perfumes": 1}
    print(find_sue(info, sues))

if __name__ == "__main__":
    prob16a()
