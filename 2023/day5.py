test = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

def prob5a(text):
    blocks = text.split("\n\n")
    seeds = [int(x) for x in blocks[0].split()[1:]]
    for block in blocks[1:]:
        for i in range(len(seeds)):
            for line in block.split("\n")[1:]:
                dest_start, source_start, length = (int(x) for x in line.split())
                if seeds[i] >= source_start and seeds[i] - source_start < length:
                    seeds[i] = dest_start + seeds[i] - source_start
                    break
    return min(seeds)

def prob5b(text):
    # too much work to track individual seeds. instead work with ranges
    blocks = text.split("\n\n")
    seeds = [int(x) for x in blocks[0].split()[1:]]
    seeds = [[seeds[2*i], seeds[2*i+1]] for i in range(len(seeds)//2)]
    for block in blocks[1:]:
        next_seeds = []
        for seed_start, seed_length in seeds:
            for line in block.split("\n")[1:]:
                dest_start, source_start, source_length = (int(x) for x in line.split())
                # case 1: whole seed range contained in map range
                if (seed_start >= source_start
                    and seed_start + seed_length <= source_start + source_length):
                    next_seeds.append([dest_start + seed_start - source_start,
                                       seed_length])
                    break  # done with this seed
                # case 2: seed range ends but doesn't begin in map range
                elif (seed_start + seed_length >= source_start + 1 and seed_start + seed_length <= source_start + source_length):
                    next_seeds.append([dest_start, seed_start + seed_length - source_start])
                    # mutate the seed and continue
                    seed_length = source_start - seed_start
                # case 3: seed range begins but doesn't end in map range
                elif seed_start >= source_start and seed_start < source_start + source_length:
                    next_seeds.append([dest_start + seed_start - source_start,
                                       source_start + source_length - seed_start])
                    # mutate the seed and continue
                    seed_length = seed_start + seed_length - (source_start + source_length)
                    seed_start = source_start + source_length
            else:
                # case 4: exited the for loop normally (part of seed range not mapped)
                # retain the remainder of the seed range
                next_seeds.append([seed_start, seed_length])
        seeds = next_seeds
    # return minimum of seed start numbers
    return min(seed[0] for seed in seeds)

if __name__ == "__main__":
    print(prob5a(test))
    print(prob5a(open("input5", "r").read()[:-1]))
    print(prob5b(test))
    print(prob5b(open("input5", "r").read()[:-1]))

