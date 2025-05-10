import heapq
from grid import DIRECTIONS, GRID_SIZE

class AStarSimulator:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.open_set = []
        self.closed_set = set()
        self.came_from = {}
        self.g_score = {start: 0}
        self.f_score = {start: self.grid.heuristic(start, goal)}
        heapq.heappush(self.open_set, (self.f_score[start], start))
        self.path = []
        self.finished = False

    def step(self):
        if self.finished:
            return
        if not self.open_set:
            self.finished = True
            return
        _, current = heapq.heappop(self.open_set)
        self.closed_set.add(current)

        if current == self.goal:
            node = current
            while node in self.came_from:
                self.path.append(node)
                node = self.came_from[node]
            self.path.append(self.start)
            self.path.reverse()
            self.finished = True
            return

        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE
                and self.grid.grid[neighbor] != 1):
                tentative_g = self.g_score[current] + 1
                if neighbor not in self.g_score or tentative_g < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g
                    f = tentative_g + self.grid.heuristic(neighbor, self.goal)
                    self.f_score[neighbor] = f
                    if neighbor not in self.closed_set:
                        heapq.heappush(self.open_set, (f, neighbor))