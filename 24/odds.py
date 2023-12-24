import fileinput
from z3 import Int, Solver


def parse():
    stones = []
    for line in fileinput.input():
        stone = [int(v) for v in line.strip().replace(" @ ", ", ").split(", ")]
        stones.append(stone)
    return stones


def intersect(a, b):
    """
    https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
    """
    a_px, a_py, a_pz, a_vx, a_vy, a_vz = a
    b_px, b_py, b_pz, b_vx, b_vy, b_vz = b

    x1 = a_px
    x2 = x1 + a_vx
    y1 = a_py
    y2 = y1 + a_vy

    x3 = b_px
    x4 = x3 + b_vx
    y3 = b_py
    y4 = y3 + b_vy

    try:
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
            (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        )
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
            (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        )
    except ZeroDivisionError:
        return None

    if px == 0 or py == 0:
        return None
    return px, py


def time_at_position(a, x, y):
    a_px, a_py, a_pz, a_vx, a_vy, a_vz = a
    t = (x - a_px) / a_vx
    return t


def count(stones, minp, maxp):
    C = 0

    for i, a in enumerate(stones):
        for b in stones[i + 1 :]:
            inter = intersect(a, b)

            if not inter:
                continue

            px, py = inter
            ta = time_at_position(a, px, py)
            tb = time_at_position(b, px, py)

            if minp <= px <= maxp and minp <= py <= maxp and ta >= 0 and tb >= 0:
                C += 1
    return C


def solve(stones):
    n = len(stones)
    x, y, z, vx, vy, vz = Int("x"), Int("y"), Int("z"), Int("vx"), Int("vy"), Int("vz")
    T = [Int(f"T{i}") for i in range(n)]

    solver = Solver()
    for i, stone in enumerate(stones):
        xi, yi, zi, vxi, vyi, vzi = stone
        solver.add((x + T[i] * vx) - (xi + T[i] * vxi) == 0)
        solver.add((y + T[i] * vy) - (yi + T[i] * vyi) == 0)
        solver.add((z + T[i] * vz) - (zi + T[i] * vzi) == 0)
    solver.check()

    M = solver.model()
    return M.eval(x + y + z)


def main():
    stones = parse()

    print(f"Part 1: {count(stones, 200000000000000, 400000000000000)}")
    print(f"Part 2: {solve(stones)}")


if __name__ == "__main__":
    main()
