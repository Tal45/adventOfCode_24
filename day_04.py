# question & input can be found @ https://adventofcode.com/2024/day/4

def count_xmas(grid):
    rows, cols = len(grid), len(grid[0])
    word = "XMAS"
    word_len = len(word)
    count = 0

    def check_direction(row, col, dir_x, dir_y):
        for i in range(word_len):
            new_row = row + i * dir_x
            new_col = col + i * dir_y
            if not (0 <= new_row < rows and 0 <= new_col < cols):
                return False
            if grid[new_row][new_col] != word[i]:
                return False
        return True

    for row in range(rows):
        for col in range(cols):
            directions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1)
            ]
            for dir_x, dir_y in directions:
                if check_direction(row, col, dir_x, dir_y):
                    count += 1

    return count


def count_x_mas(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0

    def is_valid_x(row, col):
        diagonal1 = [grid[row - 1][col - 1], grid[row + 1][col + 1]]
        diagonal2 = [grid[row - 1][col + 1], grid[row + 1][col - 1]]
        return sorted(diagonal1) == ['M', 'S'] == sorted(diagonal2)

    for row in range(1, rows-1):
        for col in range(1, cols-1):
            if grid[row][col] == 'A':
                if is_valid_x(row, col):
                    count += 1

    return count


if __name__ == '__main__':
    # replace with your input directory
    input_directory = "inputfiles/day4.txt"
    mat = []
    with open(input_directory) as f:
        for line in f:
            row = list(line.rstrip())
            mat.append(row)

    print(count_xmas(mat))
    print(count_x_mas(mat))
