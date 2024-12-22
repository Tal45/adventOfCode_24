# input & question can be found @ https://adventofcode.com/2024/day/22

from functools import cache
from collections import defaultdict
import time


def parse_input(inp_dir):
    nums = []
    with open(inp_dir, "r") as file:
        for line in file:
            if line:
                nums.append(int(line.rstrip()))

    return nums


def calculate_sn(sn, days=2000):
    for _ in range(days):
        res = sn * 64
        sn = mix(sn, res)
        sn = prune(sn)

        res = sn // 32
        sn = mix(sn, res)
        sn = prune(sn)

        res = sn * 2048
        sn = mix(sn, res)
        sn = prune(sn)

    return sn


@cache
def mix(res, sn):
    return res ^ sn


@cache
def prune(sn):
    return sn % 16777216


def get_total_sn(inp_dir):
    s_nums = parse_input(inp_dir)
    total_sn = 0

    for sn in s_nums:
        total_sn += calculate_sn(sn)

    return total_sn


def get_most_bananas(inp_dir):
    s_nums = parse_input(inp_dir)
    total_sales = defaultdict(int)

    for sn in s_nums:
        current_seq = [0] * 2000
        current_price = sn % 10
        sales = {}

        for i in range(2000):
            sn = calculate_sn(sn, 1)
            new_price = sn % 10
            delta = new_price - current_price

            current_seq[i] = delta
            if i >= 3:
                seq = tuple(current_seq[i - 3:i + 1])
                if seq not in sales:
                    sales[seq] = new_price

            current_price = new_price

        for seq, bananas in sales.items():
            total_sales[seq] += bananas

    return max(total_sales.values())


if __name__ == '__main__':
    curr_time = time.time()
    inp_directory = "inputfiles/day22.txt"
    print(get_total_sn(inp_directory))
    print(get_most_bananas(inp_directory))
    print('----- Program executed in %s seconds -----' % round(time.time() - curr_time, 2))
