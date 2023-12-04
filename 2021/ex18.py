import re

# def flattened(l):
#     for x in l:
#         print(f"Looking at {x}")
#         if type(x) is list:
#             print(f"{x} is a list")
#             yield next(flattened(x))
#         else:
#             print(f"{x} is not a list")
#             yield x

def nums_in(string):
    return [match for match in re.finditer(r"\d+", string)]

def nesting_depth(string, pos):
    return string.count("[", 0, pos) - string.count("]", 0, pos)

def reduction_step(sn):
    nums = nums_in(sn)
    # Check for explodes
    for index, match in enumerate(nums):
        if nesting_depth(sn, match.start()) >= 5:
            if index > 0:
                prev = nums[index-1]
                temp = (sn[:prev.start()] + str(int(prev.group(0)) + int(match.group(0))) +
                        sn[prev.end():match.start()-1])
            else:
                temp = sn[:match.start()-1]
            temp += "0"
            nxt = nums[index+1]
            if index < len(nums) - 2:
                nxtnxt = nums[index+2]
                temp += (sn[nxt.end()+1:nxtnxt.start()] +
                         str(int(nxt.group(0)) + int(nxtnxt.group(0))) +
                         sn[nxtnxt.end():])
            else:
                temp += sn[nxt.end()+1:]
            # print(f"Explode at [{match.group(0)},{nxt.group(0)}] to get {temp}")
            sn = temp
            return sn
    # Check for splits
    for match in nums:
        num = int(match.group(0))
        if num >= 10:
            sn = f"{sn[:match.start()]}[{num//2},{num - num//2}]{sn[match.end():]}"
            # print(f"Split at {match.group(0)} to get {sn}")
            return sn
    # print("Nothing to reduce")
    return sn

def reduce(sn):
    sn_new = reduction_step(sn)
    while sn_new != sn:
        # print("Reducing again...")
        sn = sn_new
        sn_new = reduction_step(sn)
    return sn_new

def add(sn1, sn2):
    # print(f"Adding {sn1}, {sn2}")
    return reduce(f"[{sn1},{sn2}]")

def add_list(list_of_sns):
    # print(f"Starting with {list_of_sns[0]}...")
    sn = reduce(list_of_sns[0])
    for next_sn in list_of_sns[1:]:
        sn = add(sn, next_sn)
    return sn

def magnitude_of_pair(match):
    return str(3*int(match.group(1)) + 2*int(match.group(2)))

def magnitude(sn):
    while not sn.isnumeric():
        sn = re.sub(r"\[(\d+),(\d+)\]", magnitude_of_pair, sn)
        # print(f"Replaced with {sn}")
    return int(sn)

def max_mag_of_pair_sum(list_of_sns):
    return max(magnitude(add(sni, snj)) for sni in list_of_sns for snj in list_of_sns)

def test():
    assert magnitude("[[1,2],[[3,4],5]]") == 143
    assert magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
    assert magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]") == 445
    assert magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]") == 791
    assert magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]") == 1137
    assert magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]") == 3488

    test_list = open("test18.txt","r").read().split("\n")[:-1]
    assert add_list(test_list) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
    assert magnitude(add_list(test_list)) == 4140

    test_list_b = open("test18b.txt", "r").read().split("\n")[:-1]
    assert max_mag_of_pair_sum(test_list_b) == 3993


def prob18a():
    problem_list = open("input18.txt", "r").read().split("\n")[:-1]
    return magnitude(add_list(problem_list))

def prob18b():
    problem_list = open("input18.txt", "r").read().split("\n")[:-1]
    return max_mag_of_pair_sum(problem_list)



