import fileinput
from collections import deque


def parse():
    grid = []
    start = None
    for line in fileinput.input():
        grid.append(line.strip())

    for row, values in enumerate(grid):
        for col, value in enumerate(values):
            if value == "S":
                start = (row, col)

    return grid, start


def display(grid, seen=set()):
    for r, row in enumerate(grid):
        line = ["O" if (r, c) in seen else grid[r][c] for c, _ in enumerate(row)]
        print("".join(line))
    print()


def neighbors(grid, row, col):
    H, W = len(grid), len(grid[0])
    ns = []
    for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        if 0 <= row + dr < H and 0 <= col + dc < W:
            ns.append((row + dr, col + dc))
    return ns


def neighbors(grid, row, col, with_infinite=False):
    H, W = len(grid), len(grid[0])
    ns = []

    for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        if 0 <= row + dr < H and 0 <= col + dc < W:
            ns.append((row + dr, col + dc))
        elif with_infinite:
            ns.append((row + dr, col + dc))
    return ns


def get_row_at(grid, row, col):
    H, W = len(grid), len(grid[0])

    r, c = None, None

    if 0 <= row < H:
        r = row
    else:
        r = row % H

    if 0 <= col < W:
        c = col
    else:
        c = col % W

    return r, c


def get_value_at(grid, row, col):
    H, W = len(grid), len(grid[0])

    r, c = get_row_at(grid, row, col)

    return grid[r][c]


def search(grid, start, max_steps=64, with_infinite=False):
    seen = set()
    reached = set()
    row, col = start

    queue = deque([(row, col, 0)])

    while queue:
        row, col, steps = queue.popleft()

        if (row, col, steps) in seen:
            continue
        seen.add((row, col, steps))

        if steps == max_steps:
            reached.add((row, col))
            continue

        for nrow, ncol in neighbors(grid, row, col, with_infinite):
            if get_value_at(grid, nrow, ncol) in ".S":
                queue.append((nrow, ncol, steps + 1))

    return reached


def main():
    grid, start = parse()
    # print(start)
    # display(grid)

    H, W = len(grid), len(grid[0])

    reached = search(grid, start, max_steps=64)
    print(f"Part 1: {len(reached)}")

    # f(n)
    reached = search(grid, start, max_steps=65, with_infinite=True)
    f0 = len(reached)
    # f(n+H)
    reached = search(grid, start, max_steps=65 + H, with_infinite=True)
    f1 = len(reached)
    # f(n+2H)
    reached = search(grid, start, max_steps=65 + 2 * H, with_infinite=True)
    f2 = len(reached)

    print(f"{f0, f1, f2=}")
    # fit f0, f1, f2 into quadratic
    # https://www.wolframalpha.com/input?i=quadratic+fit+calculator&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3x%22%7D+-%3E%22%7B0%2C+1%2C+2%7D%22&assumption=%7B%22F%22%2C+%22QuadraticFitCalculator%22%2C+%22data3y%22%7D+-%3E%22%7B3947%2C+35153%2C+97459%7D%22
    a0 = 3947
    a1 = 15656
    a2 = 15550

    max_steps = (26501365 - 65) // H

    reached = a2 * (max_steps**2) + a1 * max_steps + a0
    print(f"Part 2: {reached}")

    # max_steps = 65 + H

    # reached = a / d + (b * max_steps) / d + (c * max_steps**2) / d
    # print(reached)

    # display(grid, reached)


if __name__ == "__main__":
    main()
