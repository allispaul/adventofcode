import re
import json

total = 0

def sum_nums(input):
    return sum([int(x) for x in re.findall(r"[^-\d](\d+)", input)]) \
        + sum([int(x) for x in re.findall(r"-\d+", input)])

def assemble_ints(x):
    global total
    total += int(x)
    return int(x)

def count_non_reds(data):
    count = 0
    if type(data) is dict:
        for key in data:
            if data[key] == "red":
                return 0
            count += count_non_reds(data[key])
        return count
    elif type(data) is list:
        return sum(count_non_reds(x) for x in data)
    elif type(data) is int:
        return data
    elif type(data) is str:
        return 0
    else:
        raise ValueError(f"Couldn't process {data} of type {type(data)}")


if __name__ == "__main__":
    assert sum_nums("[1,2,3]") == 6
    assert sum_nums('{"a":2,"b":4}') == 6
    assert sum_nums("[[[3]]]") == 3
    assert sum_nums('{"a":{"b":4},"c":-1}') == 3
    assert sum_nums("[]") == 0
    assert sum_nums('{"a":25, "b":[-1,-1]}') == 23
    assert count_non_reds([1,{"c":"red","b":2},3]) == 4
    assert count_non_reds({"d":"red","e":[1,2,3,4],"f":5}) == 0
    assert count_non_reds([1,"red",5]) == 6

    # input = open("input12.txt", 'r').read()
    # print([int(x) for x in re.findall(r"[^-](\d+)", input)])
    # print([int(x) for x in re.findall(r"-\d+", input)])
    # print(sum_nums(input))
    j = json.load(open("input12.txt", 'r'), parse_int=assemble_ints)
    print(total)

    print(count_non_reds(j))
    
    
