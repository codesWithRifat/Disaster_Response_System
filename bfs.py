from collections import deque
from grid import DIRECTIONS, GRID_SIZE

class BFSSimulator:
    def __init__(self, grid, start):
        self.grid = grid
        self.visited = set()
        self.exploration_queue = deque([start])
        self.visited.add(start)
        self.last_explored = None

    def step(self):
        if not self.exploration_queue:
            return True

        current = self.exploration_queue.popleft()
        self.last_explored = current

        if self.grid.grid[current] == 2 and current not in self.grid.found_survivors:
            self.grid.found_survivors.append(current)

        for dx, dy in DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if (nx, ny) not in self.visited and self.grid.grid[nx, ny] != 1:
                    self.visited.add((nx, ny))
                    self.exploration_queue.append((nx, ny))

        return len(self.grid.found_survivors) == len(self.grid.survivors)