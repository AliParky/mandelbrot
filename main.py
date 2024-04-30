import pygame
import numpy as np

# Define resolution constants
WIDTH, HEIGHT = 800, 800

# Function to calculate Mandelbrot set
def calculate_mandelbrot(c, max_iter=100):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

# Function to generate Mandelbrot matrix
def generate_mandelbrot_matrix(center_x, center_y, zoom):
    mandelbrot_matrix = np.zeros((WIDTH, HEIGHT))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            real = (x - WIDTH // 2) / (WIDTH // 2) * zoom + center_x
            imag = (y - HEIGHT // 2) / (HEIGHT // 2) * zoom + center_y
            mandelbrot_matrix[y, x] = calculate_mandelbrot(complex(real, imag))
    return mandelbrot_matrix

# Function to color a pixel
def color_pixel(iteration):
    return (iteration, iteration, iteration)

# Function to draw Mandelbrot set on a surface
def draw_mandelbrot(mandelbrot_matrix, surface):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            iteration = mandelbrot_matrix[y, x]
            color = color_pixel(iteration)
            surface.set_at((x, y), color)

# Function to convert screen coordinates to Mandelbrot set coordinates
def screen_to_mandelbrot(x, y, center_x, center_y):
    real = ((x - WIDTH // 2) / (WIDTH // 2)) + center_x
    imag = ((y - HEIGHT // 2) / (HEIGHT // 2)) + center_y
    return real, imag

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define center coordinates
center_x, center_y = 0.0, 0.0

# Define zoom level
zoom = 1.0

# Generate Mandelbrot matrix
mandelbrot_matrix = generate_mandelbrot_matrix(center_x, center_y, zoom)

# Create a new surface and draw the Mandelbrot set on it
mandelbrot_surface = pygame.Surface((WIDTH, HEIGHT))
draw_mandelbrot(mandelbrot_matrix, mandelbrot_surface)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(mandelbrot_surface, (0, 0))

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw a square around the mouse position
    pygame.draw.rect(screen, (255, 255, 0), (mouse_x - 50, mouse_y - 50, 100, 100), 2)

    pygame.display.flip()

pygame.quit()