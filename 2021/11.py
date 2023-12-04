import os
import time

def parse_input(filename):
    output = []
    lines = open(filename).read().split("\n")[:-1]
    for line in lines:
        output.append([int(x) for x in line])
    return output

color = {"RED": "\033[31m", "END": "\033[0m"}

dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

class Dumbo_Grid():

    def __init__(self, energies):
        self.energies = energies
        self.all_flashed = False

    def __repr__(self):
        output = ""
        for line in self.energies:
            for num in line:
                if num <= 9:
                    output += "\033[3" + str(num) + "m" + str(num) + color["END"]
                else:
                    output += str(num)
            output += "\n"
        return output

    def step(self):
        """Returns the number of flashes."""
        flashed = set()
        X = len(self.energies[0])
        Y = len(self.energies)
        # increase all energies
        for y in range(Y):
            for x in range(X):
                self.energies[y][x] += 1
        # now flash octopuses as long as new ones keep flashing
        new_flashes = True
        while new_flashes:
            new_flashes = False
            for y in range(Y):
                for x in range(X):
                    # flash each octopus with high energy that hasn't flashed
                    if self.energies[y][x] > 9 and (x, y) not in flashed:
                        flashed.add((x,y))
                        new_flashes = True
                        # add 1 to each adjacent energy
                        # OK if they've already flashed, as their energy will
                        # get reset anyway
                        for dir in dirs:
                            if (0 <= x+dir[0] < X) and (0 <= y+dir[1] < Y):
                                self.energies[y+dir[1]][x+dir[0]] += 1
        # now reset any octopus that flashed
        for (x, y) in flashed:
            self.energies[y][x] = 0
        # check if everything flashed
        self.all_flashed = (len(flashed) == X*Y)
        return len(flashed)


def test():
    my_grid = Dumbo_Grid(parse_input("test11.txt"))
    counter = 0
    while not my_grid.all_flashed:
        counter += 1
        my_grid.step()
        os.system("clear")
        print(my_grid)
        time.sleep(0.1)
    print(counter)

def prob11a():
    my_grid = Dumbo_Grid(parse_input("input11.txt"))
    counter = 0
    for _ in range(100):
        counter += my_grid.step()
    print(counter)

def prob11b():
    my_grid = Dumbo_Grid(parse_input("input11.txt"))
    counter = 0
    while not my_grid.all_flashed:
        counter += 1
        my_grid.step()
    print(counter)

test()
prob11a()
prob11b()
