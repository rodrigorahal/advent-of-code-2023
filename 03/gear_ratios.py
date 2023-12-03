import fileinput
import math
from collections import defaultdict


def parse():
    return [line.strip() for line in fileinput.input()]


def adjecents(grid, row, col):
    H, W = len(grid), len(grid[0])
    res = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if 0 <= row + dr < H and 0 <= col + dc < W:
                res.append((row + dr, col + dc))
    return res


def nums(grid):
    res = []
    for row, values in enumerate(grid):
        num = []
        for col, value in enumerate(values):
            if value.isdigit():
                num.append(((row, col), value))
            elif not value.isdigit() and num:
                res.append(num)
                num = []
        if num:
            res.append(num)
    return res


def count(grid):
    s = 0
    for num in nums(grid):
        found = False
        for (r, c), v in num:
            for ar, ac in adjecents(grid, r, c):
                if not grid[ar][ac].isdigit() and not grid[ar][ac] == ".":
                    n = int("".join(v for _, v in num))
                    s += n
                    found = True
                    break
            if found:
                break
    return s


def find(grid):
    gears = defaultdict(set)
    for num in nums(grid):
        for (r, c), _ in num:
            for ar, ac in adjecents(grid, r, c):
                if grid[ar][ac] == "*":
                    n = int("".join(v for _, v in num))
                    gears[(ar, ac)].add(n)
    return gears


def ratio(gears):
    return sum(math.prod(nums) for nums in gears.values() if len(nums) == 2)


def main():
    grid = parse()
    print(f"Part 1: {count(grid)}")
    gears = find(grid)
    print(f"Part 2: {ratio(gears)}")


if __name__ == "__main__":
    main()
