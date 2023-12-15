import fileinput
from collections import defaultdict


class hashmap:
    def __init__(self):
        self.boxes = defaultdict(list)

    def put(self, key, value):
        box = self.hash(key)
        for i, (k, _) in enumerate(self.boxes[box]):
            if key == k:
                self.boxes[box][i] = (key, value)
                break
        else:
            self.boxes[box].append((key, value))

    def remove(self, key):
        box = self.hash(key)
        for i, (k, _) in enumerate(self.boxes[box]):
            if key == k:
                del self.boxes[box][i]

    def items(self):
        return self.boxes.items()

    @staticmethod
    def hash(key):
        res = 0
        for char in key:
            code = ord(char)
            res += code
            res *= 17
            res = res % 256
        return res


def parse():
    line = fileinput.input().readline()
    return line.strip().split(",")


def allocate(string, map):
    if "=" in string:
        key, value = string.split("=")
        map.put(key, int(value))

    elif "-" in string:
        key = string[:-1]
        map.remove(key)
    return


def run(sequence):
    map = hashmap()
    for s in sequence:
        allocate(s, map)
    return map


def power(map):
    S = 0
    for box, lens in map.items():
        for i, (_, value) in enumerate(lens, start=1):
            S += (box + 1) * i * value
    return S


def main():
    sequence = parse()
    print(f"Part 1: {sum(hashmap.hash(s) for s in sequence)}")
    map = run(sequence)
    print(f"Part 2: {power(map)}")


if __name__ == "__main__":
    main()
