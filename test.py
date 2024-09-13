import pygame
import sys

# Initialize pygame
pygame.init()

# Define constants
TILE_SIZE = 100  # Each tile is 100x100 pixels
BOARD_SIZE = 5   # 5x5 board
WINDOW_SIZE = TILE_SIZE * BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

# Create the display window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("5x5 Tiles Board")

# Function to draw the board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Alternate between colors for each tile
            color = COLORS[(row + col) % len(COLORS)]
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            # Draw grid lines for clarity (optional)
            pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with a background color (optional)
    screen.fill(WHITE)

    # Draw the tiled board
    draw_board()

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
