import fileinput
import math


def parse():
    res = []
    for line in fileinput.input():
        _, values = line.strip().split(":")
        res.append([int(v) for v in values.split()])
    times, dists = res
    return times, dists


def race(time, dist):
    wins = 0
    for hold in range(time + 1):
        speed = hold
        traveled = (time - hold) * speed
        wins += traveled > dist
    return wins


def simulate(times, dists):
    return math.prod(race(time, dist) for time, dist in zip(times, dists))


def main():
    times, dists = parse()
    print(f"Part 1: {simulate(times, dists)}")

    time = int("".join([str(t) for t in times]))
    dist = int("".join([str(t) for t in dists]))

    print(f"Part 2: {race(time, dist)}")


if __name__ == "__main__":
    main()
