def is_nice(string):
    if "ab" in string or "cd" in string or "pq" in string or "xy" in string:
        return False
    double = False
    vowels = 0
    for n in range(len(string)):
        if n < len(string)-1 and string[n] == string[n+1]:
            double = True
        if string[n] in "aeiou":
            vowels += 1
    return (double and (vowels >= 3))


def new_nice(string):
    sandwich = False
    repeat = False
    for i in range(len(string)-2):
        if string[i] == string[i+2]:
            sandwich = True
        for j in range(i+2, len(string)):
            if string[i:i+2] == string[j:j+2]:
                repeat = True
    return sandwich and repeat


def prob5a():
    assert is_nice("ugknbfddgicrmop")
    assert is_nice("aaa")
    assert not is_nice("jchzalrnumimnmhp")
    assert not is_nice("haegwjzuvuyypxyu")
    assert not is_nice("dvszwmarrgswjxmb")
    nice_count = 0
    for string in open("input5.txt", "r").read().split("\n")[:-1]:
        if is_nice(string):
            nice_count += 1
    print(nice_count)


def prob5b():
    assert new_nice("qjhvhtzxzqqjkmpb")
    assert new_nice("xxyxx")
    assert not new_nice("uurcxstgmygtbstg")
    assert not new_nice("ieodomkazucvgmuy")
    nice_count = 0
    for string in open("input5.txt", "r").read().split("\n")[:-1]:
        if new_nice(string):
            nice_count += 1
    print(nice_count)


if __name__ == "__main__":
    prob5b()
