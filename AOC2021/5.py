# Read input
def parse_input(filename):
    INPUT = filename
    data = open(INPUT, "r").read().split("\n")[:-1]
    # Parse data into a list of lists of numbers
    coords_list = []
    for line in data:
        coords = line.replace(" -> ", ",").split(",")
        coords = [int(n) for n in coords]
        coords_list.append(coords)
    print("Parsed list of", len(coords_list), "lines.")
    return coords_list

class Line():

    def __init__(self, nums):
        assert len(nums) == 4
        self.tail = nums[0:2]
        self.tip = nums[2:4]

    def __repr__(self):
        return "{:d},{:d} -> {:d},{:d}".format(self.tail[0], self.tail[1],
                                               self.tip[0], self.tip[1])

    def direction(self):
        if self.tail[1] == self.tip[1]: #horizontal
            if self.tip[0] >= self.tail[0]:
                return "E" # length 1 lines count as east
            else:
                return "W"
        elif self.tail[0] == self.tip[0]: #vertical
            if self.tip[1] > self.tail[1]:
                return "S"
            else:
                return "N"
        elif self.tail[0] - self.tail[1] == self.tip[0] - self.tip[1]:
            if self.tip[0] > self.tail[0]:
                return "SE"
            else:
                return "NW"
        elif self.tail[0] + self.tail[1] == self.tip[0] + self.tip[1]:
            if self.tip[0] > self.tail[0]:
                return "NE"
            else:
                return "SW"
        else:
            raise ValueError("The line", self,
                             "does not point in a cardinal direction.")

    def is_orthogonal(self):
        return self.direction() in {"N", "E", "S", "W"}

    def points_covered(self):
        direction = self.direction()
        if direction == "E":
            return [(x, self.tail[1]) for x in range(self.tail[0], self.tip[0]+1)]
        elif direction == "W":
            return [(x, self.tail[1]) for x in range(self.tail[0], self.tip[0]-1, -1)]
        elif direction == "S":
            return [(self.tail[0], y) for y in range(self.tail[1], self.tip[1]+1)]
        elif direction == "N":
            return [(self.tail[0], y) for y in range(self.tail[1], self.tip[1]-1, -1)]
        elif direction == "SE":
            return [(x, x + self.tail[1] - self.tail[0])
                    for x in range(self.tail[0], self.tip[0]+1)]
        elif direction == "NW":
            return [(x, x + self.tail[1] - self.tail[0])
                    for x in range(self.tail[0], self.tip[0]-1, -1)]
        elif direction == "NE":
            return [(x, self.tail[1] + self.tail[0] - x)
                    for x in range(self.tail[0], self.tip[0]+1)]
        elif direction == "SW":
            return [(x, self.tail[1] + self.tail[0] - x)
                    for x in range(self.tail[0], self.tip[0]-1, -1)]
        else:
            raise ValueError()

class Grid():

    def __init__(self, coords):
        self.lines = []
        for coord in coords:
            l = Line(coord)
            self.lines.append(l)
        self.max_x = max(x for l in self.lines for x in [l.tail[0], l.tip[0]])
        self.max_y = max(y for l in self.lines for y in [l.tail[1], l.tip[1]])
        self.points = self.count_lines()

    def count_lines(self):
        """Defines an array containing the number of lines passing through each point.
        """
        points = [[0]*(self.max_y+1) for _ in range(self.max_x+1)]
        for l in self.lines:
            for x, y in l.points_covered():
                points[x][y] = points[x][y] + 1
        return points

    def __repr__(self):
        display = ""
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if self.points[x][y]:
                    display = display + "{:>2d}".format(self.points[x][y])
                else:
                    display = display + " ."
            display = display + "\n"
        return display

    def count_intersections(self):
        """Counts the total number of line intersections."""
        intersections = 0
        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                if self.points[x][y] > 1:
                    intersections = intersections + 1
        return intersections


def unit_test():
    coords_list = parse_input("test5.txt")
    grid = Grid(coords_list)
    for l in grid.lines:
        print(f"Line {l} in direction {l.direction()} and covering the points {l.points_covered()}.")
    print(grid)
    print(grid.count_intersections())

def prob5a():
    coords_list = parse_input("input5.txt")
    grid = Grid(coords_list)
    print("Constructed {} by {} grid with {} lines.".format(grid.max_x, grid.max_y,
                                                            len(grid.lines)))
    print(grid.count_intersections())

prob5a()
