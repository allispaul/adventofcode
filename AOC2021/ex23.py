# 15 nodes that can be occupied
# number of positions is multinomial coefficient (15, (2, 2, 2, 2, 7)) = 16,216,200

class Position():

    energy_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}

    @classmethod
    def nodes_between(cls, hall_node, room_node):
        """Return a list of nodes strictly between node1 and node2."""
        between_dict = {
            (1, 7): [],
            (1, 8): [2],
            (1, 9): [2, 3],
            (1, 10): [2, 3, 4],
            (2, 7): [],
            (2, 8): [],
            (2, 9): [3],
            (2, 10): [3, 4],
            (3, 7): [2],
            (3, 8): [],
            (3, 9): [],
            (3, 10): [4],
            (4, 7): [2, 3],
            (4, 8): [3],
            (4, 9): [],
            (4, 10): [],
            (5, 7): [2, 3, 4],
            (5, 8): [3, 4],
            (5, 9): [4],
            (5, 10): []
        }
        if hall_node >= 7 and room_node <= 6:
            # We swapped the inputs
            return cls.nodes_between(room_node, hall_node)
        if room_node >= 11:
            return cls.nodes_between(hall_node, room_node-4) + [room_node-4]
        if hall_node == 0:
            return [1] + cls.nodes_between(1, room_node)
        if hall_node == 6:
            return cls.nodes_between(5, room_node) + [5]
        return between_dict[(hall_node, room_node)]

    @classmethod
    def base_cost_between(cls, hall_node, room_node):
        """Return the cost for an "A" creature to move from hall_node to room_node."""
        if hall_node >= 7 and room_node <= 6:
            # We swapped the inputs
            return cls.base_cost_between(room_node, hall_node)
        if room_node >= 11:
            return cls.base_cost_between(hall_node, room_node-4) + 1
        if hall_node == 0:
            return cls.base_cost_between(1, room_node) + 1
        if hall_node == 6:
            return cls.base_cost_between(5, room_node) + 1
        return 2*(len(cls.nodes_between(hall_node, room_node)) + 1)

    def __init__(self, pos_string):
        pos_tuple = tuple([x if x in "ABCD" else None for x in pos_string])
        if len(pos_tuple) == 15:
            pos_tuple += ("A", "B", "C", "D", "A", "B", "C", "D")
        assert len(pos_tuple) == 23
        self.pos_tuple = pos_tuple

    def __repr__(self):
        chars = self.pos_string()
        repr = "#"*13 + "\n" + f"#{chars[0]}{chars[1]}.{chars[2]}.{chars[3]}" + \
            f".{chars[4]}.{chars[5]}{chars[6]}#\n" + \
            f"###{chars[7]}#{chars[8]}#{chars[9]}#{chars[10]}###\n"
        for i in range(11,20,4):
            repr += f"  #{chars[i]}#{chars[i+1]}#{chars[i+2]}#{chars[i+3]}#  \n"
        repr += "  " + "#"*9 + "  "
        return repr

    def __hash__(self):
        return hash(self.pos_tuple)

    def __eq__(self, pos2):
        return self.pos_tuple == pos2.pos_tuple

    def pos_string(self):
        return "".join([x if x else "." for x in self.pos_tuple])

    def is_node_empty(self, node: int):
        """Return True if node is empty."""
        return self.pos_tuple[node] == None

    def is_path_clear(self, node1, node2):
        """Return True if the path from hall_node to room_node (both ints) is clear
        of creatures.
        """
        return (all(self.is_node_empty(node)
                   for node in Position.nodes_between(node1, node2))
                and self.is_node_empty(node2))

    def is_room_correct(self, creature_type):
        """creature_type 'A', 'B', 'C', or 'D'. Checks whether the corresponding room contains
        only creatures of that type.
        """
        assert creature_type in "ABCD" and len(creature_type) == 1
        room_num = ord(creature_type) - 58 # A -> 7, B -> 8, ...
        for node in range(room_num, room_num+16, 4):
            if self.pos_tuple[node] not in {None, creature_type}:
                return False
        return True

    def front_occupied_node(self, creature_type):
        assert creature_type in "ABCD" and len(creature_type) == 1
        room = ord(creature_type) - 58 # A -> 7, B -> 8, ...
        for i in range(4):
            if self.pos_tuple[room + 4*i]:
                return room + 4*i
        return None

    def front_unoccupied_node(self, creature_type):
        assert creature_type in "ABCD" and len(creature_type) == 1
        room = ord(creature_type) - 58 # A -> 7, B -> 8, ...
        for i in range(4):
            if not self.pos_tuple[room + 12 - 4*i]:
                return room + 12 - 4*i
        return None

    def front_room_nodes(self):
        """Return a list of the frontmost occupied node in each room."""
        return [self.front_occupied_node(creature_type) for creature_type in "ABCD"
                if self.front_occupied_node(creature_type) is not None]


    def move_creature(self, start, end):
        """Return a new Position in which creature has been moved from start to end,
        together with the energy cost of this move."""
        # Check that start node is occupied and end node is empty.
        assert not self.is_node_empty(start)
        assert self.is_node_empty(end)
        assert self.is_path_clear(start, end)
        creature_to_move = self.pos_tuple[start]
        new_pos = list(self.pos_tuple)
        new_pos[end] = creature_to_move
        new_pos[start] = None
        energy_cost = self.energy_costs[self.pos_tuple[start]]*self.base_cost_between(start, end)
        new_pos_string = "".join([x if x else "." for x in new_pos])
        return Position(new_pos_string), energy_cost

    def legal_moves(self):
        """Return a list of pairs: (legal move, energy cost) from this position."""
        my_room = {None: -99, "A": 7, "B": 8, "C": 9, "D": 10}
        moves_list = []
        for hall_node in range(0, 7):
            for room_node in self.front_room_nodes():
                # Moves from rooms into hall
                # First check if path is clear
                if not self.is_path_clear(room_node, hall_node) or self.is_node_empty(room_node):
                    continue
                # Don't move if you're already in the right room and the right creatures
                # are behind you
                if (self.is_room_correct(self.pos_tuple[room_node])
                    and ord(self.pos_tuple[room_node]) - 58 - room_node % 4 == 0):
                    continue
                moves_list.append(self.move_creature(room_node, hall_node))
            if not self.is_node_empty(hall_node):
                # Moves from hall into rooms
                creature_type = self.pos_tuple[hall_node]
                if self.is_room_correct(creature_type):
                    room_node = self.front_unoccupied_node(creature_type)
                    if self.is_path_clear(hall_node, room_node):
                        moves_list.append(self.move_creature(hall_node, room_node))
        return moves_list

