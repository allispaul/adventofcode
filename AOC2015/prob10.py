def look_and_say(string):
    assert string.isnumeric()
    output = ""
    current_run = string[0]
    count = 1
    for char in string[1:]:
        if char == current_run:
            count += 1
        else:
            output += str(count) + current_run
            current_run = char
            count = 1
    output += str(count) + current_run
    return output

if __name__ == "__main__":
    string = "1"
    for _ in range(6):
        print(string)
        string = look_and_say(string)
    string = "1113222113"
    for _ in range(50):
        string = look_and_say(string)
    print(len(string))
