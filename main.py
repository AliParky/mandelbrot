import pygame
import numpy as np
import threading

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
def generate_mandelbrot_matrix(center_x, center_y, zoom, resolution=WIDTH):
    mandelbrot_matrix = np.zeros((WIDTH, HEIGHT))
    step = WIDTH // resolution
    for x in range(0, WIDTH, step):
        for y in range(0, HEIGHT, step):
            real = (x - WIDTH // 2) / (WIDTH // 2) * zoom + center_x
            imag = (y - HEIGHT // 2) / (HEIGHT // 2) * zoom + center_y
            mandelbrot_matrix[y:y+step, x:x+step] = calculate_mandelbrot(complex(real, imag))
    return mandelbrot_matrix

# Function to color a pixel
def color_pixel(iteration, max_iter=100):
    scaled_value = int((iteration / max_iter) * 255)
    return (scaled_value, scaled_value, scaled_value)

# Function to draw Mandelbrot set on a surface
def draw_mandelbrot(mandelbrot_matrix, surface):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            iteration = mandelbrot_matrix[y, x]
            color = color_pixel(iteration)
            surface.set_at((x, y), color)

# Function to convert screen coordinates to Mandelbrot set coordinates
def screen_to_mandelbrot(x, y, center_x, center_y, zoom):
    real = ((x - WIDTH // 2) / (WIDTH // 2) * zoom) + center_x
    imag = ((y - HEIGHT // 2) / (HEIGHT // 2) * zoom) + center_y
    return real, imag

# Global variable to store the result of the update_mandelbrot function
mandelbrot_surface_result = None

# Function to update Mandelbrot set with new center and zoom
def update_mandelbrot(center_x, center_y, zoom):
    global mandelbrot_surface_result
    mandelbrot_matrix = generate_mandelbrot_matrix(center_x, center_y, zoom)
    mandelbrot_surface_result = pygame.Surface((WIDTH, HEIGHT))
    draw_mandelbrot(mandelbrot_matrix, mandelbrot_surface_result)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define center coordinates
center_x, center_y = 0.0, 0.0

# Define zoom level
zoom = 2

# Define zoom rectangle size
zoom_rect_size = 100

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                center_x, center_y = screen_to_mandelbrot(mouse_x, mouse_y, center_x, center_y, zoom)
                zoom *= zoom_rect_size / WIDTH
                thread = threading.Thread(target=update_mandelbrot, args=(center_x, center_y, zoom))
                thread.start()
                thread.join()
                mandelbrot_surface = mandelbrot_surface_result
            elif event.button == 4:  # Scroll up
                zoom_rect_size *= 1.1
            elif event.button == 5:  # Scroll down
                zoom_rect_size /= 1.1

    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(mandelbrot_surface, (0, 0))

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw a square around the mouse position
    pygame.draw.rect(screen, (255, 255, 0), (mouse_x - zoom_rect_size // 2, mouse_y - zoom_rect_size // 2, zoom_rect_size, zoom_rect_size), 2)

    pygame.display.flip()

pygame.quit()