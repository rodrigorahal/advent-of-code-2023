import fileinput
from collections import defaultdict
from copy import deepcopy


def parse():
    grid = []
    for line in fileinput.input():
        grid.append([char for char in line.strip()])
    return grid


def display(grid):
    for row in grid:
        print("".join(row))
    print()


def tilt_north(grid):
    H = len(grid)
    W = len(grid[0])
    for row in range(1, H):
        for col in range(W):
            rock = grid[row][col]
            if rock in ".#":
                continue

            curr = row
            r = row - 1
            for r in range(row - 1, -1, -1):
                if grid[r][col] != ".":
                    break
                curr = r

            if curr != row:
                grid[curr][col] = rock
                grid[row][col] = "."

    return grid


def tilt_south(grid):
    H = len(grid)
    W = len(grid[0])

    for row in range(H - 2, -1, -1):
        for col in range(W):
            rock = grid[row][col]
            if rock in ".#":
                continue

            curr = row
            r = row + 1
            for r in range(row + 1, H):
                if grid[r][col] != ".":
                    break
                curr = r
            if curr != row:
                grid[curr][col] = rock
                grid[row][col] = "."

    return grid


def tilt_west(grid):
    H = len(grid)
    W = len(grid[0])

    for col in range(1, W):
        for row in range(H):
            rock = grid[row][col]
            if rock in ".#":
                continue

            curr = col
            c = col - 1
            for c in range(col - 1, -1, -1):
                if grid[row][c] != ".":
                    break
                curr = c

            if curr != col:
                grid[row][curr] = rock
                grid[row][col] = "."
    return grid


def tilt_east(grid):
    H = len(grid)
    W = len(grid[0])

    for col in range(W - 2, -1, -1):
        for row in range(H):
            rock = grid[row][col]
            if rock in ".#":
                continue

            curr = col
            c = col + 1
            for c in range(col + 1, W):
                if grid[row][c] != ".":
                    break
                curr = c

            if curr != col:
                grid[row][curr] = rock
                grid[row][col] = "."
    return grid


def load(grid):
    H = len(grid)
    L = 0
    for row, rocks in enumerate(grid):
        L += (H - row) * sum(rock == "O" for rock in rocks)
    return L


def cycle(grid, n=1):
    seen = defaultdict(list)

    next_in_cycle = None

    for i in range(n):
        grid = tilt_north(grid)
        grid = tilt_west(grid)
        grid = tilt_south(grid)
        grid = tilt_east(grid)

        load_ = load(grid)

        if next_in_cycle == i:
            return load_

        seen[load_].append(i)

        # arbitrary
        if len(seen[load(grid)]) > 3:
            if seen[load_][-1] - seen[load_][-2] == seen[load_][-2] - seen[load_][-3]:
                cycle_len = seen[load_][-1] - seen[load_][-2]
                next_in_cycle = ((1000000000 - i) % cycle_len) + i - 1


def main():
    grid = parse()
    tilted = tilt_north(deepcopy(grid))
    print(f"Part 1: {load(tilted)}")
    print(f"Part 2: {cycle(deepcopy(grid), n=1000000000)}")


if __name__ == "__main__":
    main()
