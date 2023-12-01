def parse_input(filename):
    lines = open(filename, 'r').read().split('\n')[:-1]
    scanners = []
    current_scanner = []
    for line in lines:
        if line.startswith("---"):
            # new scanner
            if len(current_scanner) > 0:
                scanners.append(current_scanner)
            current_scanner = []
        elif len(line) == 0:
            continue
        else:
            coords = tuple(int(x) for x in line.split(","))
            current_scanner.append(coords)
    if len(current_scanner) > 0:
        scanners.append(current_scanner)
    return scanners

def rotate_vector(vector, direction):
    assert len(vector) == 3
    # Direction an int in range(24)
    facing_axis = direction % 3
    vector = tuple(vector[(i + facing_axis) % 3] for i in range(3))
    facing_direction = direction % 2
    if facing_direction:
        vector = (-vector[0], -vector[1], vector[2])
    side_direction = direction // 6
    for _ in range(side_direction):
        vector = (vector[0], vector[2], -vector[1])
    return vector

def rotate_scanner(scanner, direction):
    return [rotate_vector(v, direction) for v in scanner]

def subtract(vec1, vec2):
    return tuple(vec1[i] - vec2[i] for i in range(3))

def add(vec1, vec2):
    return tuple(vec1[i] + vec2[i] for i in range(3))

def translate_scanner(scanner, translation):
    return [add(v, translation) for v in scanner]

def difference_list(scanner):
    return [subtract(b, c) for b in scanner for c in scanner]

def match_scanners(scanner1, scanner2, min_matching_beacons=12):
    diff1, diff2 = difference_list(scanner1), difference_list(scanner2)
    for direction in range(24):
        diff2_rotated = rotate_scanner(diff2, direction)
        if len(set(diff1).intersection(set(diff2_rotated))) < 2*min_matching_beacons+1:
            continue
        scanner2_rotated = rotate_scanner(scanner2, direction)
        for i in scanner1:
            for j in scanner2_rotated:
                translation = subtract(i, j)
                scanner2_translated = [add(beacon, translation) for beacon in scanner2_rotated]
                common_beacons = set(scanner1).intersection(set(scanner2_translated))
                if len(common_beacons) >= min_matching_beacons:
                    # # find a matching beacon and use it to get translation vector
                    # for beacon in common_beacons:
                    #     idx = scanner2_translated.index(beacon)
                    #     beacon_untranslated = scanner2[idx]
                    #     difference_vector = subtract(beacon, beacon_untranslated)
                    return direction, translation #, difference_vector
    return None

def assemble_map(scanners):
    print(f"Total scanners: {len(scanners)}")
    oriented_scanners = [scanners.pop(0)]
    translation_vectors = [(0,0,0)]
    attempts = 0
    while scanners:
        next_s = scanners.pop(0)
        for index, fixed_s in enumerate(oriented_scanners):
            orientation = match_scanners(fixed_s, next_s)
            if orientation:
                reoriented_s = translate_scanner(rotate_scanner(next_s, orientation[0]),
                                                 orientation[1])
                oriented_scanners.append(reoriented_s)
                translation_vectors.append(orientation[1])
                attempts = 0
                break
        else:
            scanners.append(next_s)
            attempts += 1
        print(f"{len(oriented_scanners)} matched, {len(scanners)} left, " +
              f"{attempts} attempts without a match")
        if attempts > 0 and attempts == len(scanners):
            raise Exception("Couldn't assemble the map")
    return oriented_scanners, translation_vectors

def count_beacons(map):
    # Assumes an oriented map
    return len(set([b for s in map for b in s]))

def manhattan_distance(vec1, vec2):
    return sum(abs(x) for x in subtract(vec1, vec2))

def max_manhattan_distance(translation_vectors):
    return max(manhattan_distance(i,j) for i in translation_vectors
               for j in translation_vectors)

def test():
    # test vector rotation
    v = (1, 2, 3)
    rotations = []
    for d in range(24):
        if rotate_vector(v, d) not in rotations:
            rotations.append(rotate_vector(v,d))
    assert len(rotations) == 24

    # test manhattan distance
    assert manhattan_distance((1,2,3),(-2,0,2)) == 6

    # test import
    scanners = parse_input("test19.txt")
    assert len(scanners) == 5

    # test scanner rotation
    s = scanners[0]
    for d in range(24):
        s_rotated = rotate_scanner(s, d)
        assert len(s_rotated) == len(s)

    s1 = [(-1,-1,1), (-2,-2,2), (-3,-3,3), (-2,-3,1), (5,6,-4), (8,0,7)]
    s2 = [(3,3,3), (4,4,4), (5,5,5), (5,3,4), (-4,-2,-3), (2,9, -6)]
    assert match_scanners(s1,s2,6) is not None
    assert match_scanners(scanners[0], scanners[1]) is not None

    map, translation_vectors = assemble_map(scanners)
    assert map is not None
    assert count_beacons(map) == 79
    print(translation_vectors)
    print(max_manhattan_distance(translation_vectors))

def main():
    scanners = parse_input("input19.txt")
    map, translation_vectors = assemble_map(scanners)
    print(count_beacons(map))
    print(max_manhattan_distance(translation_vectors))
    return(map, translation_vectors)


