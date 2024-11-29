# Function to draw a single hexagon with its content (duplicated)
from Utilities import  *
import pygame
import math

# Screen dimensions
screen_width, screen_height = 1550, 790
HEX_SIZE_Board = 25  # Size of the hexagon
HEX_SIZE_MENU = 25 #Size of Menu Player
HEX_COLOR = (255, 255, 255)  # White (Fill Color)
BLACK =(0,0,0) # Black
BORDER_COLOR = BLACK  # Black (Border Color)
SELECTED_COLOR = (255, 0, 0)  # Red
NEIGHBOR_COLOR = (0, 255, 0)  # Green
BACKGROUND_COLOR = (0, 0, 0)  # Black
WHITE_PLAYER = (255, 255, 255)  # White
BLACK_PLAYER = (0, 255, 255)  # Black

#Background
background = pygame.image.load("./images/bg2.jpg")

#Player background
player_background = pygame.image.load("./images/Player_background.png")

#icons
blackIcon = pygame.image.load("./images/BlackIcon.png")
whiteIcon = pygame.image.load("./images/WhiteIcon.png")

#animals
Ant = pygame.image.load("./images/Ant.png")
Queen = pygame.image.load("./images/QuuenBee.png")
Beetle = pygame.image.load("./images/Beetle.png")
GrassHopper= pygame.image.load("./images/GrassHopper.png")
Spider = pygame.image.load("./images/Spider.png")

# Draw functions
def draw_hexagon(surface, x, y, fill_color, border_color):
    """Draw a single hexagon centered at (x, y) with a solid color and a border."""
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + HEX_SIZE * math.cos(angle)
        py = y + HEX_SIZE * math.sin(angle)
        points.append((px, py))
    # Draw the filled hexagon
    pygame.draw.polygon(surface, fill_color, points)
    # Draw the border of the hexagon
    pygame.draw.polygon(surface, border_color, points, width=1)  # Border width = 1 pixel


def draw_text_centered(surface, text, x, y, font_size=20, color=(255, 255, 255)):
    """Draw text centered at (x, y)."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_single_hex(q, r, camera_x, camera_y, screen, hex_map, selected_hex):
    """Draws a single hexagon at the specified (q, r) position."""
    x, y = hex_to_pixel(q, r, HEX_SIZE_Board)
    x += screen_width // 2 + camera_x  # Apply camera position
    y += screen_height // 2 + camera_y

    # Determine the fill color
    fill_color = SELECTED_COLOR if (q, r) == selected_hex else HEX_COLOR

    # Draw the hexagon
    draw_hexagon(screen, x, y, fill_color, BORDER_COLOR, HEX_SIZE_Board)

    # Draw the piece, if it exists
    piece = hex_map.get_piece(q, r)
    if piece:
        draw_text_centered(screen, piece, x, y)

def draw_player(player1_name, player2_name, Players_type, screen):
    # Get the window size after setting the display mode
    window_width, window_height = pygame.display.get_surface().get_size()
    player_background = pygame.image.load("Player_background.png")
    screen.blit(player_background, (0, 0))
    screen.blit(player_background, (window_width - 250, 0))
    num_of_pieces = 11  # for one player

    # White Player
    name1 = font.render(player1_name, True, BLACK)
    screen.blit(whiteIcon, (window_width - 195, 10))
    screen.blit(name1, (window_width - 170, 10))

    # Black Player
    name2 = font.render(player2_name, True, BLACK)
    screen.blit(blackIcon, (55, 10))
    screen.blit(name2, (80, 10))

    # if Players_type is "Human-Human":
    # elif Players_type is "Human-AI":
    # elif Players_type is "AI-AI":

# display available positions on the screen
def display_avail(list, screen):
    for element in list:
        x, y = hex_to_pixel(element[0], element[1])
        x += WIDTH // 2
        y += HEIGHT // 2
        draw_hexagon(screen, x, y, (255, 0, 255), BORDER_COLOR)
