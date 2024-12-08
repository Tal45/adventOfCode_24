# question and input @ https://adventofcode.com/2024/day/8

def parse_input_to_grid(dir):
    grid = []
    with open(dir, "r") as file:
        for line in file:
            grid.append(list(line.rstrip()))

    return grid


def find_ants_and_bounds(grid):
    ant_cords = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != '.':
                ant_cords.append((row, col, grid[row][col]))

    return ant_cords, (len(grid), len(grid[0]))


def count_antinodes(map, bounds):
    new_nodes = set()
    new_nodes_harmonics = set()
    for idx, ant in enumerate(map):
        current_ant = map.pop(idx)
        for ant2 in map:
            if ant[2] == ant2[2]:
                tmp = create_antinodes(ant, ant2, bounds)
                for n in tmp:
                    if n:
                        new_nodes.add(n)
                tmp2 = create_antinodes_w_harmonics(ant, ant2, bounds)
                for n in tmp2:
                    if n:
                        new_nodes_harmonics.add(n)
        map.insert(idx, current_ant)
    return len(new_nodes), len(new_nodes_harmonics)


def create_antinodes_w_harmonics(ant, ant2, bounds):
    diff_node1 = (ant[0] - ant2[0], ant[1] - ant2[1])
    diff_node2 = (ant2[0] - ant[0], ant2[1] - ant[1])
    node1 = (ant[0], ant[1])
    node2 = (ant2[0], ant2[1])
    antinodes_list = []
    i = 0
    while inbounds(node1, bounds):
        antinodes_list.append(node1)
        node1 = (ant[0] + i*diff_node1[0], ant[1] + i*diff_node1[1])
        i += 1

    i = 0
    while inbounds(node2, bounds):
        antinodes_list.append(node2)
        node2 = (ant2[0] + i*diff_node2[0], ant2[1] + i*diff_node2[1])
        i += 1

    return antinodes_list


def create_antinodes(ant, ant2, bounds):
    diff_node1 = (ant[0] - ant2[0], ant[1] - ant2[1])
    diff_node2 = (ant2[0] - ant[0], ant2[1] - ant[1])
    node1 = (ant[0] + diff_node1[0], ant[1] + diff_node1[1])
    node2 = (ant2[0] + diff_node2[0], ant2[1] + diff_node2[1])
    if not inbounds(node1, bounds):
        node1 = None
    if not inbounds(node2, bounds):
        node2 = None
    return node1, node2


def inbounds(node, bounds):
    return 0 <= node[0] < bounds[0] and 0 <= node[1] < bounds[1]


if __name__ == '__main__':
    input_directory = "inputfiles/day8.txt"
    grid = parse_input_to_grid(input_directory)
    map_ants, map_bounds = find_ants_and_bounds(grid)
    print(count_antinodes(map_ants, map_bounds))
