import fileinput
import networkx as nx
from collections import defaultdict


def parse():
    V = set()
    E = set()
    G = defaultdict(set)
    for line in fileinput.input():
        left, right = line.strip().split(": ")
        right = right.strip().split()
        V.add(left)
        for r in right:
            V.add(r)
            G[left].add(r)
            G[r].add(left)
            E.add((left, r))
            E.add((r, left))

    return G, V, E


def solve(G):
    g = nx.DiGraph()

    for k, vs in G.items():
        for v in vs:
            g.add_edge(k, v, capacity=1.0)
            g.add_edge(v, k, capacity=1.0)

    source = list(G.keys())[0]
    sink = list(G.keys())[-1]
    cut, (L, R) = nx.minimum_cut(g, source, sink)
    assert cut == 3
    return len(L) * len(R)


def main():
    G, V, E = parse()
    size = solve(G)
    print(f"Part 1: {size}")


if __name__ == "__main__":
    main()
