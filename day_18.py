# question & input can be found @ https://adventofcode.com/2024/day/18
from collections import deque

update_cells = []


def parse_input(directory):
    with open(directory, "r") as file:
        for line in file:
            x, y = map(int, line.split(','))
            update_cells.append((x, y))


def inbounds(pos, bounds):
    return 0 <= pos[0] <= bounds[0] and 0 <= pos[1] <= bounds[1]


def shortest_path(bounds):
    end_point = (bounds[0], bounds[1])
    last_byte = bounds[2]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(0, 0, 0)])
    visited = set()
    visited.add((0, 0))

    while queue:
        x, y, dist = queue.popleft()

        if (x, y) == end_point:
            return dist

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if inbounds((nx, ny), end_point) and (ny, nx) not in update_cells[:last_byte] and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))

    return -1


def binary_search_byte(bounds):
    left = bounds[2] + 1
    right = len(update_cells)
    mid = (left + right) // 2

    while left != right:
        bounds = (bounds[0], bounds[1], mid)
        if shortest_path(bounds) == -1:
            right = mid - 1
        else:
            left = mid + 1
        mid = (left + right) // 2

    return update_cells[mid - 1]


if __name__ == '__main__':
    input_dir = "inputfiles/day18.txt"
    parse_input(input_dir)
    bounds_inp = (70, 70, 1024)
    bounds_test = (6, 6, 12)
    print(shortest_path(bounds_inp))
    print(binary_search_byte(bounds_inp))
