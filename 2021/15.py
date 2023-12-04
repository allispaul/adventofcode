import os
import time
import heapq
color = {"RED": "\033[31m", "GREEN": "\033[32m", "END": "\033[0m"}

def parse_input(filename):
    lines = open(filename).read().split("\n")[:-1]
    array = []
    for line in lines:
        array.append([int(x) for x in line])
    return array

def accessible_nodes(node, array):
    """node an ordered pair, array an array.

    Returns the set of all ordered pairs horizontally or vertically next to
    node in array.
    """
    maxX = len(array[0])
    maxY = len(array)
    if node[0] < 0 or node[0] >= maxX or node[1] < 0 or node[1] >= maxY:
        raise ValueError(f"Node at {node} not in array")
    nodes = set()
    if node[0] > 0:
        nodes.add((node[0]-1,node[1]))
    if node[1] > 0:
        nodes.add((node[0],node[1]-1))
    if node[0] < maxX-1:
        nodes.add((node[0]+1,node[1]))
    if node[1] < maxY-1:
        nodes.add((node[0],node[1]+1))
    return nodes


def safest_path(risk_levels, start, end, *, printing=None, h = lambda x: 0):
    """risk_levels an array of numbers, start and end two ordered pairs specifying
    positions in the array. printing=x shows a visualization of the function's
    progress constructing the path, with a pause of x seconds in between each frame.
    h is a heuristic function used for the more efficient A* variant.

    Returns (1) a dict containing the safest path from start to end, in the following
    format: for each edge A -> B on the path, safest_path[B] = A. The dict will also
    contain the safest path from start to other nodes (for example, to every node
    visited on the safest path to end), but is not guaranteed to contain the safest
    path to any particular node besides end.

    Returns (2) the total risk of the safest path from start to end.

    When h=0, this is the Dijkstra shortest-path algorithm. Here's how it works:
    1. Mark start as the current node, and its distance as 0.
    2. Follow each edge out of the current node.
    3. If a node A accessible from the current node has not been studied, and
    either it has never been reached before or
    (distance to current) + (edge length from current to A) < (distance to A),
    set the distance to A and shortest path to A accordingly.
    4. Once all edges out of the current node have been followed, mark
    the current node as studied. (There is no use in returning to it.)
    5. Repeat, taking the unstudied node with the shortest distance as current.

    When h is defined, this is the A* algorithm, which varies the Dijkstra algorithm
    by replacing step 5 with:
    5. Repeat, taking the unstudied node x minimizing distance(x) + h(x) as current.
    The A* algorithm is guaranteed to find a least-cost past as long as h(x) never
    overestimates the actual distance from x to end. A good choice of h here is the
    L1 distance to end (because the risk of every node is at least 1).
    """

    # Initialize outputs and local variables
    path = dict()
    studied = set()
    prev = None
    # Entries in queue have the format:
    ### (sort_priority, (x1, y1), (x0, y0)).
    ### sort_priority = distance + h is used to order the queue.
    ### (x1, y1) is the node, (x0, y0) is the node it was reached from
    ### (used to compute the path).
    queue = [(h(start), (start[0], start[1]), None)]

    # Main loop
    while queue:
        est_dist, current, prev = heapq.heappop(queue)
        # Check if we've already seen this one
        if current in studied:
            continue
        # Draw path to the node we came from
        if prev:
            path[current] = prev
        # Check if we're done
        if current == end:
            # The estimated distance of end is its actual distance
            return path, est_dist

        next_nodes = accessible_nodes(current, risk_levels).difference(studied)
        for node in next_nodes:
            risk = risk_levels[node[1]][node[0]]
            next_dist = est_dist + risk + h(node) - h(current)
            if printing != None:
                print(f"Starting at {current}, estimated distance of {est_dist}, "
                      + f"h = {h(current)}")
                print(f"Can move to {node}, risk level {risk}, h = {h(node)}, "
                      + f"new estimated distance of {next_dist}")
            heapq.heappush(queue, (next_dist, node, current))
            # It doesn't matter if node is already in the heap, since we'll only ever
            ### use the version of it with the lowest est_dist.
        # Display search progress
        if printing != None and path: # allow printing=0 for no pause
            time.sleep(printing)
            highlight_path(risk_levels, trace_path(path, start, current),
                           studied)
            print(f"Looking at: {current}, estimated distance: {est_dist}")
        studied.add(current)

