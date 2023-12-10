import fileinput
from itertools import tee


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse():
    records = []
    for line in fileinput.input():
        records.append([int(n) for n in line.strip().split()])
    return records


def generate(history):
    sequences = [history]
    sequence = history
    while not all(v == 0 for v in sequence):
        new_sequence = []
        for a, b in pairwise(sequence):
            new_sequence.append(b - a)
        sequences.append(new_sequence)
        sequence = new_sequence
    return sequences


def predict(history, backwards=False):
    sequences = generate(history)
    for a, b in pairwise(reversed(sequences)):
        if backwards:
            b.insert(0, b[0] - a[0])
        else:
            b.append(a[-1] + b[-1])
    if backwards:
        return sequences[0][0]
    return sequences[0][-1]


def count(records, backwards=False):
    return sum(predict(history, backwards) for history in records)


def main():
    records = parse()
    print(f"Part 1: {count(records)}")
    print(f"Part 2: {count(records, backwards=True)}")


if __name__ == "__main__":
    main()
