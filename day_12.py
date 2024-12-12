# input and question can be found @ https://adventofcode.com/2024/day/12

def parse_input(dir):
    grid = []
    with open(dir, "r") as file:
        for line in file:
            grid.append(list(line.rstrip()))

    return grid


def find_all_plants(grid, pos, type, region, mark):
    if not inbounds(pos, grid) or grid[pos[0]][pos[1]] != type:
        return

    up = (pos[0] - 1, pos[1])
    down = (pos[0] + 1, pos[1])
    left = (pos[0], pos[1] - 1)
    right = (pos[0], pos[1] + 1)

    count = 0
    if not inbounds(up, grid) or not same_neighbour(up, grid, type, mark):
        count += 1
    if not inbounds(down, grid) or not same_neighbour(down, grid, type, mark):
        count += 1
    if not inbounds(left, grid) or not same_neighbour(left, grid, type, mark):
        count += 1
    if not inbounds(right, grid) or not same_neighbour(right, grid, type, mark):
        count += 1

    region.add((pos[0], pos[1], count))
    grid[pos[0]][pos[1]] = mark

    find_all_plants(grid, up, type, region, mark)
    find_all_plants(grid, down, type, region, mark)
    find_all_plants(grid, left, type, region, mark)
    find_all_plants(grid, right, type, region, mark)


def inbounds(pos, grid):
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])


def same_neighbour(pos, grid, type, mark):
    return grid[pos[0]][pos[1]] == type or grid[pos[0]][pos[1]] == mark


def calculate_cost(grid):
    total_cost = 0
    discount_cost = 0
    visit_mark = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if isinstance(grid[row][col], str):
                region = set()
                find_all_plants(grid, (row,col), grid[row][col], region, visit_mark)
                perimeter = sum(x[2] for x in region)
                area = len(region)
                all_region_cords = get_all_region_cords(grid, visit_mark)
                sides = count_sides(all_region_cords)
                total_cost += area * perimeter
                discount_cost += area * sides
                visit_mark += 1

    return total_cost, discount_cost


def get_all_region_cords(grid, mark):
    tmp = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == mark:
                tmp.append((r, c))
    return tmp


def count_sides(region_cords):
    count = 0
    for pos in region_cords:

        left = (pos[0], pos[1] - 1) in region_cords
        right = (pos[0], pos[1] + 1) in region_cords
        up = (pos[0] - 1, pos[1]) in region_cords
        down = (pos[0] + 1, pos[1]) in region_cords
        up_left = (pos[0] - 1, pos[1] - 1) in region_cords
        up_right = (pos[0] - 1, pos[1] + 1) in region_cords
        down_left = (pos[0] + 1, pos[1] - 1) in region_cords
        down_right = (pos[0] + 1, pos[1] + 1) in region_cords

        if not left and not up:
            count += 1
        if not right and not up:
            count += 1
        if not left and not down:
            count += 1
        if not right and not down:
            count += 1
        if not up_right and up and right:
            count += 1
        if not up_left and up and left:
            count += 1
        if not down_left and down and left:
            count += 1
        if not down_right and down and right:
            count += 1

    return count


if __name__ == "__main__":
    input_dir = "inputfiles/day12.txt"
    grid = parse_input(input_dir)
    print(calculate_cost(grid))
