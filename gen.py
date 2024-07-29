from collections import deque


def is_solvable(maze, start, end, height, width):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([start])
    visited = set()
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == end:
            return True
        for d in directions:
            ni, nj = current[0] + d[0], current[1] + d[1]
            if (
                0 <= ni < height
                and 0 <= nj < width
                and maze[ni][nj] in ["c", "e"]
                and (ni, nj) not in visited
            ):
                visited.add((ni, nj))
                queue.append((ni, nj))

    return False


# Updated maze generation to ensure connectivity
import random
from colorama import init, Fore

# Initialize colorama
init()


def printMaze(maze):
    for row in maze:
        for cell in row:
            if cell == "u":
                print(Fore.WHITE + ".", end="")
            elif cell == "c":
                print(Fore.GREEN + ".", end="")
            elif cell == "w":
                print(Fore.RED + "#", end="")
            elif cell == "s":
                print(Fore.BLUE + "S", end="")
            elif cell == "e":
                print(Fore.MAGENTA + "E", end="")
        print()


def surroundingCells(rand_wall, maze, height, width):
    s_cells = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for d in directions:
        ni, nj = rand_wall[0] + d[0], rand_wall[1] + d[1]
        if 0 <= ni < height and 0 <= nj < width and maze[ni][nj] == "c":
            s_cells += 1
    return s_cells


# Init variables
wall = "w"
cell = "c"
unvisited = "u"
height = 1001
width = 2001
maze = []

entrance = "s"
exit = "e"

# Initialize the maze with outer walls
maze = [
    [
        wall if i == 0 or i == height - 1 or j == 0 or j == width - 1 else unvisited
        for j in range(width)
    ]
    for i in range(height)
]

# Randomize starting point and set it a cell
starting_height, starting_width = random.randint(1, height - 2), random.randint(
    1, width - 2
)
maze[starting_height][starting_width] = cell
walls = [
    [starting_height + di, starting_width + dj]
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if maze[starting_height + di][starting_width + dj] == unvisited
]

while walls:
    rand_wall = random.choice(walls)
    walls.remove(rand_wall)

    r, c = rand_wall
    if maze[r][c] == wall:
        continue

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    adjacent_cells = [
        maze[r + d[0]][c + d[1]]
        for d in directions
        if 0 <= r + d[0] < height and 0 <= c + d[1] < width
    ]

    if adjacent_cells.count(cell) < 2:
        maze[r][c] = cell
        new_walls = [
            (r + d[0], c + d[1])
            for d in directions
            if 0 <= r + d[0] < height
            and 0 <= c + d[1] < width
            and maze[r + d[0]][c + d[1]] == unvisited
        ]

        for nw in new_walls:
            if nw not in walls:
                walls.append(nw)

        maze[r][c] = cell

# Mark the remaining unvisited cells as walls
for i in range(height):
    for j in range(width):
        if maze[i][j] == unvisited:
            maze[i][j] = wall

# Set entrance and exit
for i in range(1, width - 1):
    if maze[1][i] == "c":
        maze[0][i] = entrance
        start = (0, i)
        break

for i in range(width - 2, 0, -1):
    if maze[height - 2][i] == "c":
        maze[height - 1][i] = exit
        end = (height - 1, i)
        break

# Print final maze
with open("maze.txt", "w") as file:
    for row in maze:
        for cell in row:
            if cell == "u":
                file.write(".")
            elif cell == "c":
                file.write(".")
            elif cell == "w":
                file.write("#")
            elif cell == "s":
                file.write("S")
            elif cell == "e":
                file.write("E")
        file.write("\n")
