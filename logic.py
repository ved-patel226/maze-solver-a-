import heapq


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
        # Manhattan distance heuristic
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
