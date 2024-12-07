# question and input @ https://adventofcode.com/2024/day/6

from copy import deepcopy


def parse_input(input_dir):
    map = []
    with open(input_dir, "r") as file:
        for line in file:
            map.append(list(line.rstrip()))
    return map


direction_map = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def locate_guard(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == '^':
                return [i, j], 0
            elif mat[i][j] == '>':
                return [i, j], 1
            elif mat[i][j] == 'v':
                return [i, j], 2
            elif mat[i][j] == '<':
                return [i, j], 3
    return (0, 0), 0


def count_distinct_positions(grid):
    count = 0
    cords, direction = locate_guard(grid)
    row_len = len(grid) - 1
    col_len = len(grid[0]) - 1
    visited = [[False for _ in range(col_len + 1)] for _ in range(row_len + 1)]

    grid[cords[0]][cords[1]] = '.'

    while 0 <= cords[0] <= row_len and 0 <= cords[1] <= col_len:
        visited[cords[0]][cords[1]] = True
        next_step = (cords[0] + direction_map[direction][0], cords[1] + direction_map[direction][1])

        if (
                0 <= next_step[0] <= row_len and 0 <= next_step[1] <= col_len
                and grid[next_step[0]][next_step[1]] == '#'
                ):

            direction = (direction + 1) % 4

        else:
            cords[0], cords[1] = next_step[0], next_step[1]
            if (
                    0 <= next_step[0] <= row_len and 0 <= next_step[1] <= col_len
                    and not visited[next_step[0]][next_step[1]]
                    ):
                count += 1

    return count + 1


def count_possible_new_obstacles(grid):
    res = 0

    start_cords, start_dir = locate_guard(grid)
    cords, dir = start_cords, start_dir

    while 0 <= cords[0] < len(grid) and 0 <= cords[1] < len(grid[0]):
        grid[cords[0]][cords[1]] = 'X'
        next_cords = (cords[0] + direction_map[dir][0], cords[1] + direction_map[dir][1])

        while (
            0 <= next_cords[0] < len(grid) and 0 <= next_cords[1] < len(grid[0])
            and grid[next_cords[0]][next_cords[1]] == '#'
                ):

            dir = (dir + 1) % 4
            next_cords = [cords[0] + direction_map[dir][0], cords[1] + direction_map[dir][1]]

        cords = next_cords

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'X' and not (i == start_cords[0] and j == start_cords[1]):
                grid[i][j] = '#'
                if is_loop(grid, start_cords, start_dir):
                    res += 1
                grid[i][j] = 'X'

    return str(res)


def is_loop(mat, cords, dir):
    direction_grid = [[[False] * 4 for _ in range(len(mat[0]))] for _ in range(len(mat))]

    while 0 <= cords[0] < len(mat) and 0 <= cords[1] < len(mat[0]):
        if direction_grid[cords[0]][cords[1]][dir]:
            return True
        direction_grid[cords[0]][cords[1]][dir] = True

        next_cords = (cords[0] + direction_map[dir][0], cords[1] + direction_map[dir][1])

        while (
                0 <= next_cords[0] < len(mat) and 0 <= next_cords[1] < len(mat[0])
                and mat[next_cords[0]][next_cords[1]] == '#'
                ):

            dir = (dir + 1) % 4
            next_cords = (cords[0] + direction_map[dir][0], cords[1] + direction_map[dir][1])

        cords = next_cords

    return False


if __name__ == '__main__':
    input_directory = "inputfiles/day6.txt"
    grid = parse_input(input_directory)
    grid_copy = deepcopy(grid)
    print(count_distinct_positions(grid_copy))
    grid_copy = deepcopy(grid)
    print(count_possible_new_obstacles(grid_copy))
