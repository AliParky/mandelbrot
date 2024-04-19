import pygame
import numpy as np

# Function to calculate Mandelbrot set
def calculate_mandelbrot(c, max_iter=100):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

# Function to generate Mandelbrot matrix
def generate_mandelbrot_matrix():
    mandelbrot_matrix = np.zeros((800, 800))
    for x in range(800):
        for y in range(800):
            real = (x - 400) / 400
            imag = (y - 400) / 400
            mandelbrot_matrix[y, x] = calculate_mandelbrot(complex(real, imag))
    return mandelbrot_matrix

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