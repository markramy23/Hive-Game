# Function to draw a single hexagon with its content (duplicated)
from Utilities import  *
import pygame
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
