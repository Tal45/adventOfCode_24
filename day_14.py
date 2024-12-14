# input & question can be found @ https://adventofcode.com/2024/day/14

import re
import matplotlib.pyplot as plt
import numpy as np


def parse_input(dir):
    robots = []
    pattern = r"-?\d+(?:\.\d+)?"
    with open(dir, "r") as file:
        for line in file:
            nums = list(map(int, re.findall(pattern, line.rstrip())))
            pos, vel = (nums[1], nums[0]), (nums[3], nums[2])
            robots.append((pos, vel))
    return robots


def move_robots(robots, row, col, seconds):
    grid = [[0 for _ in range(col)] for _ in range(row)]

    for robot in robots:
        x, y = robot[0]
        vec_x, vec_y = robot[1]
        for _ in range(seconds):
            x = (x + vec_x) % row
            y = (y + vec_y) % col
        grid[x][y] += 1

    return grid


def calculate_safety_factor(grid):
    row = len(grid)
    col = len(grid[0])
    q1, q2, q3, q4 = 0, 0, 0, 0
    for x in range(row):
        for y in range(col):
            if grid[x][y] > 0:
                if x < row // 2 and y < col // 2:
                    q1 += grid[x][y]
                elif x < row // 2 and y > col // 2:
                    q2 += grid[x][y]
                elif x > row // 2 and y < col // 2:
                    q3 += grid[x][y]
                elif x > row // 2 and y > col // 2:
                    q4 += grid[x][y]

    return q1 * q2 * q3 * q4


def find_tree(robots, row, col, seconds):
    grid = [[0 for _ in range(col)] for _ in range(row)]

    for robot in robots:
        x,y = robot[0]
        grid[x][y] += 1

    for i in range(seconds):
        for idx, robot in enumerate(robots):
            x,y = robot[0]
            vec_x, vec_y = robot[1]
            grid[x][y] -= 1
            x = (x + vec_x) % row
            y = (y + vec_y) % col
            grid[x][y] += 1
            robots[idx] = ((x, y), (vec_x, vec_y))
        find_consecutive_in_row(grid, i + 1)


def find_consecutive_in_row(grid, sec):
    for row in range(len(grid)):
        count = 0
        for col in range(len(grid[0])):
            if grid[row][col] > 0:
                count += 1
                if count == 10:
                    save_highlighted_grid(grid, f"second_{sec}")
                    return
            else:
                count = 0
    return


# save_highlighted_grid function courtesy of ChatGPT
def save_highlighted_grid(grid, filename, output_folder = "day14_easter_egg"):
    """
    Save a 2D grid as a picture, highlighting cells with the specified value.

    :param grid: 2D list or numpy array representing the grid.
    :param filename: The name of the file to save the picture (e.g., "grid.png").
    """
    import os
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    grid = np.array(grid)
    rows, cols = grid.shape

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Create a colored grid with a colormap
    cmap = plt.cm.Pastel1  # Use a pastel colormap for background
    ax.matshow(grid, cmap=cmap, alpha=0.3)

    # Add text annotations for each cell
    for i in range(rows):
        for j in range(cols):
            color = "black"
            if grid[i, j] > 0:
                color = "white"
            ax.text(j, i, str(grid[i, j]), va='center', ha='center', color=color)

    # Set axis ticks to represent grid layout
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=1)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

    # Save the figure
    plt.savefig(f"{output_folder}/{filename}.png", dpi=300, bbox_inches='tight')
    print(f"Picture saved to {output_folder}/{filename}")
    plt.close(fig)


if __name__ == '__main__':
    input_dir = "inputfiles/day14.txt"
    robots = parse_input(input_dir)
    row, col, ticks = 103, 101, 100
    grid = move_robots(robots, row, col, ticks)
    print(calculate_safety_factor(grid))
    find_tree(robots, row, col, 10000)
