import pygame
pygame.init()
win_width = 1200
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('My Game')

bg_color = (255, 255, 255)

# Set the size and position of the game character
char_width = 50
char_height = 50
# char_x = win_width / 2 - char_width / 2
# char_y = win_height - char_height - 10
char_x = 600
char_y = 550

# Set the speed at which the game character moves
char_speed = 1

# Set the game loop flag
running = True

# Start the game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    win.fill(bg_color)

    # Move the game character based on input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        char_x -= char_speed
    if keys[pygame.K_RIGHT]:
        char_x += char_speed
    if keys[pygame.K_UP]:
        char_y -= char_speed
    if keys[pygame.K_DOWN]:
        char_y += char_speed

    # Draw the game character
    pygame.draw.rect(win, (0, 0, 255), (char_x, char_y, char_width, char_height))

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
