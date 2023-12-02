import fileinput

NUMS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def parse():
    return [line.strip() for line in fileinput.input()]


def digits(words):
    return [[char for char in word if char.isdigit()] for word in words]


def count(digits):
    return sum(int(d[0] + d[-1]) for d in digits)


def digits_with_cursive(words):
    digits = []
    for word in words:
        word_digits = []
        for i, char in enumerate(word):
            for j, num in enumerate(NUMS):
                if word[i:].startswith(num):
                    word_digits.append(str(j + 1))
            if char.isdigit():
                word_digits.append(char)
        digits.append(word_digits)
    return digits


def main():
    words = parse()
    print(f"Part 1: {count(digits(words))}")
    print(f"Part 2: {count(digits_with_cursive(words))}")


if __name__ == "__main__":
    main()
