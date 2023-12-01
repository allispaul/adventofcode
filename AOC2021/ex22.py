import re
import sys

class Reactor():
    def __init__(self):
        self.cubes = dict()

    def apply_instruction(self, xmin, xmax, ymin, ymax, zmin, zmax, on):
        if (xmin > 50 or ymin > 50 or zmin > 50 or xmax < -50 or ymax < -50
            or zmax < -50):
            return None
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                for z in range(zmin, zmax+1):
                    if on:
                        self.cubes[(x,y,z)] = 1
                    else:
                        self.cubes[(x,y,z)] = 0

    def on_cubes(self):
        count = 0
        for k in self.cubes.keys():
            if self.cubes[k]:
                count += 1
        return count


def cap(n):
    if n >= 51:
        return 51
    elif n <= -51:
        return -51
    else:
        return n

def parse_instruction(text):
    m = re.match(r"(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", text)
    if m.group(1) == "on":
        on = True
    elif m.group(1) == "off":
        on = False
    else:
        raise SyntaxError(f"Unrecognized instruction {m.group(1)}")
    dims = [int(m.group(n)) + (n % 2) for n in range(2, 8)]
    return tuple(dims) + (on,)


class Cube():
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        """A Cube contains everything in the box xmin <= x < xmax, ymin <= y < ymax,
        zmin <= z < zmax.
        """

        if xmin > xmax:
            xmin = xmax
        if ymin > ymax:
            ymin = ymax
        if zmin > zmax:
            zmin = zmax
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def contained_in(self, cube2):
        """Return True if this cube is completely contained in cube2."""
        return (self.xmin >= cube2.xmin and
                self.ymin >= cube2.ymin and
                self.zmin >= cube2.zmin and
                self.xmax <= cube2.xmax and
                self.ymax <= cube2.ymax and
                self.zmax <= cube2.zmax)

    def intersect(self, cube2):
        return Cube(max(self.xmin, cube2.xmin), min(self.xmax, cube2.xmax),
                    max(self.ymin, cube2.ymin), min(self.ymax, cube2.ymax),
                    max(self.zmin, cube2.zmin), min(self.zmax, cube2.zmax))

    def __repr__(self):
        return f"Cube with x={self.xmin}..{self.xmax-1},y={self.ymin}..{self.ymax-1},z={self.zmin}..{self.zmax-1}"

    def split(self, value, plane):
        """Split this cube along a plane. Return a list of cubes."""
        if plane == "x":
            if self.xmin < value < self.xmax:
                return [Cube(self.xmin, value, self.ymin, self.ymax, self.zmin, self.zmax),
                        Cube(value, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)]
        elif plane == "y":
            if self.ymin < value < self.ymax:
                return [Cube(self.xmin, self.xmax, self.ymin, value, self.zmin, self.zmax),
                        Cube(self.xmin, self.xmax, value, self.ymax, self.zmin, self.zmax)]
        elif plane == "z":
            if self.zmin < value < self.zmax:
                return [Cube(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, value),
                        Cube(self.xmin, self.xmax, self.ymin, self.ymax, value, self.zmax)]
        else:
            raise ValueError(f"Couldn't split along plane {plane}")
        return [self]

    def dissect(self, cube2):
        """Cut self into smaller cubes, such that each one is either contained in, or
        disjoint from, cube2.
        """
        cubes_list = [self]
        for (value, plane) in [(cube2.xmin, "x"), (cube2.xmax, "x"),
                               (cube2.ymin, "y"), (cube2.ymax, "y"),
                               (cube2.zmin, "z"), (cube2.zmax, "z")]:
            new_cubes_list = []
            for cube in cubes_list:
                new_cubes_list += cube.split(value, plane)
            cubes_list = new_cubes_list
        return cubes_list

    def volume(self):
        return (self.xmax - self.xmin)*(self.ymax - self.ymin)*(self.zmax - self.zmin)

class FullReactor():
    def __init__(self):
        self.cubes = []

    def on_cubes(self):
        count = 0
        for cube in self.cubes:
            count += (cube.xmax - cube.xmin)*(cube.ymax - cube.ymin)*(cube.zmax - cube.zmin)
        return count

    # def __repr__(self):
    #     repr = ""
    #     for cube in self.cubes:
    #         repr += cube.__repr__() + "\n"
    #     return repr

    def activate_cube(self, xmin, xmax, ymin, ymax, zmin, zmax):
        new_cube = Cube(xmin, xmax, ymin, ymax, zmin, zmax)
        cubes_list = []
        for old_cube in self.cubes:
            cubes_list += old_cube.dissect(new_cube)
        self.cubes = [cube for cube in cubes_list if not cube.contained_in(new_cube)]
        self.cubes.append(new_cube)

    def deactivate_cube(self, xmin, xmax, ymin, ymax, zmin, zmax):
        new_cube = Cube(xmin, xmax, ymin, ymax, zmin, zmax)
        cubes_list = []
        for old_cube in self.cubes:
            cubes_list += old_cube.dissect(new_cube)
        self.cubes = [cube for cube in cubes_list if not cube.contained_in(new_cube)]

    def apply_instruction(self, args):
        if args[6]:
            self.activate_cube(args[0], args[1]+1, args[2], args[3]+1, args[4], args[5]+1)
        else:
            self.deactivate_cube(args[0], args[1]+1, args[2], args[3]+1, args[4], args[5]+1)

