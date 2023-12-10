import fileinput
from copy import deepcopy
import sys

sys.setrecursionlimit(100000)


CONNECTIONS = {
    "|": {
        (-1, 0): ["|", "7", "F"],
        (1, 0): ["|", "L", "J"],
    },
    "-": {
        (0, -1): ["-", "L", "F"],
        (0, 1): ["-", "J", "7"],
    },
    "L": {
        (-1, 0): ["|", "7", "F"],
        (0, 1): ["-", "J", "7"],
    },
    "J": {
        (-1, 0): ["|", "7", "F"],
        (0, -1): ["-", "L", "F"],
    },
    "7": {
        (1, 0): ["|", "L", "J"],
        (0, -1): ["-", "L", "F"],
    },
    "F": {
        (1, 0): ["|", "L", "J"],
        (0, 1): ["-", "J", "7"],
    },
}


def neighbours(grid, row, col):
    H, W = len(grid), len(grid[0])
    pipe = grid[row][col]
    ns = []
    for dr, dc in CONNECTIONS[pipe]:
        if 0 <= (row + dr) < H and 0 <= (col + dc) < W:
            if grid[row + dr][col + dc] in CONNECTIONS[pipe][(dr, dc)]:
                ns.append((row + dr, col + dc))
    return ns


def parse():
    grid = []
    start = None

    row = 0
    for line in fileinput.input():
        pipes = line.strip()
        grid.append(pipes)
        for col, char in enumerate(pipes):
            if char == "S":
                start = (row, col)
        row += 1
    return grid, start


def display(grid, cycle):
    for row, values in enumerate(grid):
        line = "".join(
            [char if (row, col) in cycle else " " for col, char in enumerate(values)]
        )
        print(line)


def dfs(grid, start, parent=None, finished=None, seen=None, path=None):
    if not finished:
        finished = set()
    if not seen:
        seen = {}
    if not path:
        path = []

    row, col = start
    if (row, col) in finished:
        return False, path

    if (row, col) in seen:
        return True, path

    seen[(row, col)] = True
    path.append((row, col))
    for nrow, ncol in neighbours(grid, row, col):
        if grid[nrow][col] == ".":
            continue
        if (nrow, ncol) == parent:
            continue
        found, path = dfs(grid, (nrow, ncol), (row, col), finished, seen, path)
        if found:
            return found, path
    # finished[(row, col)] = True
    finished.add((row, col))
    return False, path


def find(grid, start):
    row, col = start
    for pipe in CONNECTIONS:
        G = deepcopy(grid)
        G[row] = G[row].replace("S", pipe)
        has_cycle, path = dfs(G, start)
        if has_cycle:
            return path


def generate_edges(cycle):
    edges = set()
    edges.add((cycle[-1], cycle[0]))
    for a, b in zip(cycle, cycle[1::]):
        edges.add((a, b))
    return edges


def crossings(edges, row, col):
    return sum(has_crossing(edge, row, col) for edge in edges)


def has_crossing(edge, row, col):
    a, b = edge
    (arow, _), (brow, _) = a, b

    if arow > brow:
        a, b = b, a
    (arow, acol), (brow, bcol) = a, b

    if arow == brow:
        # dont consider horizontal edges
        return False
    elif acol == bcol:
        return arow <= row < brow and col <= acol


# https://en.wikipedia.org/wiki/Point_in_polygon
def ray_casting(grid, cycle):
    inside = 0
    # could do interval merging; but why bother?
    edges = generate_edges(cycle)
    for row, tiles in enumerate(grid):
        for col, _ in enumerate(tiles):
            if (row, col) in cycle:
                continue
            count = crossings(edges, row, col)
            if count % 2 == 1:
                inside += 1
    return inside


def main():
    grid, start = parse()

    cycle = find(grid, start)
    print(f"Part 1: {len(cycle) // 2}")
    # display(grid, cycle)
    inside = ray_casting(grid, cycle)
    print(f"Part 2: {inside}")


if __name__ == "__main__":
    main()
