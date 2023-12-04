def increment(string):
    if string[-1] == "z":
        return increment(string[:-1]) + "a"
    return string[:-1] + chr(ord(string[-1])+1)

def validate(string):
    assert len(string) == 8
    if "i" in string or "o" in string or "l" in string:
        return False
    doubles = 0
    straight = False
    for i in range(len(string)-2):
        if string[i] == string[i+1]:
            doubles += 1
            # don't count triples twice
            if string[i+1] == string[i+2]:
                doubles -= 1
        if ord(string[i])+1 == ord(string[i+1]) and ord(string[i])+2 == ord(string[i+2]):
            straight = True
    # check last pair
    if string[-2] == string[-1]:
        doubles += 1
    return doubles >= 2 and straight

def inc_until_valid(string):
    while not validate(string):
        string = increment(string)
    return string

def main():
    assert increment("xx") == "xy"
    assert increment("yz") == "za"
    assert increment("xzz") == "yaa"
    assert validate("abcdffaa")
    assert validate("ghjaabcc")
    assert not validate("hijklmmn")
    assert not validate("abbceffg")
    assert not validate("abbcegjk")
    print(inc_until_valid("abcdefgh"))
    # print(inc_until_valid("ghijklmn"))
    pwd = inc_until_valid("hxbxwxba")
    print(pwd)
    pwd = inc_until_valid(increment(pwd))
    print(pwd)

if __name__ == "__main__":
    main()
