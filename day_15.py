# question & input @ https://adventofcode.com/2024/day/15

dir = {
        '^': (-1, 0),
        '>': (0, 1),
        '<': (0, -1),
        'v': (1, 0)
    }


def parse_input(directory):
    moves = []
    grid = []
    with open(directory, "r") as file:
        data = file.read()
        g, m = data.split('\n\n')

    for line in g.split('\n'):
        grid.append(list(line))

    for line in m:
        moves += list(line.rstrip())

    return grid, moves


def find_bot(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '@':
                return r, c


def run_bot(grid, moves, pos):
    while moves:
        move = moves.pop(0)
        next_pos = calc_pos(pos, dir[move])
        if inbounds(next_pos, grid):
            if grid[next_pos[0]][next_pos[1]] == '.':
                grid[next_pos[0]][next_pos[1]], grid[pos[0]][pos[1]] = grid[pos[0]][pos[1]], grid[next_pos[0]][
                    next_pos[1]]
                pos = next_pos
            elif grid[next_pos[0]][next_pos[1]] == 'O':
                pos = push_box(grid, pos, dir[move])


def push_box(grid, pos, move):
    box_n_bot = ['@', 'O']
    end_row, end_col = pos
    can_move = False
    while inbounds((end_row, end_col), grid):
        if grid[end_row][end_col] in box_n_bot:
            end_row, end_col = end_row + move[0], end_col + move[1]
        elif grid[end_row][end_col] == '.':
            can_move = True
            break
        else:
            break

    if can_move:
        while (end_row, end_col) != pos:
            grid[end_row][end_col] = grid[end_row - move[0]][end_col - move[1]]
            end_row, end_col = end_row - move[0], end_col - move[1]
        grid[pos[0]][pos[1]] = '.'
        pos = calc_pos(pos, move)

    return pos


def sum_gps(grid):
    total_sum = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'O':
                total_sum += (100 * r) + c

    return total_sum


def update_warehouse(grid):
    new_grid = []
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[0])):
            if grid[r][c] == '#':
                row.append('#')
                row.append('#')
            elif grid[r][c] == 'O':
                row.append('[')
                row.append(']')
            elif grid[r][c] == '.':
                row.append('.')
                row.append('.')
            else:
                row.append('@')
                row.append('.')
        new_grid.append(row)
    return new_grid


def inbounds(pos, grid):
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])


def calc_pos(pos, move):
    return pos[0] + move[0], pos[1] + move[1]


def run_bot_extended(grid, move, bot_pos):
    new_pos = calc_pos(bot_pos, dir[move])
    if not inbounds(new_pos, grid) or grid[new_pos[0]][new_pos[1]] == '#':
        return False

    if grid[new_pos[0]][new_pos[1]] == '.':
        grid[bot_pos[0]][bot_pos[1]] = '.'
        grid[new_pos[0]][new_pos[1]] = '@'
        return True

    if move in "<>":
        can_move = False
        curr_pos = new_pos
        while inbounds(curr_pos, grid) and grid[curr_pos[0]][curr_pos[1]] != '#':
            if grid[curr_pos[0]][curr_pos[1]] == '.':
                can_move = True
                break
            curr_pos = calc_pos(curr_pos, dir[move])

        if not can_move:
            return False

        curr_pos = new_pos
        while grid[curr_pos[0]][curr_pos[1]] != '.':
            grid[curr_pos[0]][curr_pos[1]], grid[bot_pos[0]][bot_pos[1]] = grid[bot_pos[0]][bot_pos[1]], grid[curr_pos[0]][curr_pos[1]]
            curr_pos = calc_pos(curr_pos, dir[move])

        grid[curr_pos[0]][curr_pos[1]] = grid[bot_pos[0]][bot_pos[1]]
        grid[bot_pos[0]][bot_pos[1]] = '.'
        return True

    if check_vertical(grid, move, new_pos):
        if grid[new_pos[0]][new_pos[1]] == '[':
            lr = calc_pos(new_pos, (0, 1))
        else:
            lr = calc_pos(new_pos, (0, -1))

        push_vertical(grid, move, new_pos)
        grid[bot_pos[0]][bot_pos[1]] = '.'
        grid[lr[0]][lr[1]] = '.'
        grid[new_pos[0]][new_pos[1]] = '@'
        return True

    return False


def check_vertical(grid, move, pos):
    lr = get_box_lr(grid, pos)
    next_pos = calc_pos(pos, dir[move])
    next_lr = calc_pos(lr, dir[move])

    if grid[next_pos[0]][next_pos[1]] == '.' and grid[next_lr[0]][next_lr[1]] == '.':
        return True

    if grid[next_pos[0]][next_pos[1]] == '#' or grid[next_lr[0]][next_lr[1]] == '#':
        return False

    if grid[next_pos[0]][next_pos[1]] != '.':
        if not check_vertical(grid, move, next_pos):
            return False

    if grid[next_lr[0]][next_lr[1]] != '.':
        if not check_vertical(grid, move, next_lr):
            return False

    return True


def push_vertical(grid, move, pos):
    lr = get_box_lr(grid, pos)
    next_pos = calc_pos(pos, dir[move])
    next_lr = calc_pos(lr, dir[move])

    if grid[next_pos[0]][next_pos[1]] != '.':
        push_vertical(grid, move, next_pos)

    if grid[next_lr[0]][next_lr[1]] != '.':
        push_vertical(grid, move, next_lr)

    grid[next_pos[0]][next_pos[1]] = grid[pos[0]][pos[1]]
    grid[next_lr[0]][next_lr[1]] = grid[lr[0]][lr[1]]
    grid[pos[0]][pos[1]] = '.'
    grid[lr[0]][lr[1]] = '.'


def sum_gps_p2(grid):
    total_sum = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '[':
                total_sum += (100 * r) + c

    return total_sum


def get_box_lr(grid, pos):
    if grid[pos[0]][pos[1]] == '[':
        lr = calc_pos(pos, (0, 1))
    else:
        lr = calc_pos(pos, (0, -1))
    return lr


if __name__ == '__main__':
    input_dir = "inputfiles/day15.txt"
    grid, moves = parse_input(input_dir)
    bot_pos = find_bot(grid)
    run_bot(grid, moves, bot_pos)
    print(sum_gps(grid))

    grid, moves = parse_input(input_dir)
    new_grid = update_warehouse(grid)
    for move in moves:
        bot_pos = find_bot(new_grid)
        run_bot_extended(new_grid, move, bot_pos)
    print(sum_gps_p2(new_grid))
