import fileinput
from collections import defaultdict


def parse():
    cards = []
    for line in fileinput.input():
        a, b = line.strip().split(":")
        _, id = a.split()
        w, g = b.split(" | ")

        w = {int(n) for n in w.split()}
        g = {int(n) for n in g.split()}
        cards.append((int(id), w, g))
    return cards


def score(cards):
    s = 0
    for _, w, g in cards:
        match = w.intersection(g)
        if match:
            s += pow(2, len(match) - 1)
    return s


def copy(cards):
    cards_by_id = {id: (w, g) for id, w, g in cards}
    copies = defaultdict(int)

    for id, (w, g) in cards_by_id.items():
        n = len(w.intersection(g))
        for i in range(id + 1, id + n + 1):
            copies[i] += 1

    for copy, ncopies in copies.items():
        w, g = cards_by_id[copy]
        n = len(w.intersection(g))
        for i in range(copy + 1, copy + 1 + n):
            copies[i] += ncopies

    return sum(copies.values()) + len(cards)


def main():
    cards = parse()
    print(f"Part 1: {score(cards)}")
    print(f"Part 2: {copy(cards)}")


if __name__ == "__main__":
    main()
