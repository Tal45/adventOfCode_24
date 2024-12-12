# question & input can be found @ https://adventofcode.com/2024/day/11
from collections import Counter


def parse_input(dir):
    with open(dir, "r") as file:
        line = file.read()
    return list(map(int, line.split()))


def count_stones_after_blinks(stones, blinks):
    curr_counts = Counter(stones)
    transformations = {}

    for _ in range(blinks):
        next_counts = Counter()

        for val, count in curr_counts.items():
            if val in transformations:
                new_stones = transformations[val]

            else:
                if val == 0:
                    new_stones = [1]

                elif len(str(val)) % 2 == 0:
                    num_str = str(val)
                    mid = len(num_str) // 2
                    new_stones = [int(num_str[:mid]), int(num_str[mid:])]

                else:
                    new_stones = [val * 2024]

            transformations[val] = new_stones

            for stone in new_stones:
                next_counts[stone] += count

        curr_counts = next_counts

    return sum(curr_counts.values())


if __name__ == "__main__":

    input_directory = "inputfiles/day11.txt"
    stones = parse_input(input_directory)
    print(count_stones_after_blinks(stones, 25))
    print(count_stones_after_blinks(stones, 75))


