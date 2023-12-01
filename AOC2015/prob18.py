import os


class Grid():
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),  (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    ON = "#"
    OFF = "."

    def __init__(self, data):
        self.y_dim = len(data)
        self.x_dim = len(data[0])
        self.values = []
        for row in data:
            assert len(row) == self.x_dim
            self.values.append(list(row))

    def __repr__(self):
        repr = ""
        for row in self.values:
            for node in row:
                repr += node
            repr += "\n"
        return repr

    def is_on(self, x, y):
        if x < 0 or x >= self.x_dim or y < 0 or y >= self.y_dim:
            return False
        return self.values[y][x] == self.ON

    def neighbors(self, x, y):
        count = 0
        for direction in self.DIRECTIONS:
            if self.is_on(x + direction[0], y + direction[1]):
                count += 1
        return count

    def count_on(self):
        count = 0
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if self.is_on(x, y):
                    count += 1
        return count

    def update_from_list(self, data):
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                self.values[y][x] = Grid.OFF
        for (x, y) in data:
            self.values[y][x] = Grid.ON

    def step_time(self):
        on_next_step = []
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if self.is_on(x, y) and self.neighbors(x, y) in {2, 3}:
                    on_next_step.append((x, y))
                elif not self.is_on(x, y) and self.neighbors(x, y) == 3:
                    on_next_step.append((x, y))
        self.update_from_list(on_next_step)


class BustedGrid(Grid):
    def __init__(self, data):
        super().__init__(data)
        self.values[0][0] = Grid.ON
        self.values[self.y_dim-1][0] = Grid.ON
        self.values[0][self.x_dim-1] = Grid.ON
        self.values[self.y_dim-1][self.x_dim-1] = Grid.ON

    def update_from_list(self, data):
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                self.values[y][x] = Grid.OFF
        for (x, y) in data:
            self.values[y][x] = Grid.ON
        self.values[0][0] = Grid.ON
        self.values[self.y_dim-1][0] = Grid.ON
        self.values[0][self.x_dim-1] = Grid.ON
        self.values[self.y_dim-1][self.x_dim-1] = Grid.ON


test_data = """.#.#.#
...##.
#....#
..#...
#.#..#
####..""".split("\n")


def test():
    g = Grid(test_data)
    print(g)
    while True:
        _ = input("> ")
        g.step_time()
        os.system("clear")
        print(g)


def test_busted():
    g = BustedGrid(test_data)
    print(g)
    while True:
        _ = input("> ")
        g.step_time()
        os.system("clear")
        print(g)


def prob18a():
    starting_grid = open("input18.txt", "r").read().split("\n")[:-1]
    g = Grid(starting_grid)
    print(g)
    for n in range(100):
        g.step_time()
        os.system("clear")
        print(g)
    print(g.count_on())


def prob18b():
    starting_grid = open("input18.txt", "r").read().split("\n")[:-1]
    g = BustedGrid(starting_grid)
    print(g)
    for n in range(100):
        g.step_time()
        os.system("clear")
        print(g)
    print(g.count_on())

def main():
    starting_grid = open("input18.txt", "r").read().split("\n")[:-1]
    g = Grid(starting_grid)
    print(g)
    while True:
        g.step_time()
        os.system("clear")
        print(g)

if __name__ == "__main__":
    main()
