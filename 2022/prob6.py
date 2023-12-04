def n_distinct_chars(string, n):
    for i in range(len(string)):
        if len(set(string[i:i+n])) == n:
            return i+n


def test():
    assert n_distinct_chars("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
    assert n_distinct_chars("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert n_distinct_chars("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert n_distinct_chars("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert n_distinct_chars("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11

    assert n_distinct_chars("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert n_distinct_chars("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert n_distinct_chars("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert n_distinct_chars("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert n_distinct_chars("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26

if __name__ == "__main__":
    test()
    string = open("input6.txt", "r").read()
    print(n_distinct_chars(string, 4))
    print(n_distinct_chars(string, 14))
