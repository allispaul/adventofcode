def parse_input(filename):
    return open(filename).read().split("\n")[:-1]

def strip_matches(string):
    old_string = string
    while True:
        new_string = old_string.replace("()", "")
        new_string = new_string.replace("[]", "")
        new_string = new_string.replace("{}", "")
        new_string = new_string.replace("<>", "")
        if new_string == old_string:
            return new_string
        old_string = new_string

def syntax_score(stripped_line):
    for char in stripped_line:
        if char == ")":
            return 3
        elif char == "]":
            return 57
        elif char == "}":
            return 1197
        elif char == ">":
            return 25137
    return 0

def autocomplete_score(stripped_line):
    score = 0
    for char in reversed(stripped_line):
        if char == "(":
            score = score*5 + 1
        elif char == "[":
            score = score*5 + 2
        elif char == "{":
            score = score*5 + 3
        elif char == "<":
            score = score*5 + 4
    return score

def test():
    lines = parse_input("test10.txt")
    auto_scores = []
    for line in lines:
        stripped = strip_matches(line)
        score = syntax_score(stripped)
        if score == 0:
            print(f"{line} -> {stripped}: {autocomplete_score(stripped)}")
            auto_scores.append(autocomplete_score(stripped))
    auto_scores.sort()
    print(auto_scores)
    print(auto_scores[(len(auto_scores)-1)//2])

def prob10a():
    lines = parse_input("input10.txt")
    total_score = 0
    for line in lines:
        stripped = strip_matches(line)
        total_score += syntax_score(stripped)
    print(total_score)

def prob10b():
    lines = parse_input("input10.txt")
    auto_scores = []
    for line in lines:
        stripped = strip_matches(line)
        score = syntax_score(stripped)
        if score == 0:
            auto_scores.append(autocomplete_score(stripped))
    auto_scores.sort()
    print(auto_scores[(len(auto_scores)-1)//2])


test()
prob10a()
prob10b()
