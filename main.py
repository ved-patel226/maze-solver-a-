import pygame
import sys
import time

from termcolor import cprint
from logic import aStar

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
PATH_COLOR = (0, 0, 255)
EXPLORED_COLOR = (200, 200, 200)
DELAY_MS = 0
OUTPUT_FILE = "maze_visualization.png"


# Function to load maze from a file
def load_maze(file_path):
    with open(file_path, "r") as file:
        maze = [line.strip() for line in file.readlines()]
    return maze


# Function to draw the maze on the surface
def draw_maze(surface):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == "#":
                pygame.draw.rect(surface, BLACK, rect)
            elif cell == ".":
                pygame.draw.rect(surface, WHITE, rect)
            elif cell == "S":
                pygame.draw.rect(surface, START_COLOR, rect)
            elif cell == "E":
                pygame.draw.rect(surface, END_COLOR, rect)


# Function to draw explored cells and path
def draw_explored_path(surface, explored, path):
    if explored:
        for x, y in explored:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, EXPLORED_COLOR, rect)
    if path:
        for x, y in path:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, PATH_COLOR, rect)


# Load maze and initialize variables
maze = load_maze("maze.txt")
start = None
end = None
for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == "S":
            start = (x, y)
        elif cell == "E":
            end = (x, y)

if not start or not end:
    raise ValueError("Start or End position not found in the maze file.")

# Calculate dimensions
ROWS = len(maze)
COLS = len(maze[0])
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Find the path using A* algorithm
astar = aStar(maze, start, end)
path, explored = astar.search()
cprint(path, "red")

# Ask the user for their choice
choice = input("Do you want to visualize the maze with Pygame (y/n)? ").strip().lower()

if choice == "y":
    # Pygame visualization
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Visualization")

    # Create an off-screen surface to draw on
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(WHITE)

    # Draw the maze
    draw_maze(surface)

    # Main loop
    running = True
    explored_steps = 0  # Variable to keep track of explored steps
    path_step = 0  # Variable to keep track of path steps
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)  # Fill background with white
        screen.blit(surface, (0, 0))

        # Draw explored cells up to the current explored step
        if explored:
            for x, y in explored[:explored_steps]:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, EXPLORED_COLOR, rect)

        # Draw the path up to the current path step
        if path:
            for x, y in path[: path_step + 1]:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, PATH_COLOR, rect)

        pygame.display.flip()

        # Increment steps and delay
        if explored_steps < len(explored):
            explored_steps += 1
        elif path_step < len(path):
            path_step += 1

        # time.sleep(DELAY_MS / 1000.0)  # Delay in seconds

    pygame.quit()

else:
    # Save as PNG
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(WHITE)

    # Draw the maze and the path
    draw_maze(surface)
    draw_explored_path(surface, explored, path)

    # Save the surface to a PNG file
    pygame.image.save(surface, OUTPUT_FILE)
    cprint(f"Visualization saved to {OUTPUT_FILE}", "green", attrs=["bold"])

pygame.quit()
sys.exit()
