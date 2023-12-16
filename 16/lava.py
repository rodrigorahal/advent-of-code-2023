import fileinput


REFLECT = {
    ".": lambda dr, dc: [(dr, dc)],
    "/": lambda dr, dc: [(-dc, -dr)],
    "\\": lambda dr, dc: [(dc, dr)],
    "|": lambda dr, dc: [(dr, dc)] if dr else [(1, 0), (-1, 0)],
    "-": lambda dr, dc: [(dr, dc)] if dc else [(0, 1), (0, -1)],
}


def parse():
    grid = []
    for line in fileinput.input():
        grid.append(line.strip())
    return grid


def display(grid, energized):
    for row, values in enumerate(grid):
        line = ["#" if (row, col) in energized else v for col, v in enumerate(values)]
        print("".join(line))
    print()


def deflect(grid, row, col, dr, dc):
    mirror = grid[row][col]
    return REFLECT[mirror](*(dr, dc))


def search(grid, start=(0, 0), dir=(0, 1)):
    H, W = len(grid), len(grid[0])

    for dr, dc in deflect(grid, *start, *dir):
        stack = [(start, (dr, dc))]

    energized = set()
    seen = set()

    while stack:
        (row, col), (dr, dc) = stack.pop()

        if (row, col, dr, dc) in seen:
            continue

        seen.add((row, col, dr, dc))
        energized.add((row, col))

        nrow, ncol = (row + dr, col + dc)

        if not ((0 <= nrow < H) and (0 <= ncol < W)):
            continue

        for ndr, ndc in deflect(grid, nrow, ncol, dr, dc):
            stack.append(((nrow, ncol), (ndr, ndc)))

    return len(energized)


def find(grid):
    H, W = len(grid), len(grid[0])
    max_energized = 0

    for row, dr in [(0, 1), (H - 1, -1)]:
        for col in range(W):
            energized = search(grid, (row, col), dir=(dr, 0))
            max_energized = max(max_energized, energized)

    for col, dc in [(0, 1), (W - 1, -1)]:
        for row in range(H):
            energized = search(grid, (row, col), dir=(0, dc))
            max_energized = max(max_energized, energized)

    return max_energized


def main():
    grid = parse()
    energized = search(grid)
    print(f"Part 1: {energized}")
    print(f"Part 2: {find(grid)}")


if __name__ == "__main__":
    main()
