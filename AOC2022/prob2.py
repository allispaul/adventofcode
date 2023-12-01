# "One-liners"
# Anything we care about is a linear function on Z/3
def score_a(games):
    return sum((ord(g.split()[1]) - 87)                                 # for move choice
               + ((ord(g.split()[1]) - ord(g.split()[0]) - 1) % 3 * 3)  # for win/loss/draw
               for g in games)


def score_b(games):
    return sum(((ord(g.split()[1])-1) % 3 * 3)                          # for win/loss/draw
               + ((ord(g.split()[0]) + ord(g.split()[1]) - 1) % 3 + 1)  # for move choice
               for g in games)



if __name__ == "__main__":
    test = ["A Y", "B X", "C Z"]
    # test A
    assert score_a(test) == 15
    # part A
    print(score_a(open('input2.txt', 'r')))
    # test B
    assert score_b(test) == 12
    # part B
    print(score_b(open('input2.txt', 'r')))

