def parse_input(filename):
    lines = open(filename).read().split("\n")[:-1]
    template = lines[0]
    rules = lines[2:]
    return (template, rules)

def follow_rule(bond, rules):
    rule_bonds = [rule[:2] for rule in rules]
    if bond in rule_bonds:
        return rules[rule_bonds.index(bond)][-1]
    else:
        return ""

def insert(polymer, rules):
    new_polymer = polymer[0]
    for n in range(len(polymer)-1):
        bond = polymer[n:n+2]
        new_polymer += follow_rule(bond, rules) + polymer[n+1]
    return new_polymer

def most_common(string):
    chars = list(set(string))
    counts = [string.count(char) for char in chars]
    return max(counts), chars[counts.index(max(counts))]

def least_common(string):
    chars = list(set(string))
    counts = [string.count(char) for char in chars]
    return min(counts), chars[counts.index(min(counts))]

def char_counts(bond, char, n, rules):
    if n == 0:
        return bond.count(char)
    else:
        new_molecule = follow_rule(bond, rules)
        return char_counts(bond[0] + new_molecule, char, n-1, rules) + \
            char_counts(new_molecule + bond[1], char, n-1, rules) - \
            (new_molecule == char)

### These methods aren't efficient enough to deal with large strings.
### Instead, use the fact that we just need to keep track of the number of
### each digraph (bond). The rules are encoded by a matrix acting on digraph numbers.

def count_bonds(string, all_chars):
    """all_chars a list of all characters that can occur through the transformation
    rules. We have to pass it explicitly because some of them might not occur in the
    initial string.
    """
    # Generate empty dictionary of possible bonds
    bonds = dict()
    for x in all_chars:
        for y in all_chars:
            bonds[x+y] = 0
    # Count bonds in string
    for n in range(len(string)-1):
        bonds[string[n:n+2]] += 1
    return bonds

def all_chars(rules):
    return set("".join(rules)) - {" ", "-", ">"}

def next_bonds(bonds, rules):
    """bonds a dict giving numbers of each bond. Returns a similar dict obtained by
    following the insertion rules.
    """
    new_dict = dict.fromkeys(bonds.keys(), 0)
    for rule in rules:
        new_dict[rule[0]+rule[-1]] += bonds[rule[0:2]]
        new_dict[rule[-1]+rule[1]] += bonds[rule[0:2]]
    return new_dict

def char_counts_from_dict(template, bonds, all_chars):
    """Gives dict of occurrences of each character, given initial template and dict
    of bonds after some number of iterations.
    Initial template is needed because each character will be double-counted in bonds,
    except for the initial and final characters of the string. However, these are
    the same as the initial and final characters of the template.
    """
    counts = dict.fromkeys(all_chars, 0)
    for bond in bonds:
        counts[bond[0]] += bonds[bond]
        counts[bond[1]] += bonds[bond]
    counts[template[0]] += 1
    counts[template[-1]] += 1
    for char in counts:
        counts[char] /= 2
    return counts




def test():
    template, rules = parse_input("test14.txt")
    chars = all_chars(rules)
    bonds = count_bonds(template, chars)
    print(template)
    print(bonds)
    print(char_counts_from_dict(template, bonds, chars))
    for _ in range(10):
        bonds = next_bonds(bonds, rules)
    counts = char_counts_from_dict(template, bonds, chars)
    print(max(counts.values()) - min(counts.values()))

    template, rules = parse_input("input14.txt")
    chars = all_chars(rules)
    bonds = count_bonds(template, chars)
    for _ in range(10):
        bonds = next_bonds(bonds, rules)
    counts = char_counts_from_dict(template, bonds, chars)
    print(max(counts.values()) - min(counts.values()))

def prob14a():
    polymer, rules = parse_input("input14.txt")
    for _ in range(10):
        polymer = insert(polymer, rules)
    print(most_common(polymer)[0] - least_common(polymer)[0])

def prob14b():
    template, rules = parse_input("input14.txt")
    chars = all_chars(rules)
    bonds = count_bonds(template, chars)
    for _ in range(40):
        bonds = next_bonds(bonds, rules)
    counts = char_counts_from_dict(template, bonds, chars)
    print(max(counts.values()) - min(counts.values()))

test()
prob14a()
prob14b()