def trace_path(path, start, end):
    """path a dict of safest paths. Extracts a list describing the safest path
    from start to end"""
    path_list = [end]
    while start not in path_list:
        path_list.append(path[path_list[-1]])
        path_list.reverse()
    return path_list

def highlight_path(array, path, studied=set()):
    """path a list of ordered pairs, studied a set of ordered pairs. Clears the
    screen and prints array with path and studied highlighted.
    """
    for y in range(len(array)):
        line = ""
        for x in range(len(array[0])):
            if (x, y) in path:
                line += color["RED"] + str(array[y][x]) + color["END"]
            elif (x, y) in studied:
                line += color["GREEN"] + str(array[y][x]) + color["END"]
            else:
                line += str(array[y][x])
        print(line)

def augmod9(line, k):
    """Only use this for k < 9."""
    newline = line.copy()
    for n in range(len(line)):
        newline[n] += k
        if newline[n] > 9:
            newline[n] -= 9
    return newline

def quintuple(array):
    new_array = [[] for _ in range(len(array))]
    for y, line in enumerate(array):
        for counter in range(5):
            new_array[y] += augmod9(line, counter)
    for counter in range(1,5):
        for y in range(len(array)):
            new_array.append(augmod9(new_array[y], counter))
    return new_array

def test():
    risk_levels = parse_input("test15.txt")

    _ = input("Starting search without heuristic...")
    tic = time.perf_counter()
    path1, distance1 = safest_path(risk_levels, (0,0), (9,9),)
    toc = time.perf_counter()
    time1 = toc-tic

    _ = input("Starting search with heuristic...")
    tic = time.perf_counter()
    path2, distance2 = safest_path(risk_levels, (0,0), (9,9), printing=0,
                                  h=lambda x: (9-x[0]) + (9-x[1]))
    toc = time.perf_counter()
    time2 = toc-tic
    print(highlight_path(risk_levels, trace_path(path1, (0,0), (9,9))))
    print(highlight_path(risk_levels, trace_path(path2, (0,0), (9,9))))
    print(f"No heuristic: finished in {time1:0.4f}s and found distance {distance1}.")
    print(f"Heuristic: finished in {time2:0.4f}s and found distance {distance2}.")


def prob15a():
    risk_levels = parse_input("input15.txt")
    maxX = len(risk_levels[0])
    maxY = len(risk_levels)
    end = (maxX-1, maxY-1)

    _ = input("Starting search without heuristic...")
    tic = time.perf_counter()
    path, distance_nh = safest_path(risk_levels, (0,0), end)
    time_nh = time.perf_counter() - tic

    _ = input("Starting search with heuristic...")
    tic = time.perf_counter()
    path, distance_h = safest_path(risk_levels, (0,0), end,
                                  h = lambda pt: (end[0] - pt[0]) + (end[1] - pt[1]))
    time_h = time.perf_counter() - tic

    _ = input("Starting search with strong heuristic...")
    tic = time.perf_counter()
    path, distance_sh = safest_path(risk_levels, (0,0), end,
                              h = lambda pt: 9*((end[0] - pt[0]) + (end[1] - pt[1])))
    time_sh = time.perf_counter() - tic

    print(f"No heuristic: finished in {time_nh:0.4f}s and found "
          + f"distance {distance_nh}.")
    print(f"Heuristic: finished in {time_h:0.4f}s and found "
          + f"distance {distance_h}.")
    print(f"Strong heuristic: finished in {time_sh:0.4f}s and found "
          + f"distance {distance_sh}.")

def prob15b():
    risk_levels = quintuple(parse_input("input15.txt"))
    maxX = len(risk_levels[0])
    maxY = len(risk_levels)
    end = (maxX-1, maxY-1)
    tic = time.perf_counter()
    path, distance = safest_path(risk_levels, (0,0), end)
    time_nh = time.perf_counter() - tic
    print(distance)
    print(f"Found in {time_nh:0.4f}s.")

    tic = time.perf_counter()
    path, distance = safest_path(risk_levels, (0,0), end, h=lambda x: end[0] - x[0]
                                 + end[1] - x[1])
    time_nh = time.perf_counter() - tic
    print(distance)
    print(f"Found in {time_nh:0.4f}s.")

# test()
# prob15a()
prob15b()
