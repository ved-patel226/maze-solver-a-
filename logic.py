import heapq
from termcolor import cprint

class aStar:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.open_set = []
        self.came_from = {}
        self.g_score = {}
        self.f_score = {}
        self.explored = []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def search(self):
        self.open_set.append(self.start)
        self.came_from[self.start] = None
        self.g_score[self.start] = 0
        self.f_score[self.start] = self.heuristic(self.start, self.end)

        while self.open_set:
            current = min(
                self.open_set, key=lambda o: self.f_score.get(o, float("inf"))
            )
            if current == self.end:
                return self.reconstruct_path(current), self.explored

            self.open_set.remove(current)
            self.explored.append(current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = self.g_score.get(current, float("inf")) + 1

                if (
                    neighbor not in self.g_score
                    or tentative_g_score < self.g_score[neighbor]
                ):
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    self.f_score[neighbor] = self.g_score[neighbor] + self.heuristic(
                        neighbor, self.end
                    )

                    if neighbor not in self.open_set:
                        self.open_set.append(neighbor)

        return [], self.explored

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        if x > 0 and self.maze[y][x - 1] != "#":  # Left
            neighbors.append((x - 1, y))
        if x < self.cols - 1 and self.maze[y][x + 1] != "#":  # Right
            neighbors.append((x + 1, y))
        if y > 0 and self.maze[y - 1][x] != "#":  # Up
            neighbors.append((x, y - 1))
        if y < self.rows - 1 and self.maze[y + 1][x] != "#":  # Down
            neighbors.append((x, y + 1))
        return neighbors

    def reconstruct_path(self, current):
        path = []
        while current in self.came_from:
            path.append(current)
            current = self.came_from[current]
        path.reverse()
        return path


class RightHandRule:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.explored = []
        self.path = []
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        self.current_direction_index = 0

    def search(self):
        current = self.start
        self.path.append(current)
        self.explored.append(current)
        while current != self.end:
            current = self.follow_right_hand(current)
            if not current:
                cprint("No path found", "magenta")
                break
            self.path.append(current)
            self.explored.append(current)
        
        return self.path, self.explored

    def follow_right_hand(self, current):
        x, y = current
        for i in range(4):
            direction = self.directions[(self.current_direction_index + i) % 4]
            next_x, next_y = x + direction[0], y + direction[1]
            if self.is_valid_move(next_x, next_y):
                self.current_direction_index = (self.current_direction_index + i - 1) % 4
                return next_x, next_y
        return None

    def is_valid_move(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows and self.maze[y][x] != "#"
    
class DeadEndFilling:
    def __init__(self, maze, start, end):
        self.original_maze = [list(row) for row in maze]
        self.maze = [list(row) for row in maze]
        self.start = start
        self.end = end
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.explored = []
        self.path = []

class DeadEndFilling:
    def __init__(self, maze, start, end):
        self.original_maze = [list(row) for row in maze]
        self.maze = [list(row) for row in maze]
        self.start = start
        self.end = end
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.explored = []
        self.path = []

    def search(self):
        while True:
            self.mark_dead_ends()
            if self.is_path_to_end():
                self.path = self.find_path(self.start, self.end)
                return self.path, self.explored
            else:
                return [], self.explored

    def mark_dead_ends(self):
        while True:
            dead_ends_found = False
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.maze[y][x] == "." and self.is_dead_end((x, y)):
                        self.remove_dead_end((x, y))
                        dead_ends_found = True
                        self.explored.append((x, y))
            if not dead_ends_found:
                break

    def is_dead_end(self, node):
        x, y = node
        neighbors = self.get_neighbors(node)
        return len(neighbors) == 1

    def remove_dead_end(self, node):
        x, y = node
        self.maze[y][x] = "#"  # Mark dead end as wall

    def is_path_to_end(self):
        return bool(self.find_path(self.start, self.end))

    def find_path(self, start, end):
        queue = [start]
        came_from = {start: None}
        while queue:
            current = queue.pop(0)
            if current == end:
                return self.reconstruct_path(came_from, end)
            for neighbor in self.get_neighbors(current):
                if neighbor not in came_from and self.maze[neighbor[1]][neighbor[0]] == ".":
                    came_from[neighbor] = current
                    queue.append(neighbor)
        return []

    def reconstruct_path(self, came_from, current):
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        if x > 0 and self.maze[y][x - 1] != "#":  # Left
            neighbors.append((x - 1, y))
        if x < self.cols - 1 and self.maze[y][x + 1] != "#":  # Right
            neighbors.append((x + 1, y))
        if y > 0 and self.maze[y - 1][x] != "#":  # Up
            neighbors.append((x, y - 1))
        if y < self.rows - 1 and self.maze[y + 1][x] != "#":  # Down
            neighbors.append((x, y + 1))
        return neighbors

class Dijkstra:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.open_set = []
        self.came_from = {}
        self.g_score = {}
        self.explored = []

    def search(self):
        heapq.heappush(self.open_set, (0, self.start))
        self.came_from[self.start] = None
        self.g_score[self.start] = 0

        while self.open_set:
            current_cost, current = heapq.heappop(self.open_set)
            
            if current == self.end:
                return self.reconstruct_path(current), self.explored

            self.explored.append(current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = self.g_score.get(current, float("inf")) + 1

                if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    heapq.heappush(self.open_set, (tentative_g_score, neighbor))

        return [], self.explored

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        if x > 0 and self.maze[y][x - 1] != "#":  # Left
            neighbors.append((x - 1, y))
        if x < self.cols - 1 and self.maze[y][x + 1] != "#":  # Right
            neighbors.append((x + 1, y))
        if y > 0 and self.maze[y - 1][x] != "#":  # Up
            neighbors.append((x, y - 1))
        if y < self.rows - 1 and self.maze[y + 1][x] != "#":  # Down
            neighbors.append((x, y + 1))
        return neighbors

    def reconstruct_path(self, current):
        path = []
        while current in self.came_from:
            path.append(current)
            current = self.came_from[current]
        path.reverse()
        return path
