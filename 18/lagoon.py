import fileinput
from collections import deque

DIRS = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}

COLORS = ["R", "D", "L", "U"]


def parse():
    cmds = []
    for line in fileinput.input():
        cmd, amt, color = line.split()
        amt = int(amt)
        color = color.removeprefix("(").removesuffix(")")
        cmds.append((cmd, amt, color))
    return cmds


def parse_color(color):
    color = color.removeprefix("#")
    amt = color[:-1]
    cmd = int(color[-1])

    return COLORS[cmd], int(f"0x{amt}", base=16), color


def run(cmds, start=(0, 0)):
    grid = set()
    grid.add(start)
    row, col = start
    for cmd, amt, color in cmds:
        dr, dc = DIRS[cmd]
        for _ in range(amt):
            row, col = row + dr, col + dc
            grid.add((row, col))
    return grid


def display(grid):
    rows = [r for r, _ in grid]
    cols = [c for _, c in grid]

    for r in range(min(rows), max(rows) + 1):
        line = ["#" if (r, c) in grid else "." for c in range(min(cols), max(cols) + 1)]
        print("".join(line))
    print()


def edges(grid):
    rows = [r for r, _ in grid]
    cols = [c for _, c in grid]

    return min(rows), max(rows) + 1, min(cols), max(cols) + 1


def neighbors(grid, row, col, minr, maxr, minc, maxc):
    res = []
    for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if minr - 1 <= row + dr <= maxr and minc - 1 <= col + dc <= maxc:
            if (row + dr, col + dc) in grid:
                continue
            res.append((row + dr, col + dc))

    return res


def search(grid, start):
    seen = set()
    queue = deque([(start)])

    minr, maxr, minc, maxc = edges(grid)

    while queue:
        row, col = queue.popleft()

        if (row, col) in seen:
            continue

        seen.add((row, col))

        for nrow, ncol in neighbors(grid, row, col, minr, maxr, minc, maxc):
            queue.append((nrow, ncol))
    return seen


def count(seen, minr, maxr, minc, maxc):
    C = 0
    for r in range(minr, maxr):
        for c in range(minc, maxc):
            if (r, c) in seen:
                continue
            C += 1
    return C


def main():
    cmds = parse()

    grid = run(cmds)
    minr, maxr, minc, maxc = edges(grid)
    seen = search(grid, (minr - 1, minc - 1))
    print(f"Part 1: {count(seen, minr, maxr, minc, maxc)}")


if __name__ == "__main__":
    main()
