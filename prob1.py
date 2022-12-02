def best_calories(file):
    best = current_total = 0
    for line in file:
        if line == "\n":
            if current_total > best:
                best = current_total
            current_total = 0
        else:
            current_total += int(line)
    return best


def three_best_calories(file):
    current_total = 0
    calories_list = [0, 0, 0]
    for line in file:
        if line == "\n":
            for val in calories_list:
                if current_total > val:
                    calories_list.append(current_total)
                    calories_list.sort()
                    calories_list = calories_list[1:]
                    break
            current_total = 0
        else:
            current_total += int(line)
    return calories_list


if __name__ == "__main__":
    print(best_calories(open("test1.txt", "r")))
    print(best_calories(open("input1.txt", "r")))
    print(three_best_calories(open("test1.txt", "r")))
    print(three_best_calories(open("input1.txt", "r")))
    cals = three_best_calories(open("input1.txt", "r"))
    print(sum(cals))
