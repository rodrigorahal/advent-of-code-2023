import fileinput
from copy import deepcopy


def parse():
    patterns = []
    with open("13/input.txt") as f:
        blocks = f.read().split("\n\n")
        for block in blocks:
            pattern = [line.strip() for line in block.split("\n")]
            patterns.append(pattern)
    return patterns


def display(pattern):
    for line in pattern:
        print(line)
    print()


def find(pattern, prev=None):
    for row in range(len(pattern) - 1):
        if pattern[row] == pattern[row + 1]:
            found = is_mirror(pattern, row, row + 1)
            if found and prev and row + 1 == prev:
                continue
            elif found:
                return row + 1
    return None


def is_mirror(pattern, up, down):
    H = len(pattern)
    while 0 <= up and down < H:
        if pattern[down] != pattern[up]:
            return False
        down += 1
        up -= 1
    return True


def count(patterns):
    C = 0
    for pattern in patterns:
        row = find(pattern)
        col = find(list(zip(*pattern)))
        if row:
            C += 100 * row
        elif col:
            C += col
    return C


def toggle(value):
    return "#" if value == "." else "."


def generate(pattern):
    generated = []
    for row, values in enumerate(pattern):
        for col, value in enumerate(values):
            v = toggle(value)
            p = deepcopy(pattern)
            p[row] = p[row][:col] + v + p[row][col + 1 :]
            generated.append(p)
    return generated


def find_with_smudge(pattern):
    prev_row = find(pattern)
    prev_col = find(list(zip(*pattern)))

    for p in generate(pattern):
        row = find(p, prev=prev_row)
        col = find(list(zip(*p)), prev=prev_col)

        if row and row != prev_row:
            return 100 * row

        if col and col != prev_col:
            return col
    return None


def count_with_smudge(patterns):
    return sum(find_with_smudge(pattern) for pattern in patterns)


def main():
    patterns = parse()
    print(f"Part 1: {count(patterns)}")
    print(f"Part 2: {count_with_smudge(patterns)}")


if __name__ == "__main__":
    main()