def test1():
    steps = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".split("\n")
    r = Reactor()
    for step in steps:
        r.apply_instruction(*parse_instruction(step))
    print(r.on_cubes())

def test2():
    steps = open("test22.txt", 'r').read().split("\n")[:-3]
    r = Reactor()
    for step in steps:
        r.apply_instruction(*parse_instruction(step))
    print(r.on_cubes())
    return r

def prob22a():
    steps = open("input22.txt", 'r').read().split("\n")[:-3]
    r = Reactor()
    for step in steps:
        r.apply_instruction(*parse_instruction(step))
    print(r.on_cubes())
    return r

def test3():
    steps = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".split("\n")
    r = FullReactor()
    for step in steps:
        print(r)
        print(step)
        r.apply_instruction(parse_instruction(step))
    print(r.on_cubes())

def test4():
    steps = open("test22b.txt", 'r').read().split("\n")[:-1]
    r = FullReactor()
    for count, step in enumerate(steps):
        print(f"Applying instruction {count} of {len(steps)}...")
        r.apply_instruction(parse_instruction(step))
    return r.on_cubes()

def prob22b():
    steps = open("input22.txt", 'r').read().split("\n")[:-1]
    r = FullReactor()
    for count, step in enumerate(steps):
        print(f"Applying instruction {count} of {len(steps)}...")
        r.apply_instruction(parse_instruction(step))
    return r.on_cubes()

# This is still too slow!
# Let's try a completely different strategy:

def prob22bredux(filename):
    steps = [parse_instruction(line)
             for line in open(filename, 'r')]
    x_breaks = [inst[0] for inst in steps] + [inst[1]+1 for inst in steps]
    x_breaks = list(set(x_breaks))
    x_breaks.sort()
    xmin = min(x_breaks)
    xmax = max(x_breaks)
    y_breaks = [inst[2] for inst in steps] + [inst[3]+1 for inst in steps]
    y_breaks = list(set(y_breaks))
    y_breaks.sort()
    ymin = min(y_breaks)
    ymax = max(y_breaks)
    z_breaks = [inst[4] for inst in steps] + [inst[5]+1 for inst in steps]
    z_breaks = list(set(z_breaks))
    z_breaks.sort()
    zmin = min(z_breaks)
    zmax = max(z_breaks)
    lit_cubes = 0
    print(f"{len(x_breaks)=}, {len(y_breaks)=}, {len(z_breaks)=}")
    for x_idx, left_edge in enumerate(x_breaks[:-1]):
        for y_idx, front_edge in enumerate(y_breaks[:-1]):
            for z_idx, bottom_edge in enumerate(z_breaks[:-1]):
                lit = False
                for inst in steps[::-1]:
                    if (inst[0] <= left_edge <= inst[1] and
                        inst[2] <= front_edge <= inst[3] and
                        inst[4] <= bottom_edge <= inst[5]):
                        lit = inst[6]
                        break
                if lit:
                    cube_size = (x_breaks[x_idx+1]-left_edge) * (y_breaks[y_idx+1]-front_edge) \
                        * (z_breaks[z_idx+1]-bottom_edge)

                    lit_cubes += cube_size
                # print(f"x={left_edge}..{x_breaks[x_idx+1]-1}, " +
                #         f"y={front_edge}..{y_breaks[y_idx+1]-1}, " +
                #         f"z={bottom_edge}..{z_breaks[z_idx+1]-1} --> {lit} by step {step_num}")
                print(f"Checking cube #{x_idx, y_idx, z_idx}", end="\r")
    return lit_cubes

# Still too slow!

def inclusion_exclusion(cubes):
    """Takes a list of Cubes. Returns the volume of cubes[0] - (union cubes[1:])."""
    # print(f"Starting inclusion/exclusion on {cubes}.")
    if len(cubes) == 0:
        # print("Empty list, returning 0")
        return 0
    elif len(cubes) == 1:
        # print(f"Singleton list, returning volume of {cubes[0]}, which is {cubes[0].volume()}")
        return cubes[0].volume()
    # Only need to consider cubes that meet cubes[0], and only need to consider
    # their intersections with cubes[0].
    new_cubes = []
    for cube in cubes[1:]:
        smaller_cube = cubes[0].intersect(cube)
        if smaller_cube.volume() > 0:
            new_cubes.append(smaller_cube)
    # print(f"Replaced list with {new_cubes}")
    # Calculation
    difference = sum([inclusion_exclusion(new_cubes[i:]) for i in range(len(new_cubes))])
    # print(f"Difference is {difference}")
    # print(f"For {cubes}, returning {cubes[0].volume() - difference}")
    return cubes[0].volume() - difference

def prob22bonemogain(filename):
    steps = [parse_instruction(line)
             for line in open(filename, 'r')]
    # print(steps)
    total_vol = 0
    for step_num, step in enumerate(steps):
        if step[6]:
            vol = inclusion_exclusion([Cube(*step[:6]) for step in steps[step_num:]])
            total_vol += vol
    return total_vol





if __name__ == "__main__":
    filename = sys.argv[1]
    lit_cubes = prob22bredux(filename)
    print("")
    print(lit_cubes)

