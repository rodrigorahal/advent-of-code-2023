import fileinput
from copy import deepcopy
from collections import deque
from itertools import combinations


def parse():
    grid = []
    for line in fileinput.input():
        grid.append([char for char in line.strip()])
    return grid


def display(grid):
    for row in grid:
        print("".join(row))
    print()


def expand(grid):
    expanded = []

    for row in grid:
        if all(char == "." for char in row):
            expanded.append(row)
        expanded.append(row)

    expanded = list(zip(*expanded))
    egrid = deepcopy(expanded)
    grid = zip(*grid)

    j = 0
    for col in egrid:
        if all(char == "." for char in col):
            expanded.insert(j, col)
            j += 1
        j += 1

    expanded = list(zip(*expanded))

    return expanded


def galaxies(grid):
    g = []
    for row, cols in enumerate(grid):
        for col, char in enumerate(cols):
            if char == "#":
                g.append((row, col))
    return g


def neighbors(grid, row, col):
    H, W = len(grid), len(grid[0])
    ns = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= row + dr < H and 0 <= col + dc < W:
            ns.append((row + dr, col + dc))
    return ns


def all_pairs_shortest_paths(grid, empty_rows, empty_cols, expansion):
    G = set(galaxies(grid))
    pairs = set()
    S = 0

    def bfs(grid, start, S):
        seen = set()
        queue = deque([(start, 0)])

        while queue:
            (row, col), steps = queue.popleft()

            if (row, col) in seen:
                continue

            if (row, col) != start and (row, col) in G:
                if ((row, col), start) not in pairs and (
                    start,
                    (row, col),
                ) not in pairs:
                    S += steps
                    pairs.add((start, (row, col)))

            seen.add((row, col))

            for nr, nc in neighbors(grid, row, col):
                if (nr, nc) not in seen:
                    if row in empty_rows and nr != row:
                        queue.append(((nr, nc), steps + expansion))
                    elif col in empty_cols and nc != col:
                        queue.append(((nr, nc), steps + expansion))
                    else:
                        queue.append(((nr, nc), steps + 1))
        return S

    for start in G:
        S = bfs(grid, start, S)

    return S


def empty(grid):
    G = deepcopy(grid)
    rows = set()
    cols = set()

    for row, vals in enumerate(G):
        if all(char == "." for char in vals):
            rows.add(row)

    G = list(zip(*G))

    for col, vals in enumerate(G):
        if all(char == "." for char in vals):
            cols.add(col)

    return rows, cols


def main():
    grid = parse()
    # historical purposes
    # expanded = expand(deepcopy(grid))

    empty_rows, empty_cols = empty(grid)
    print(
        f"Part 1: {all_pairs_shortest_paths(grid, empty_rows, empty_cols, expansion=2)}"
    )
    print(
        f"Part 2: {all_pairs_shortest_paths(grid, empty_rows, empty_cols, expansion=1_000_000)}"
    )


if __name__ == "__main__":
    main()
