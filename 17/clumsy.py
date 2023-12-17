import fileinput
import heapq


def parse():
    grid = []
    for line in fileinput.input():
        grid.append(line.strip())
    return grid


def display(grid, path=()):
    for row, v in enumerate(grid):
        line = ["#" if (row, col) in path else v_ for col, v_ in enumerate(v)]
        print("".join(line))
    print()


def dijkstra(grid, min_blocks=0, max_blocks=3):
    H, W = len(grid), len(grid[0])

    queue = []
    (cost, start, blocks, dirs, path) = (0, (0, 0), 1, (0, 1), ((0, 0),))
    heapq.heappush(queue, (cost, start, blocks, dirs, path))

    seen = set()

    while queue:
        cost, (row, col), blocks, (dr, dc), path = heapq.heappop(queue)

        if (row, col, dr, dc, blocks) in seen:
            continue

        seen.add((row, col, dr, dc, blocks))

        if (row, col) == (H - 1, W - 1) and blocks >= min_blocks:
            return cost, path

        for ndr, ndc in [(dr, dc), (-dc, -dr), (dc, dr)]:
            nrow, ncol = row + ndr, col + ndc

            if not (0 <= nrow < H and 0 <= ncol < W):
                continue

            if min_blocks and (dr, dc) != (ndr, ndc) and blocks < min_blocks:
                continue

            if (dr, dc) == (ndr, ndc) and blocks == max_blocks:
                continue

            nblocks = blocks + 1 if (dr, dc) == (ndr, ndc) else 1

            ncost = cost + int(grid[nrow][ncol])

            heapq.heappush(
                queue,
                (ncost, (nrow, ncol), nblocks, (ndr, ndc), path + ((nrow, ncol),)),
            )


def main():
    grid = parse()
    H, W = len(grid), len(grid[0])

    w, path = dijkstra(grid, min_blocks=0, max_blocks=3)
    print(f"Part 1: {w}")

    w, path = dijkstra(grid, min_blocks=4, max_blocks=10)
    print(f"Part 2: {w}")


if __name__ == "__main__":
    main()
