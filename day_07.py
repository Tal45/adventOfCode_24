# question & input @ https://adventofcode.com/2024/day/7


def parse_input(file_dir):
    d = {}
    with open(file_dir) as file:
        for line in file:
            idx = line.index(":")
            d[int(line[:idx])] = list(map(int, line[idx+1:].split()))
    return d


def sum_calcs(d):
    total_sum_p1, total_sum_p2 = 0, 0
    for key, value in d.items():
        if recursive_calc(key, value):
            total_sum_p1 += key
        if recursive_calc_expanded(key, value):
            total_sum_p2 += key
    return total_sum_p1, total_sum_p2


def recursive_calc(value, numbers, current=0, idx=0):
    if idx == len(numbers):
        return current == value

    next_num = numbers[idx]
    if current == 0:
        return recursive_calc(value, numbers, next_num, idx + 1)

    return (
            recursive_calc(value, numbers, current + next_num, idx + 1) or
            recursive_calc(value, numbers, current * next_num, idx + 1)
    )


def recursive_calc_expanded(value, numbers, current=0, idx=0):
    if idx == len(numbers):
        return current == value

    next_num = numbers[idx]

    if current == 0:
        return recursive_calc_expanded(value, numbers, next_num, idx + 1)

    concatenated_value = int(str(current) + str(next_num))

    return (
            recursive_calc_expanded(value, numbers, current + next_num, idx + 1) or
            recursive_calc_expanded(value, numbers, current * next_num, idx + 1) or
            recursive_calc_expanded(value, numbers, concatenated_value, idx + 1)
    )


if __name__ == '__main__':
    input_directory = "inputfiles/day7.txt"
    dic = parse_input(input_directory)
    print(sum_calcs(dic))
