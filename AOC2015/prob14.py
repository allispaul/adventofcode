class Reindeer():
    def __init__(self, name, speed, duration, rest_time):
        self.name = name
        self.speed = speed
        self.duration = duration
        self.rest_time = rest_time

    def __repr__(self):
        return f"Reindeer {self.name}, who can travel {self.speed} km/s for" + \
            f" {self.duration} s, but then must rest for {self.rest_time} s."

    def distance_traveled(self, time):
        time_unit = self.duration + self.rest_time
        whole, remainder = time // time_unit, time % time_unit
        distance = whole*self.duration*self.speed
        if remainder <= self.duration:
            distance += remainder*self.speed
        else:
            distance += self.duration*self.speed
        return distance


def reindeer_from_string(string):
    words = string.split()
    return Reindeer(words[0], int(words[3]), int(words[6]), int(words[-2]))


def compete(reindeer_list, max_time=2503):
    scores = dict()
    for deer in reindeer_list:
        scores[deer] = 0
    for time in range(1, max_time+1):
        distances = [(deer, deer.distance_traveled(time)) for deer in reindeer_list]
        best_distance = max(distance[1] for distance in distances)
        for distance in distances:
            if distance[1] == best_distance:
                scores[distance[0]] += 1
    return scores



def test():
    comet = reindeer_from_string("Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.")
    dancer = reindeer_from_string("Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.")
    print(comet)
    print(dancer)
    for x in [1, 10, 11, 12, 138, 1000]:
        print(x, comet.distance_traveled(x), dancer.distance_traveled(x))
    scores = compete([comet, dancer], 1000)
    print(scores)


def prob14a():
    lines = open("input14.txt", 'r').read().split("\n")[:-1]
    reindeer_list = [reindeer_from_string(line) for line in lines]
    for deer in reindeer_list:
        print(deer.name, deer.distance_traveled(2503))
    scores = compete(reindeer_list)
    for deer in reindeer_list:
        print(deer.name, scores[deer])




if __name__ == "__main__":
    test()
    prob14a()
