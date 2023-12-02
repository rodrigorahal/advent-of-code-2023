import fileinput
import math


def parse():
    games = {}
    for line in fileinput.input():
        game, contents = line.strip().split(": ")
        id = int(game.split(" ")[-1])

        rounds = contents.split("; ")
        parsed_rounds = []
        for round in rounds:
            parsed_round = []
            cubes = round.split(", ")
            for cube in cubes:
                n, color = cube.split(" ")
                parsed_round.append((int(n), color))
            parsed_rounds.append(parsed_round)
        games[id] = parsed_rounds
    return games


def count(games):
    return sum(id for id, game in games.items() if is_valid(game))


def power(games):
    return sum(math.prod(min_cubes(game)) for id, game in games.items())


def min_cubes(game):
    mins = [0, 0, 0]
    for round in game:
        for n, color in round:
            if color == "red":
                mins[0] = max(mins[0], n)
            elif color == "green":
                mins[1] = max(mins[1], n)
            elif color == "blue":
                mins[2] = max(mins[2], n)
    return mins


def is_valid(game):
    for round in game:
        for n, color in round:
            if color == "red" and n > 12:
                return False
            elif color == "green" and n > 13:
                return False
            elif color == "blue" and n > 14:
                return False
    return True


def main():
    games = parse()
    print(f"Part 1: {count(games)}")
    print(f"Part 2: {power(games)}")


if __name__ == "__main__":
    main()
