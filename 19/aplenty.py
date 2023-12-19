from collections import defaultdict, deque

EVAL = {
    ">": lambda a, b: a > b,
    "<": lambda a, b: b > a,
}


def parse():
    workflows = defaultdict(list)
    parts = []
    with open("19/input.txt") as f:
        blocks = f.read().split("\n\n")

        for line in blocks[0].split("\n"):
            name, rules = line.removesuffix("}").split("{")
            for rule in rules.split(","):
                if ":" in rule:
                    conds, dest = rule.split(":")
                    if ">" in conds:
                        op = ">"
                        attr, value = conds.split(">")
                    elif "<" in conds:
                        op = "<"
                        attr, value = conds.split("<")
                    workflows[name].append((attr, op, int(value), dest))
                else:
                    workflows[name].append(rule)

        for line in blocks[1].split("\n"):
            part = {}
            attrs = line.strip().removeprefix("{").removesuffix("}").split(",")
            for attr in attrs:
                key, value = attr.split("=")
                part[key] = int(value)
            parts.append(part)
    return workflows, parts


def step(part, workflows, start="in"):
    curr = start

    while curr not in "AR":
        for rule in workflows[curr]:
            if isinstance(rule, tuple):
                attr, op, value, dest = rule

                if EVAL[op](part[attr], value):
                    curr = dest
                    break
            else:
                curr = rule
                break
    return curr


def run(parts, workflows):
    A = []
    for part in parts:
        final = step(part, workflows)
        if final == "A":
            A.append(part)
    return A


def score(A):
    S = 0
    for part in A:
        v = part.values()
        S += sum(v)
    return S


def search(workflows, start="in"):
    paths = []
    queue = deque([(start, [start], [])])

    while queue:
        curr, path, rules = queue.popleft()

        if curr == "A":
            paths.append((path, rules))
            continue

        for i, rule in enumerate(workflows[curr]):
            if isinstance(rule, tuple):
                attr, op, value, dest = rule
                if dest != "R":
                    queue.append((dest, path + [dest], rules + [i]))
            else:
                dest = rule
                if dest != "R":
                    queue.append((dest, path + [dest], rules + [i]))
    return paths


def combinations(workflows, path, rules):
    limits = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}

    for name, r in zip(path, rules):
        workflow = workflows[name]
        # rules that need to eval to false
        for i in range(r):
            rule = workflow[i]
            if isinstance(rule, str):
                continue
            attr, op, value, dest = rule
            if op == "<":
                limits[attr][0] = max(limits[attr][0], value)
            elif op == ">":
                limits[attr][1] = min(limits[attr][1], value)

        # rule that needs to eval to true
        rule = workflow[r]
        if isinstance(rule, tuple):
            attr, op, value, dest = rule
            if op == "<":
                limits[attr][1] = min(limits[attr][1], value - 1)
            if op == ">":
                limits[attr][0] = max(limits[attr][0], value + 1)

    n = 1
    for min_value, max_value in limits.values():
        n *= max_value - min_value + 1
    return n


def main():
    workflows, parts = parse()

    accepted = run(parts, workflows)
    print(f"Part 1: {score(accepted)}")
    paths = search(workflows)
    print(
        f"Part 2: {sum(combinations(workflows, path, rules) for (path, rules) in paths)}"
    )


if __name__ == "__main__":
    main()
