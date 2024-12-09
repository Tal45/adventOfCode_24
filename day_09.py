# question & input can be found @ https://adventofcode.com/2024/day/9

import time


def parse_input(dir):
    with open(dir, "r") as file:
        line = file.read()
        inp = list(map(int, line.rstrip()))

    return inp


def map_disk_by_id(map):
    new_map = []
    current_id = 0
    for idx, val in enumerate(map):
        if idx % 2 == 0:
            for j in range(val):
                new_map.append(current_id)
            current_id += 1
        else:
            for j in range(val):
                new_map.append('.')
    return new_map


def defragmentation(map):
    new_map = map_disk_by_id(map)

    free_space_ptr, last_id = 0, len(new_map)-1
    while free_space_ptr < last_id:
        while new_map[free_space_ptr] != '.':
            free_space_ptr += 1
        while new_map[last_id] == '.':
            last_id -= 1
        if free_space_ptr < last_id:
            new_map[free_space_ptr], new_map[last_id] = new_map[last_id], new_map[free_space_ptr]

    checksum = 0
    for idx in range(new_map.index('.')):
        checksum += idx * new_map[idx]

    return checksum


def custom_defragmentation(map):
    new_map = map_disk_by_id(map)

    def find_free_space_segment(block_size):
        current_start = -1
        current_length = 0

        for i, char in enumerate(new_map):
            if char == '.':
                if current_length == 0:
                    current_start = i
                current_length += 1

                if current_length >= block_size:
                    return current_start, i
            else:
                current_start = -1
                current_length = 0

        return None

    data_block_end = len(new_map) - 1

    while 0 <= data_block_end:
        while 0 <= data_block_end and new_map[data_block_end] == '.':
            data_block_end -= 1
        data_block_start = data_block_end

        while 0 <= data_block_start and new_map[data_block_start] == new_map[data_block_end]:
            data_block_start -= 1
        data_block_start += 1

        data_block_size = data_block_end - data_block_start + 1
        free_space_seg = find_free_space_segment(data_block_size)

        if free_space_seg and free_space_seg[1] < data_block_start:
            new_map[free_space_seg[0]:free_space_seg[1] + 1] = new_map[data_block_start:data_block_end + 1]
            new_map[data_block_start:data_block_end + 1] = ['.'] * data_block_size

        data_block_end = data_block_start - 1

    checksum = 0
    for idx, val in enumerate(new_map):
        if val != '.':
            checksum += idx * val

    return checksum


if __name__ == "__main__":
    inp_dir = "inputfiles/day9.txt"
    start_time = time.time()
    new_map = parse_input(inp_dir)
    print(defragmentation(new_map))
    print(custom_defragmentation(new_map))
    print("--- %s seconds ---" % round(time.time() - start_time, 2))



