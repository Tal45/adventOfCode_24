# question & input can be found @ https://adventofcode.com/2024/day/10
def parse_input(dir):
    li = []
    with open(dir, "r") as file:
        for line in file:
            li.append(list(map(int, line.rstrip())))

    return li


def map_start_points(grid):
    start_pnts = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                start_pnts.append((row,col))

    return start_pnts


def count_trail_scores(grid, pos, visited, prev=-1):
    if not inbounds(pos, grid):
        return 0
    if grid[pos[0]][pos[1]] - prev != 1:
        return 0

    if pos not in visited and grid[pos[0]][pos[1]] == 9:
        visited.add(pos)
        return 1

    return (
            count_trail_scores(grid, (pos[0] + 1, pos[1]), visited, grid[pos[0]][pos[1]]) +
            count_trail_scores(grid, (pos[0] - 1, pos[1]), visited, grid[pos[0]][pos[1]]) +
            count_trail_scores(grid, (pos[0], pos[1] + 1), visited, grid[pos[0]][pos[1]]) +
            count_trail_scores(grid, (pos[0], pos[1] - 1), visited, grid[pos[0]][pos[1]])
            )


def count_trail_ratings(grid, pos, prev=-1):
    if not inbounds(pos, grid):
        return 0
    if grid[pos[0]][pos[1]] - prev != 1:
        return 0

    if grid[pos[0]][pos[1]] == 9:
        return 1

    return (
            count_trail_ratings(grid, (pos[0]+1, pos[1]), grid[pos[0]][pos[1]]) +
            count_trail_ratings(grid, (pos[0]-1, pos[1]), grid[pos[0]][pos[1]]) +
            count_trail_ratings(grid, (pos[0], pos[1]+1), grid[pos[0]][pos[1]]) +
            count_trail_ratings(grid, (pos[0], pos[1]-1), grid[pos[0]][pos[1]])
            )


def inbounds(pos, grid):
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])


if __name__ == "__main__":
    input_directory = "inputfiles/day10.txt"
    grid = parse_input(input_directory)
    start_points = map_start_points(grid)
    count_scores, count_ratings = 0, 0

    for pnt in start_points:
        count_scores += count_trail_scores(grid, pnt, set())
        count_ratings += count_trail_ratings(grid, pnt)
    print(count_scores, count_ratings)