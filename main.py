import pygame
import sys
from termcolor import cprint
from logic import aStar, DeadEndFilling, Dijkstra

single = input("Do you want to run the program in single or race mode? (r/s): ")

if single.lower() == "s":
    pygame.init()

    # Constants
    CELL_SIZE = 3
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    START_COLOR = (0, 255, 0)
    END_COLOR = (255, 0, 0)
    PATH_COLOR = (255, 0, 0)
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
    astar = DeadEndFilling(maze, start, end)
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

else:
    
    pygame.init()

    # Constants
    CELL_SIZE = 20
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    START_COLOR = (0, 255, 0)
    END_COLOR = (0, 0, 255)
    PATH_COLOR = (0, 0, 255)
    EXPLORED_COLOR = (200, 200, 200)
    RHR_PATH_COLOR = (255, 165, 0)
    RHR_EXPLORED_COLOR = (200, 200, 200)

    # Function to load maze from a file
    def load_maze(file_path):
        with open(file_path, "r") as file:
            return [list(line.strip()) for line in file.readlines()]

    # Function to draw the maze on the surface
    def draw_maze(surface, maze):
        color_map = {"#": BLACK, ".": WHITE, "S": START_COLOR, "E": END_COLOR}
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, color_map.get(cell, WHITE), rect)

    # Function to draw explored cells and path
    def draw_explored_path(surface, explored, path, explored_color, path_color):
        for x, y in explored:
            pygame.draw.rect(surface, explored_color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for x, y in path:
            pygame.draw.rect(surface, path_color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def color_remaining_white_cells(surface, maze, explored, path, color):
        explored_set = set(explored)
        path_set = set(path)
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == "." and (x, y) not in explored_set and (x, y) not in path_set:
                    pygame.draw.rect(surface, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Load maze and initialize variables
    maze = load_maze("maze.txt")
    start = next((x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "S")
    end = next((x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "E")

    if not start or not end:
        raise ValueError("Start or End position not found in the maze file.")

    # Calculate dimensions
    ROWS, COLS = len(maze), len(maze[0])
    WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
    SURFACE_WIDTH, SURFACE_HEIGHT = WIDTH * 2, HEIGHT

    # Setup surfaces
    screen = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    pygame.display.set_caption("Maze Visualization")

    surface_astar = pygame.Surface((WIDTH, HEIGHT))
    surface_rhr = pygame.Surface((WIDTH, HEIGHT))

    draw_maze(surface_astar, maze)
    draw_maze(surface_rhr, maze)

    # Initialize algorithms
    astar = Dijkstra(maze, start, end)
    path_a_star, explored_a_star = astar.search()
    
    rhr = DeadEndFilling(maze, start, end)
    path_rhr, explored_rhr = rhr.search()

    # Real-time visualization
    explored_steps_astar = 0
    path_step_astar = 0
    explored_steps_rhr = 0
    path_step_rhr = 0
    rhr_done = False

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(WHITE)
        
        # Draw A* maze and path
        draw_maze(surface_astar, maze)
        draw_explored_path(surface_astar, explored_a_star[:explored_steps_astar], path_a_star[:path_step_astar + 1], EXPLORED_COLOR, PATH_COLOR)
        screen.blit(surface_astar, (WIDTH, 0))

        # Draw Right Hand Rule maze and path
        draw_maze(surface_rhr, maze)
        draw_explored_path(surface_rhr, explored_rhr[:explored_steps_rhr], path_rhr[:path_step_rhr + 1], RHR_EXPLORED_COLOR, RHR_PATH_COLOR)
        
        if rhr_done:
            color_remaining_white_cells(surface_rhr, maze, explored_rhr, path_rhr, RHR_PATH_COLOR)
            
        screen.blit(surface_rhr, (0, 0))
        pygame.display.flip()

        # Increment steps
        if explored_steps_astar < len(explored_a_star):
            explored_steps_astar += 1
        elif path_step_astar < len(path_a_star):
            path_step_astar += 1

        if explored_steps_rhr < len(explored_rhr):
            explored_steps_rhr += 1
        elif path_step_rhr < len(path_rhr):
            path_step_rhr += 1
        elif not rhr_done:
            rhr_done = True
            color_remaining_white_cells(surface_rhr, maze, explored_rhr, path_rhr, RHR_PATH_COLOR)
            
        clock.tick(60)
