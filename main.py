import pygame

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear the screen
    pygame.display.flip()

pygame.quit()