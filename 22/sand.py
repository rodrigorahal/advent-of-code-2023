import fileinput
from copy import deepcopy
from collections import defaultdict, deque

NAMES = "ABCDEFG"


def parse(with_names=False):
    bricks = []
    for i, line in enumerate(fileinput.input()):
        left, right = line.strip().split("~")
        left = tuple([int(n) for n in left.split(",")])
        right = tuple([int(n) for n in right.split(",")])

        if left[2] > right[2]:
            left, right = right, left

        if with_names:
            bricks.append((left, right, NAMES[i]))
        else:
            bricks.append((left, right, str(i)))
    return bricks


def is_supported(a, b):
    # is a supported by b?
    """
    a = 0,0,2~2,0,2
    b = 1,0,1~1,2,1

    x,y (0,0) => (2,0)
        (1,0) => (1,2)
    """
    (a0x, a0y, a0z), (a1x, a1y, a1z) = a
    (b0x, b0y, b0z), (b1x, b1y, b1z) = b

    cx = intersect((a0x, a1x), (b0x, b1x))
    cy = intersect((a0y, a1y), (b0y, b1y))

    if (cx and cy) and max(b0z, b1z) == min(a0z, a1z) - 1:
        return True
    return False


def intersect(a, b):
    a_start, a_end = a
    b_start, b_end = b

    if b_start > a_end or a_start > b_end:
        return None

    i_start = max(a_start, b_start)
    i_end = min(a_end, b_end)

    return (i_start, i_end)


def settle(bricks):
    moved = True

    while moved:
        moved = False
        for i, brick in enumerate(bricks):
            (start, end, name) = brick
            brick = (start, end)

            for j, supporting_brick in enumerate(bricks):
                # print(f"\t {supporting_brick=}")
                if i == j:
                    continue

                start, end, supporting_name = supporting_brick
                supporting_brick = (start, end)

                if is_supported(brick, supporting_brick):
                    break
            else:
                # print(f"else {brick=}")
                (b0x, b0y, b0z), (b1x, b1y, b1z) = brick
                if min(b0z, b1z) == 1:  # ground
                    pass
                else:
                    bricks[i] = ((b0x, b0y, b0z - 1), (b1x, b1y, b1z - 1), name)
                    moved = True
    return bricks


def examine(blocks):
    supported_by = defaultdict(set)
    supports = defaultdict(set)

    for i, a in enumerate(blocks):
        start, end, a_name = a
        a_stripped = (start, end)

        for j, b in enumerate(blocks):
            if i == j:
                continue

            start, end, b_name = b
            b_stripped = (start, end)

            if is_supported(a_stripped, b_stripped):
                supported_by[a].add(b)
                supports[b].add(a)

    can_not_disintegrate = set()
    for block, sps in supported_by.items():
        if len(sps) == 1:
            (a,) = sps
            can_not_disintegrate.add(a)

    return len(blocks) - len(can_not_disintegrate), supported_by, supports


def search(supported_by, supports, block):
    count = 0
    queue = deque([(block)])

    seen = set()

    while queue:
        block = queue.popleft()

        # print(f"{block=}, {supports[block]=}")

        if block in seen:
            continue

        seen.add(block)

        for supported in supports[block]:
            # print(f"\t {supported=}")
            supported_by[supported].discard(block)
            if len(supported_by[supported]) == 0:
                queue.append((supported))
                count += 1
    return count


def main():
    bricks = parse(with_names=False)

    settled = settle(deepcopy(bricks))

    safe_to_disintegrate, supported_by, supports = examine(settled)

    # for (_, _, k), v in supported_by.items():
    #     print(f"{k} is supported by {[n for (_,_, n) in v]}")

    # for (_, _, k), v in supports.items():
    #     print(f"{k} supports {[n for (_,_ , n) in v]}")

    print(f"Part 1: {safe_to_disintegrate}")

    # C = search(deepcopy(supported_by), deepcopy(supports), settled[0])
    # print(C)
    R = 0
    for block in settled:
        C = search(
            deepcopy(
                supported_by,
            ),
            deepcopy(supports),
            block,
        )
        R += C
    print(f"Part 2: {R}")


if __name__ == "__main__":
    main()
