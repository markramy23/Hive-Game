import math
import pygame
# Constants
INTMIN = -2**31
INTMAX =  2**31
WIDTH = 800
HEIGHT = 600
HEX_SIZE = 30  # Size of the hexagon
HEX_COLOR = (255, 255, 255)  # White (Fill Color)
BORDER_COLOR = (0, 0, 0)  # Black (Border Color)
SELECTED_COLOR = (255, 0, 0)  # Red
NEIGHBOR_COLOR = (0, 255, 0)  # Green
BACKGROUND_COLOR = (0, 0, 0)  # Black
def get_neighbors(pos, grid):
    """Get neighbors of a given position (q, r)."""
    directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
    q, r = pos
    return [(q + dq, r + dr) for dq, dr in directions if (q + dq, r + dr) in grid]


def hex_round(q, r):
    """Round fractional hex coordinates to the nearest hexagonal integer coordinates."""
    s = -q - r
    q_round = round(q)
    r_round = round(r)
    s_round = round(s)

    q_diff = abs(q_round - q)
    r_diff = abs(r_round - r)
    s_diff = abs(s_round - s)

    if q_diff > r_diff and q_diff > s_diff:
        q_round = -r_round - s_round
    elif r_diff > s_diff:
        r_round = -q_round - s_round

    return int(q_round), int(r_round)


# display available positions on the screen
def display_avail(list, screen):
    for element in list:
        x, y = hex_to_pixel(element[0], element[1])
        x += WIDTH // 2
        y += HEIGHT // 2
        draw_hexagon(screen, x, y, (255, 0, 255), BORDER_COLOR)


# Utility functions
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


def hex_to_pixel(q, r):
    """Convert hexagonal (q, r) coordinates to pixel coordinates (x, y)."""
    x = HEX_SIZE * (3 / 2 * q)
    y = HEX_SIZE * (math.sqrt(3) * (r + q / 2))
    return x, y


def pixel_to_hex(x, y):
    """Convert pixel (x, y) coordinates to hexagonal (q, r) coordinates."""
    x -= WIDTH // 2
    y -= HEIGHT // 2
    q = (2 / 3 * x) / HEX_SIZE
    r = (-1 / 3 * x + math.sqrt(3) / 3 * y) / HEX_SIZE
    return hex_round(q, r)

