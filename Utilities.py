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


def hex_to_pixel(q, r,hex_size):
    """Convert hexagonal (q, r) coordinates to pixel coordinates (x, y)."""
    x = hex_size * (3/2 * q)
    y = hex_size * (math.sqrt(3) * (r + q / 2))
    x += screen_width // 2
    y +=screen_height // 2
    return x, y


def pixel_to_hex(x, y):
    """Convert pixel (x, y) coordinates to hexagonal (q, r) coordinates."""
    x -= WIDTH // 2
    y -= HEIGHT // 2
    q = (2 / 3 * x) / HEX_SIZE
    r = (-1 / 3 * x + math.sqrt(3) / 3 * y) / HEX_SIZE
    return hex_round(q, r)

#Function Mapping of hex coordinates to their respective numbers 
def get_hex_number(q, r):
    hex_map = {
        (-19, 1): 0, (-17, 0): 1, (-15, -1): 2, (-19, 2): 3,
        (-17, 1): 4, (-15, 0): 5, (-19, 3): 6, (-17, 2): 7,
        (-15, 1): 8, (-19, 4): 9, (-17, 3): 10,(19, -18): 11, 
        (17, -17): 12, (15, -16): 13,(19, -17): 14, (17, -16): 15, 
        (15, -15): 16, (19, -16): 17,(17, -15): 18, (15, -14): 19,
        (19, -15): 20, (17, -14): 21
    }
    
    # Return the number if the hex coordinate exists, or None otherwise
    return hex_map.get((q, r), None)
