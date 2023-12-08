import fileinput
import math
from collections import defaultdict
from itertools import cycle


def parse():
    tree = defaultdict(list)
    with open("08/input.txt") as f:
        blocks = f.read().split("\n\n")
        cmds, maze = blocks

        for line in maze.split("\n"):
            source, dests = line.strip().split(" = ")
            left, right = dests.strip("(").strip(")").split(", ")
            tree[source].extend([left, right])
        return cmds, tree


def follow(cmds, tree, start="AAA", pattern="ZZZ"):
    steps = 0
    curr = start
    for cmd in cycle(cmds):
        left, right = tree[curr]
        curr = right if cmd == "R" else left
        steps += 1
        if curr.endswith(pattern):
            return steps


def start_at(tree):
    return [node for node in tree if node.endswith("A")]


def follow_as_ghost(cmds, tree):
    nodes = start_at(tree)
    steps = []
    for node in nodes:
        steps.append(follow(cmds, tree, start=node, pattern="Z"))
    return steps


def main():
    cmds, tree = parse()
    steps = follow(cmds, tree)
    print(f"Part 1: {steps}")

    steps = follow_as_ghost(cmds, tree)
    print(f"Part 2: {math.lcm(*steps)}")


if __name__ == "__main__":
    main()
