def parse_input(filename):
    lines = open(filename).read().split("\n")[:-1]
    output = []
    for line in lines:
        output.append(line.split("-"))
    return output

def next_nodes(this_node, arrows):
    targets = []
    for arrow in arrows:
        if arrow[0] == this_node:
            targets.append(arrow[1])
        if arrow[1] == this_node: # all arrows bidirectional
            targets.append(arrow[0])
    return targets

def print_path(path):
    print ("-".join(path))

def search_for_paths(start_node, end_node, arrows, excluded):
    """Returns paths from start_node to end_node using the arrows in arrows and not
    visiting nodes in excluded (which should be a set). Excludes paths that visit any
    lowercase nodes twice.

    Paths are expressed as tuples of nodes and should be printed with print_path.
    """
    paths_out = set()
    for node in next_nodes(start_node, arrows):
        if node == end_node:
            paths_out.add((start_node, end_node))
        elif node in excluded:
            continue
        elif node.islower():
            paths_from_node = search_for_paths(node, end_node, arrows,
                                               excluded.union({node}))
            for path in paths_from_node:
                paths_out.add((start_node,) + path)
        else:
            paths_from_node = search_for_paths(node, end_node, arrows, excluded)
            for path in paths_from_node:
                paths_out.add((start_node,) + path)
    return paths_out


def longer_paths(start_node, end_node, arrows, excluded):
    """Returns paths from start_node to end_node using the arrows in arrows and not
    visiting nodes in excluded (which should be a set). Excludes paths that visit
    more than one lowercase node twice.

    Paths are expressed as tuples of nodes and should be printed with print_path.
    paths_out now returned as a set.
    """
    paths_out = set()
    for node in next_nodes(start_node, arrows):
        if node == end_node:
            paths_out.add((start_node, end_node))
        elif node in excluded:
            continue
        elif node.islower():
            # either decide we can visit this node twice and no others:
            paths_from_node = search_for_paths(node, end_node, arrows, excluded)
            for path in paths_from_node:
                paths_out.add((start_node,) + path)
            # or agree not to visit this node twice
            paths_from_node = longer_paths(node, end_node, arrows,
                                           excluded.union({node}))
            for path in paths_from_node:
                paths_out.add((start_node,) + path)
        else:
            paths_from_node = longer_paths(node, end_node, arrows, excluded)
            for path in paths_from_node:
                paths_out.add((start_node,) + path)
    return paths_out



def test():
    arrows = parse_input("test12a.txt")
    paths = search_for_paths("start", "end", arrows, {"start"})
    print(len(paths))
    paths = longer_paths("start", "end", arrows, {"start"})
    print(len(paths))

def prob12a():
    arrows = parse_input("input12.txt")
    print(len(search_for_paths("start", "end", arrows, {"start"})))

def prob12b():
    arrows = parse_input("input12.txt")
    print(len(longer_paths("start", "end", arrows, {"start"})))

test()
prob12a()
prob12b()
