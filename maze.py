import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Maze dimensions
cols, rows = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Create a grid of cells
grid = []
for y in range(rows):
    grid.append([])
    for x in range(cols):3
        grid[y].append(1)  # 1 represents a wall

# Carve out a maze using a simple algorithm
def carve_maze(x, y):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2
        if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 1:
            grid[ny][nx] = 0
            grid[ny - dy][nx - dx] = 0
            carve_maze(nx, ny)

# Start carving from the top-left corner
grid[1][1] = 0
carve_maze(1, 1)

# Player position
player_x, player_y = 1, 1

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and grid[player_y][player_x - 1] == 0:
        player_x -= 1
    if keys[pygame.K_RIGHT] and grid[player_y][player_x + 1] == 0:
        player_x += 1
    if keys[pygame.K_UP] and grid[player_y - 1][player_x] == 0:
        player_y -= 1
    if keys[pygame.K_DOWN] and grid[player_y + 1][player_x] == 0:
        player_y += 1

    # Draw the maze
    screen.fill(BLACK)
    for y in range(rows):
        for x in range(cols):
            color = WHITE if grid[y][x] == 1 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the player
    pygame.draw.rect(screen, BLUE, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

pygame.quit()
