import re
import numpy as np


def parse_input(dir):
    with open(dir, "r") as file:
        inp = file.read()

    games = inp.strip().split("\n\n")

    l = []
    for game in games:
        pattern = r"[-\d]+"
        numbers = list(map(int, re.findall(pattern, game)))

        a = (numbers[0], numbers[1])
        b = (numbers[2], numbers[3])
        prize = (numbers[4], numbers[5])

        l.append((a, b, prize))

    return l


def find_winning_pattern(game, curr_x=0, curr_y=0, tokens=0, a_lim=0, b_lim=0, memo=None):
    if memo is None:
        memo = {}

    a, b, prize = game

    if (curr_x, curr_y) in memo:
        return memo[(curr_x, curr_y)]

    if curr_x > prize[0] or curr_y > prize[1]:
        return float('inf')

    if a_lim > 100 or b_lim > 100:
        return float('inf')

    if curr_x == prize[0] and curr_y == prize[1]:
        return tokens

    use_a = find_winning_pattern(game, curr_x + a[0], curr_y + a[1], tokens + 3, a_lim + 1, b_lim, memo)
    use_b = find_winning_pattern(game, curr_x + b[0], curr_y + b[1], tokens + 1, a_lim, b_lim + 1, memo)

    memo[(curr_x, curr_y)] = min(use_a, use_b)
    return memo[(curr_x, curr_y)]


def solve_equation_systems(game):
    a, b, prize = game
    a_mat = np.array([
        [a[0], b[0]],
        [a[1], b[1]]
    ])
    b_vec = np.array([prize[0], prize[1]])

    solution = np.linalg.solve(a_mat, b_vec)

    if is_almost_integer(solution[0]) and is_almost_integer(solution[1]):
        return int(np.round(solution[0]) * 3 + np.round(solution[1]))
    else:
        return 0


def is_almost_integer(num, tolerance=1e-3):
    return abs(num - round(num)) < tolerance


if __name__ == "__main__":
    input_dir = "inputfiles/day13.txt"
    games = parse_input(input_dir)
    total_tokens_part1 = 0
    total_tokens_part2 = 0
    for game in games:
        tokens_per_game = find_winning_pattern(game)
        if tokens_per_game != float('inf'):
            total_tokens_part1 += tokens_per_game
        game2 = (game[0], game[1], (game[2][0] + 10000000000000, game[2][1] + 10000000000000))
        total_tokens_part2 += solve_equation_systems(game2)

    print(total_tokens_part1, total_tokens_part2)