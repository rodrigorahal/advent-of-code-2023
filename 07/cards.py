import fileinput
from collections import Counter


card_ranks = {c: i for i, c in enumerate(reversed("AKQJT98765432"))}


def parse():
    hands = []
    for line in fileinput.input():
        hand, bid = line.strip().split()
        hands.append((hand, int(bid)))
    return hands


def get_type(hand, with_joker=False):
    counter = Counter(hand)

    if with_joker and "J" in counter:
        j = counter.pop("J")
        if not counter:
            counter["J"] += j
        else:
            (card, _), *_ = counter.most_common(1)
            counter[card] += j

    if len(counter) == 1:
        # five of a kind
        return 7
    elif len(counter) == 2:
        (_, c), *_ = counter.most_common(1)
        if c == 4:
            # four of a kind
            return 6
        # full house
        return 5
    elif len(counter) == 3:
        (_, c), *_ = counter.most_common(1)
        if c == 3:
            # three of a kind
            return 4
        # two pairs
        return 3
    elif len(counter) == 4:
        # one pair
        return 2
    # high card
    return 1


def key_compare(hand, with_joker=False):
    hand, _ = hand
    return get_type(hand, with_joker), tuple(card_ranks[c] for c in hand)


def play(hands, with_joker=False):
    if with_joker:
        card_ranks["J"] = -1
    return sorted(hands, key=lambda h: key_compare(h, with_joker))


def winnings(ranked):
    return sum(i * bid for i, (_, bid) in enumerate(ranked, start=1))


def main():
    hands = parse()

    ranked = play(hands)
    print(f"Part 1: {winnings(ranked)}")

    ranked = play(hands, with_joker=True)
    print(f"Part 2: {winnings(ranked)}")


if __name__ == "__main__":
    main()
