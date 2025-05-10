import numpy as np
import random

GRID_SIZE = 20
CELL_SIZE = 40
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Grid:
    def __init__(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.generate_obstacles()
        self.place_survivors_and_start_points()
        self.found_survivors = []
        self.paths = {}

    def generate_obstacles(self):
        obstacle_count = int(GRID_SIZE * GRID_SIZE * 0.25)
        for _ in range(obstacle_count):
            while True:
                x, y = random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)
                if self.grid[x, y] == 0:
                    self.grid[x, y] = 1
                    break

    def place_survivors_and_start_points(self):
        self.survivors = []
        for _ in range(50):
            while True:
                x, y = random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)
                if self.grid[x, y] == 0:
                    self.grid[x, y] = 2
                    self.survivors.append((x, y))
                    break

        self.start_points = []
        sides = ['top', 'bottom', 'left', 'right']
        selected_sides = random.sample(sides, 2)
        for side in selected_sides:
            if side == 'top':
                x, y = random.randrange(GRID_SIZE), 0
            elif side == 'bottom':
                x, y = random.randrange(GRID_SIZE), GRID_SIZE - 1
            elif side == 'left':
                x, y = 0, random.randrange(GRID_SIZE)
            elif side == 'right':
                x, y = GRID_SIZE - 1, random.randrange(GRID_SIZE)
            while self.grid[x, y] != 0:
                if side == 'top':
                    x, y = random.randrange(GRID_SIZE), 0
                elif side == 'bottom':
                    x, y = random.randrange(GRID_SIZE), GRID_SIZE - 1
                elif side == 'left':
                    x, y = 0, random.randrange(GRID_SIZE)
                elif side == 'right':
                    x, y = GRID_SIZE - 1, random.randrange(GRID_SIZE)
            self.grid[x, y] = 3
            self.start_points.append((x, y))

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])