# question & input can be found @ https://adventofcode.com/2024/day/20

from collections import deque
from itertools import combinations
import time


def parse_input(directory):
    g = []
    with open(directory, "r") as file:
        for line in file:
            g.append(list(line.rstrip()))
    return g


def find_path(grid):
    rows = len(grid)
    cols = len(grid[0])
    start, end = None, None

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    queue = deque([(start[0], start[1], [(start[0], start[1], 1)])])
    visited = set()
    visited.add(start)

    while queue:
        r, c, current_path = queue.popleft()

        if (r, c) == end:
            return current_path

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] in ('.', 'E'):
                visited.add((nr, nc))
                queue.append((nr, nc, current_path + [(nr, nc, len(current_path) + 1)]))

    return []


def calculate_cheats(grid):
    original_path = find_path(grid)
    if not original_path:
        return 0

    count_cheats = 0

    for points in combinations(original_path, 2):
        (x1, y1, score1), (x2, y2, score2) = points
        if x1 == x2 and abs(y1 - y2) == 2 or y1 == y2 and abs(x1 - x2) == 2:
            savings = abs(score1 - score2) - 2
            if savings >= 100:
                count_cheats += 1

    return count_cheats


def calculate_cheats_p2(grid):
    original_path = find_path(grid)
    if not original_path:
        return 0

    count_cheats = 0

    for points in combinations(original_path, 2):
        (x1, y1, score1), (x2, y2, score2) = points
        md = abs(x2 - x1) + abs(y2 - y1)
        if 2 <= md <= 20:
            savings = abs(score1 - score2) - md
            if savings >= 100:
                count_cheats += 1

    return count_cheats


if __name__ == "__main__":
    curr_time = time.time()
    input_dir = "inputfiles/day20.txt"
    grid = parse_input(input_dir)
    print(calculate_cheats(grid))
    print(calculate_cheats_p2(grid))
    print("--- Program executed in %s seconds ---" % round(time.time() - curr_time, 2))