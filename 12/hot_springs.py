import fileinput
from collections import deque, Counter
from functools import lru_cache


def parse():
    records = []
    for line in fileinput.input():
        springs, groups = line.strip().split()
        groups = [int(v) for v in groups.split(",")]
        records.append((springs, groups))
    return records


def generate(springs, groups):
    stack = [springs]
    seen = set()
    total = sum(groups)

    possible = set()

    while stack:
        springs = stack.pop()

        if "?" not in springs and sum(1 for char in springs if char == "#") == total:
            possible.add(springs)

        if springs in seen:
            continue

        seen.add(springs)

        for i, s in enumerate(springs):
            if s == "?":
                sps = list(springs)
                a = "".join(sps[:i] + ["."] + sps[i + 1 :])
                b = "".join(sps[:i] + ["#"] + sps[i + 1 :])
                stack.append(a)
                stack.append(b)
                break
    return possible


def is_valid(springs, groups):
    g = []
    c = 0
    for i in range(len(springs)):
        if springs[i] == "#":
            c += 1
        elif springs[i] == "." and c:
            g.append(c)
            c = 0
    if c:
        g.append(c)

    return g == groups


def count(records):
    return sum(arrengements(springs, groups) for springs, groups in records)


def arrengements(springs, groups):
    return sum(is_valid(p, groups) for p in generate(springs, groups))


def count_folded(records, folds=5):
    count = 0
    for springs, groups in records:
        springs = "?".join([springs] * folds)
        groups = tuple(groups * folds)
        count += dp(springs, groups)
    return count


@lru_cache(maxsize=128000)
def dp(springs, groups, i=0, g=0, current=0):
    # exhausted springs
    if i == len(springs):
        # exhausted groups and none left
        if g == len(groups) and current == 0:
            return 1
        # group left to match is equal to currently matching
        elif g == len(groups) - 1 and groups[g] == current:
            return 1
        return 0

    count = 0

    current_springs = [springs[i]]
    if springs[i] == "?":
        # try both possibilities
        current_springs = [".", "#"]
    for spring in current_springs:
        if spring == ".":
            # nothing, keep going
            if current == 0:
                count += dp(springs, groups, i + 1, g, 0)

            # group ended
            elif current > 0 and g < len(groups) and groups[g] == current:
                # match found, reset current, increment i and g
                count += dp(springs, groups, i + 1, g + 1, 0)

        elif spring == "#":
            count += dp(springs, groups, i + 1, g, current + 1)
    return count


def main():
    records = parse()
    # print(f"Part 1: {count(records)}")
    print(f"Part 1: {count_folded(records, folds=1)}")
    print(f"Part 2: {count_folded(records)}")


if __name__ == "__main__":
    main()
