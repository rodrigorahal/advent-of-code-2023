import fileinput
from collections import deque, defaultdict


def parse():
    grid = []
    start, target = None, None
    for line in fileinput.input():
        grid.append(line.strip())

    for col, char in enumerate(grid[0]):
        if char == ".":
            start = (0, col)

    for col, char in enumerate(grid[-1]):
        if char == ".":
            target = (len(grid) - 1, col)
    return grid, (start), target


def display(grid):
    for row in grid:
        print(row)
    print()


def neighbors_with_slope(grid, row, col, place):
    H, W = len(grid), len(grid[0])
    res = []

    if place == ">":
        nr, nc = row, col + 1
        if 0 <= nr < H and 0 <= nc < W:
            res.append((nr, nc))
    elif place == "^":
        nr, nc = row - 1, col
        if 0 <= nr < H and 0 <= nc < W:
            res.append((nr, nc))
    elif place == "v":
        nr, nc = row + 1, col
        if 0 <= nr < H and 0 <= nc < W:
            res.append((nr, nc))
    elif place == "<":
        nr, nc = row, col - 1
        if 0 <= nr < H and 0 <= nc < W:
            res.append((nr, nc))
    else:
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if 0 <= row + dr < H and 0 <= col + dc < W:
                res.append((row + dr, col + dc))
    return res


def neighbors(grid, row, col):
    H, W = len(grid), len(grid[0])
    res = []
    for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if 0 <= row + dr < H and 0 <= col + dc < W:
            res.append((row + dr, col + dc))
    return res


def search(grid, start, target):
    max_path = float("-inf")
    queue = deque([(start, set(), 0)])

    while queue:
        (row, col), seen, path = queue.pop()

        if (row, col) in seen:
            continue

        if (row, col) == target:
            max_path = max(max_path, path)
            continue

        for nr, nc in neighbors_with_slope(grid, row, col, grid[row][col]):
            if grid[nr][nc] in (".", ">", "<", "v", "^") and (nr, nc) not in seen:
                queue.append(((nr, nc), {*seen, (row, col)}, path + 1))
    return max_path


def pre_process(grid, start, target):
    H, W = len(grid), len(grid[0])

    V = set()
    for row in range(H):
        for col in range(W):
            if grid[row][col] != "#":
                ns = neighbors(grid, row, col)
                ns = [(nr, nc) for (nr, nc) in ns if grid[nr][nc] != "#"]
                if len(ns) > 2:
                    V.add((row, col))
    V.add(start)
    V.add(target)

    processed = defaultdict(list)

    for ROW, COL in V:
        queue = deque([(ROW, COL, 0)])
        seen = set()
        while queue:
            (row, col, w) = queue.pop()
            if (row, col) in seen:
                continue
            seen.add((row, col))

            if (row, col) in V and (row, col) != (ROW, COL):
                processed[(ROW, COL)].append((w, row, col))
                continue

            for nr, nc in neighbors(grid, row, col):
                if (nr, nc) in seen or grid[nr][nc] == "#":
                    continue
                queue.append((nr, nc, w + 1))
    return processed


def search_processed(processed, start, target):
    max_path = float("-inf")
    queue = deque([(start, {}, 0)])

    while queue:
        (row, col), seen, path = queue.pop()

        if (row, col) in seen:
            continue

        if (row, col) == target:
            max_path = max(max_path, path)
            continue

        for w, nr, nc in processed[(row, col)]:
            queue.append(((nr, nc), {*seen, (row, col)}, path + w))
    return max_path


def main():
    grid, start, target = parse()
    # display(grid)
    max_path = search(grid, start, target)
    print(f"Part 1: {max_path}")

    processed = pre_process(grid, start, target)
    max_path = search_processed(processed, start, target)
    print(f"Part 2: {max_path}")


if __name__ == "__main__":
    main()
