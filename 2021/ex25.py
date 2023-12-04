import os

class SeaCucumber():
    RIGHT = ">"
    DOWN = "v"

    def __init__(self, direction, x, y, grid):
        self.direction = direction
        assert self.direction in {self.RIGHT, self.DOWN}
        self.x = x
        self.y = y
        self.grid = grid
        self.to_move = False

    def look_ahead(self):
        """Return True if there is a free space ahead."""
        if self.direction == self.RIGHT:
            space_ahead = ((self.x + 1) % self.grid.x_dim, self.y)
        elif self.direction == self.DOWN:
            space_ahead = (self.x, (self.y + 1) % self.grid.y_dim)
        for creature in self.grid.census:
            if (creature.x, creature.y) == space_ahead:
                return False
        return True

    def __repr__(self):
        if self.direction == self.RIGHT:
            text_direction = "right"
        else:
            text_direction = "down"
        return f"Sea cucumber at ({self.x}, {self.y}) facing {text_direction}"

    def move_ahead(self):
        """Move one space forward."""
        if self.direction == self.RIGHT:
            space_ahead = ((self.x + 1) % self.grid.x_dim, self.y)
        elif self.direction == self.DOWN:
            space_ahead = (self.x, (self.y + 1) % self.grid.y_dim)
        (self.x, self.y) = space_ahead



class Grid():

    def __init__(self, map):
        lines = map.split("\n")[:-1]
        self.y_dim = len(lines)
        self.x_dim = len(lines[0])
        assert all(len(line) == self.x_dim for line in lines)
        assert self.x_dim >= 5
        assert self.y_dim >= 5
        self.array = [list(line) for line in lines]
        self.census = []
        for y, line in enumerate(lines):
            assert len(line) == self.x_dim
            for x, char in enumerate(line):
                if char == ">":
                    self.census.append(SeaCucumber(SeaCucumber.RIGHT, x, y, self))
                elif char == "v":
                    self.census.append(SeaCucumber(SeaCucumber.DOWN, x, y, self))
                elif char != ".":
                    raise ValueError(f"Unrecognized character: {char}")

    def __repr__(self):
        # array = [["." for x in range(self.x_dim)] for y in range(self.y_dim)]
        # for creature in self.census:
        #     try:
        #         array[creature.y][creature.x] = creature.direction
        #     except IndexError:
        #         raise IndexError(f"Creature at {creature.x, creature.y} out of range")
        # return "\n".join(["".join(row) for row in array])
        return "\n".join(["".join(row) for row in self.array])

    def move_right(self, printing=False):
        somebody_moved = False
        for row in self.array:
            to_move = []
            for x in range(self.x_dim-1):
                if row[x] == ">" and row[x+1] == ".":
                    to_move.append(x)
            if row[-1] == ">" and row[0] == ".":
                to_move.append(-1)
            for x in to_move:
                row[x] = "."
                row[x+1] = ">"
            if to_move:
                somebody_moved = True
        # for creature in self.census:
        #     creature.to_move = False
        #     if creature.direction == SeaCucumber.RIGHT:
        #         creature.to_move = creature.look_ahead()
        # for creature in self.census:
        #     if creature.to_move:
        #         creature.move_ahead()
        #         somebody_moved = True
        if printing:
            os.system("clear")
            print(self)
        return somebody_moved

    def move_down(self, printing=False):
        somebody_moved = False
        for col in range(self.x_dim):
            to_move = []
            for y in range(self.y_dim-1):
                if (self.array[y][col] == "v" and self.array[y+1][col] == "."):
                    to_move.append(y)
            if self.array[-1][col] == "v" and self.array[0][col] == ".":
                to_move.append(-1)
            for y in to_move:
                self.array[y][col] = "."
                self.array[y+1][col] = "v"
            if to_move:
                somebody_moved = True
        # somebody_moved = False
        # for creature in self.census:
        #     creature.to_move = False
        #     if creature.direction == SeaCucumber.DOWN:
        #         creature.to_move = creature.look_ahead()
        # for creature in self.census:
        #     if creature.to_move:
        #         creature.move_ahead()
        #         somebody_moved = True
        if printing:
            os.system("clear")
            print(self)
        return somebody_moved

    def step(self, printing=False):
        somebody_moved_right = self.move_right(printing)
        somebody_moved_down = self.move_down(printing)
        return somebody_moved_right or somebody_moved_down

    def settle(self, printing=False):
        somebody_moved = True
        steps = 0
        while somebody_moved:
            somebody_moved = self.step(printing)
            steps += 1
            print(steps)
        return steps


def test():
    map = open("test25.txt", "r").read()
    g = Grid(map)
    steps = g.settle(printing=True)
    print(steps)


def prob25a():
    map = open("input25.txt", "r").read()
    g = Grid(map)
    steps = g.settle(printing=True)
    print(steps)


if __name__ == "__main__":
    prob25a()
