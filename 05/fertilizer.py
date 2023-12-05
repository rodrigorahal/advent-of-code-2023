import fileinput
from concurrent.futures import ProcessPoolExecutor, as_completed


def parse():
    seeds = []
    maps = []
    m = []
    for line in fileinput.input():
        if line.startswith("seeds"):
            _, ss = line.strip().split(": ")
            for s in ss.split():
                seeds.append(int(s))
        elif line == "\n":
            if m:
                maps.append(m)
                m = []
            continue
        elif line[0].isdigit():
            dest, source, range_ = line.strip().split()
            dest, source, range_ = int(dest), int(source), int(range_)
            m.append((dest, source, range_))
        elif not line[0].isdigit():
            continue
    if m:
        maps.append(m)
    return seeds, maps


def find(seeds, maps):
    minloc = float("+inf")
    for seed in seeds:
        next = seed
        for ranges in maps:
            next = match(next, ranges)
        minloc = min(minloc, next)
    return minloc


def match(value, ranges):
    for dest, source, range_ in ranges:
        if source <= value < source + range_:
            return (value - source) + dest
    return value


def find_ranges(seeds, maps):
    pairs = list(zip(seeds[::2], seeds[1::2]))
    minloc = float("+inf")
    for st, r in pairs:
        input_ranges = [(st, st + r)]
        matching_ranges = input_ranges
        for ranges in maps:
            matching_ranges = match_ranges(matching_ranges, ranges)
        minloc = min(minloc, min(matching_ranges)[0])
    return minloc


def match_ranges(input_ranges, ranges):
    # [ast                                             aed)
    #                   [bst           bed)
    #
    # [LEFT            ][INTERSECTION     ][RIGHT         )

    matched = []
    to_match_ranges = input_ranges
    for dest, source, range_ in ranges:
        new_to_match_ranges = []
        while to_match_ranges:
            ast, aed = to_match_ranges.pop()
            bst, bed = source, source + range_

            left = ast, min(aed, bst)
            intersection = max(ast, bst), min(aed, bed)
            right = max(ast, bed), aed

            lst, led = left
            if led > lst:
                new_to_match_ranges.append(left)
            ist, ied = intersection
            if ied > ist:
                matched.append(
                    (intersection[0] - source + dest, intersection[1] - source + dest)
                )
            rst, red = right
            if red > rst:
                new_to_match_ranges.append(right)
        to_match_ranges = new_to_match_ranges
    return matched + to_match_ranges


def main():
    seeds, maps = parse()
    print(f"Part 1: {find(seeds, maps)}")
    print(f"Part 2: {find_ranges(seeds, maps)}")


if __name__ == "__main__":
    main()
