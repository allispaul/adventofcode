import math

def parse_input(filename):
    return [int(_) for _ in open(filename).read().split(",")]

class Lanternfish():

    def __init__(self, timer):
        self.timer = timer

    def __repr__(self):
        return f"Lanternfish of timer {self.timer}"

    def time(self):
        return self.timer

    def age(self):
        """Move the timer of the lanternfish one tick forward."""
        if self.timer > 0:
            self.timer = self.timer - 1
        else:
            self.timer = 6

class School():

    def __init__(self, timers):
        self.fish = []
        for timer in timers:
            self.fish.append(Lanternfish(timer))

    def __len__(self):
        return len(self.fish)

    def __repr__(self):
        return str([f.time() for f in self.fish])

    def age(self):
        babies = []
        for f in self.fish:
            if f.time() == 0:
                babies.append(Lanternfish(8))
            f.age()
        self.fish = self.fish + babies

    def sort(self):
        return sorted([f.time() for f in self.fish])

def test():
    school = School([0])
    fish_nums = []
    for day in range(20):
        school.age()
        fish_nums.append(len(school))
        # print(f"Day {day}: {len(school)} fish")
        # print(school)
        print(school.sort())
    print(fish_nums)


def prob6a():
    init_lanternfish = parse_input("input6.txt")
    school = School(init_lanternfish)
    for _ in range(80):
        school.age()
    print(len(school))

def prob6b():
    init_lanternfish = parse_input("input6.txt")
    school = School(init_lanternfish)
    for day in range(256):
        school.age()
        print(f"Day {day}: {len(school)} fish")


test()
