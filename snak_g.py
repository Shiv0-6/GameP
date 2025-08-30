import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Set up the game window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define the snake and food
snake = [(250, 250)]
food = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
snake_speed = 5

# Create the game loop
game_over = False
while not game_over:
    # Handle user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_speed = (-5, 0)
            elif event.key == pygame.K_RIGHT:
                snake_speed = (5, 0)
            elif event.key == pygame.K_UP:
                snake_speed = (0, -5)
            elif event.key == pygame.K_DOWN:
                snake_speed = (0, 5)
    
    # Update the game state
    snake_x, snake_y = snake[-1]
    dx,dy = snake_speed
    new_snake_x = snake_x + dx
    new_snake_y = snake_y + dy
    snake.append((new_snake_x, new_snake_y))
    if food == (new_snake_x, new_snake_y):
        food = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    else:
        snake.pop(0)
    
    # Draw the game elements
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, [food[0], food[1], 10, 10])
    for x, y in snake:
        pygame.draw.rect(screen, WHITE, [x, y, 10, 10])
    pygame.display.update()

# Quit Pygame properly
pygame.quit()
