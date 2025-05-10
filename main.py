import pygame
from grid import Grid, GRID_SIZE, CELL_SIZE, WIDTH, HEIGHT
from bfs import BFSSimulator
from astar import AStarSimulator
from kmeans import kmeans

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Disaster Response System")
    clock = pygame.time.Clock()

    grid = Grid()
    bfs_sim1 = BFSSimulator(grid, grid.start_points[0])
    bfs_sim2 = BFSSimulator(grid, grid.start_points[1])

    phase = 'bfs'
    clusters = []
    centroids = []
    priority_list = []
    cluster_colors = [PURPLE, ORANGE, TEAL]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        if phase == 'bfs':
            done1 = bfs_sim1.step()
            done2 = bfs_sim2.step()

            if len(grid.found_survivors) >= 50 or (done1 and done2):
                phase = 'clustering'

        elif phase == 'clustering':
            survivors = grid.found_survivors
            if survivors:
                points = [(x, y) for (x, y) in survivors]
                clusters, centroids = kmeans(points)
                cluster_sizes = [len(c) for c in clusters]
                sorted_indices = sorted(range(len(cluster_sizes)), key=lambda i: -cluster_sizes[i])
                priority_list = [(centroids[i], cluster_sizes[i]) for i in sorted_indices]
                print("Priority List:")
                for i, (center, size) in enumerate(priority_list):
                    print(f"Cluster {i+1}: Center {center}, Size {size}")

                for center in centroids:
                    min_dist = float('inf')
                    nearest_start = None
                    for start in grid.start_points:
                        dist = grid.heuristic(center, start)
                        if dist < min_dist:
                            min_dist = dist
                            nearest_start = start
                    astar_sim = AStarSimulator(grid, tuple(center), nearest_start)
                    while not astar_sim.finished:
                        astar_sim.step()
                    if astar_sim.path:
                        grid.paths[tuple(center)] = astar_sim.path
            phase = 'done'

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if grid.grid[x, y] == 1:
                    pygame.draw.rect(screen, GRAY, rect)
                elif grid.grid[x, y] == 2:
                    color = RED
                    for i, cluster in enumerate(clusters):
                        if (x, y) in cluster:
                            color = cluster_colors[i]
                            break
                    pygame.draw.rect(screen, color, rect)
                elif grid.grid[x, y] == 3:
                    pygame.draw.rect(screen, BLUE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

        if phase == 'bfs':
            for (x, y) in bfs_sim1.visited:
                rect = pygame.Rect(x*CELL_SIZE +5, y*CELL_SIZE +5, CELL_SIZE-10, CELL_SIZE-10)
                pygame.draw.rect(screen, YELLOW, rect)
            for (x, y) in bfs_sim2.visited:
                rect = pygame.Rect(x*CELL_SIZE +5, y*CELL_SIZE +5, CELL_SIZE-10, CELL_SIZE-10)
                pygame.draw.rect(screen, YELLOW, rect)
            if bfs_sim1.last_explored:
                x, y = bfs_sim1.last_explored
                rect = pygame.Rect(x*CELL_SIZE +5, y*CELL_SIZE +5, CELL_SIZE-10, CELL_SIZE-10)
                pygame.draw.rect(screen, ORANGE, rect)
            if bfs_sim2.last_explored:
                x, y = bfs_sim2.last_explored
                rect = pygame.Rect(x*CELL_SIZE +5, y*CELL_SIZE +5, CELL_SIZE-10, CELL_SIZE-10)
                pygame.draw.rect(screen, ORANGE, rect)

        if phase == 'done':
            for idx, (center, path) in enumerate(grid.paths.items()):
                color = cluster_colors[idx % len(cluster_colors)]
                for (x, y) in path:
                    rect = pygame.Rect(x*CELL_SIZE +10, y*CELL_SIZE +10, CELL_SIZE-20, CELL_SIZE-20)
                    pygame.draw.rect(screen, color, rect)
                cx, cy = center
                center_rect = pygame.Rect(cx*CELL_SIZE +15, cy*CELL_SIZE +15, CELL_SIZE-30, CELL_SIZE-30)
                pygame.draw.rect(screen, BLACK, center_rect)

        for (x, y) in grid.start_points:
            rect = pygame.Rect(x*CELL_SIZE +5, y*CELL_SIZE +5, CELL_SIZE-10, CELL_SIZE-10)
            pygame.draw.rect(screen, BLACK, rect)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()