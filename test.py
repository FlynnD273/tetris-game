import pygame

# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Check if a specific key is pressed
    if keys[pygame.K_w]:
        print("W key is pressed")
    if keys[pygame.K_s]:
        print("S key is pressed")

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