def BFS(start_pos, end_pos):
    reached = {start_pos: 0} # position: energy cost
    # reached = [(start_pos, 0, False)] # position, energy cost, all children calculated?
    new_moves = {start_pos}
    next_new_moves = {start_pos}
    cost_cap = None
    while next_new_moves:
        next_new_moves = set()
        status_string = f"Found {len(reached)} positions. Searching {len(new_moves)} of them."
        if end_pos in reached:
            status_string += f" Found path to target with cost {reached[end_pos]}."
            cost_cap = reached[end_pos]
        print(status_string, end="\r")
        for pos in new_moves:
            moves = pos.legal_moves()
            for move in moves:
                # Ignore expensive moves
                if cost_cap and move[1] >= cost_cap:
                    continue
                if move[0] not in reached or reached[pos] + move[1] < reached[move[0]]:
                    reached[move[0]] = reached[pos] + move[1]
                    next_new_moves.add(move[0])
                    not_all_searched = True
        new_moves = next_new_moves
    return reached[end_pos]

def DFS(start_pos, end_pos, cache=None):
    if not cache:
        cache = {start_pos: 0}
    

def test():
    # # p = Position(".......BACDBCDA")
    # p = Position("........A.B....")
    # q = Position("........B.A....")
    # # q = p.move_creature(8, 0)
    # print(p)
    # print(q)
    # moves = p.legal_moves()
    # q = moves[0][0]
    # print(BFS(q, p))
    # p = Position(".......BCBDADCA")
    # q = Position(".......ABCDABCD")
    # print(p)
    # print(q)
    # _ = input("Press ENTER to start: ")
    # print("\n" + str(BFS(p, q)))
    p = Position(".......BCBDDCBADBACADCA")
    q = Position(".......ABCDABCDABCDABCD")
    print(p)
    print(q)
    _ = input("Press ENTER to start: ")
    print("\n" + str(BFS(p, q)))

def main():
    p = Position(".......DDAADCBADBACCCBB")
    q = Position(".......ABCDABCDABCDABCD")
    print(p)
    print(q)
    _ = input("Press ENTER to start: ")
    print("\n" + str(BFS(p, q)))


if __name__ == "__main__":
    main()
