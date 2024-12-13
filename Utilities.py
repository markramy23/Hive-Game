import math
import pygame

# Constants
INTMIN = -2**31
INTMAX =  2**31
#WIDTH = 800
#HEIGHT = 600
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


def hex_to_pixel(q, r,hex_size,screen_width,screen_height):
    """Convert hexagonal (q, r) coordinates to pixel coordinates (x, y)."""
    x = hex_size * (3/2 * q)
    y = hex_size * (math.sqrt(3) * (r + q / 2))
    x += screen_width // 2
    y +=screen_height // 2
    return x, y

def pixel_to_hex(x, y,hex_size,screen_width,screen_height):
    """Convert pixel (x, y) coordinates to hexagonal (q, r) coordinates."""
    x -= screen_width // 2
    y -= screen_height // 2
    q = (2/3 * x) / hex_size
    r = (-1/3 * x + math.sqrt(3)/3 * y) / hex_size
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
    
def add_pieces(positions, color ,piece_images,pieces,screen_width,screen_height,hex_map_on_menu):
    from GUI import HEX_SIZE_MENU
    piece_index = 0
    for name, count in pieces.items():
        for i in range(1, count + 1):
            if piece_index >= len(positions):
                break
            x, y = positions[piece_index]
            q, r = pixel_to_hex(x, y, HEX_SIZE_MENU,screen_width,screen_height)
            img = piece_images[name]
            hex_map_on_menu.add_piece(q, r, f"{name}{i}", color, img)
            piece_index += 1
def change_map_position(event, dragging, last_mouse_pos, hive):
    """
    Handle camera movement by dragging the map with the mouse, updating the hive's position.
    
    Args:
        event: The current pygame event.
        dragging: Boolean indicating if the map is being dragged.
        last_mouse_pos: Tuple of the last recorded mouse position.
        hive: The hive object, with x and y properties for position.
    
    Returns:
        Updated dragging state and last mouse position.
    """
    # if hex_map.x < 50 or hex_map.y < 50:
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:  # Right mouse button starts dragging
            dragging = True
            last_mouse_pos = pygame.mouse.get_pos()
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 3:  # Right mouse button stops dragging
            dragging = False
    elif event.type == pygame.MOUSEMOTION:
        if dragging:
            current_mouse_pos = pygame.mouse.get_pos()
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            # Update the hive's position
            #if hive.x+dx >100  :
                #hive.x = hive.x
            #else:
            hive.x += dx
            hive.y += dy
            last_mouse_pos = current_mouse_pos

    return dragging, last_mouse_pos
    # else:
    #     hex_map.x = 0
    #     hex_map.y =0
    #     return False , last_mouse_pos
def general_get_hex_number(q, r,positions_black,positions_white,screen_width,screen_height):
    from GUI import HEX_SIZE_Board
    # Mapping of hex coordinates to their respective numbers
    hex_map = { 
        pixel_to_hex(positions_black[0][0]  , positions_black[0][1],HEX_SIZE_Board,screen_width,screen_height)  : 0   ,
        pixel_to_hex(positions_black[1][0]  , positions_black[1][1],HEX_SIZE_Board,screen_width,screen_height)  : 1   ,     
        pixel_to_hex(positions_black[2][0]  , positions_black[2][1],HEX_SIZE_Board,screen_width,screen_height)  : 2   ,
        pixel_to_hex(positions_black[3][0]  , positions_black[3][1],HEX_SIZE_Board,screen_width,screen_height)  : 3   ,
        pixel_to_hex(positions_black[4][0]  , positions_black[4][1],HEX_SIZE_Board,screen_width,screen_height)  : 4   ,
        pixel_to_hex(positions_black[5][0]  , positions_black[5][1],HEX_SIZE_Board,screen_width,screen_height)  : 5   ,
        pixel_to_hex(positions_black[6][0]  , positions_black[6][1],HEX_SIZE_Board,screen_width,screen_height)  : 6   ,
        pixel_to_hex(positions_black[7][0]  , positions_black[7][1],HEX_SIZE_Board,screen_width,screen_height)  : 7   ,
        pixel_to_hex(positions_black[8][0]  , positions_black[8][1],HEX_SIZE_Board,screen_width,screen_height)  : 8   ,
        pixel_to_hex(positions_black[9][0]  , positions_black[9][1],HEX_SIZE_Board,screen_width,screen_height)  : 9   ,
        pixel_to_hex(positions_black[10][0] , positions_black[10][1],HEX_SIZE_Board,screen_width,screen_height) : 10  ,
        pixel_to_hex(positions_white[0][0]  , positions_white[0][1],HEX_SIZE_Board,screen_width,screen_height)  : 11  ,
        pixel_to_hex(positions_white[1][0]  , positions_white[1][1],HEX_SIZE_Board,screen_width,screen_height)  : 12  ,
        pixel_to_hex(positions_white[2][0]  , positions_white[2][1],HEX_SIZE_Board,screen_width,screen_height)  : 13  ,
        pixel_to_hex(positions_white[3][0]  , positions_white[3][1],HEX_SIZE_Board,screen_width,screen_height)  : 14  ,
        pixel_to_hex(positions_white[4][0]  , positions_white[4][1],HEX_SIZE_Board,screen_width,screen_height)  : 15  ,
        pixel_to_hex(positions_white[5][0]  , positions_white[5][1],HEX_SIZE_Board,screen_width,screen_height)  : 16  ,
        pixel_to_hex(positions_white[6][0]  , positions_white[6][1],HEX_SIZE_Board,screen_width,screen_height)  : 17  ,
        pixel_to_hex(positions_white[7][0]  , positions_white[7][1],HEX_SIZE_Board,screen_width,screen_height)  : 18  ,
        pixel_to_hex(positions_white[8][0]  , positions_white[8][1],HEX_SIZE_Board,screen_width,screen_height)  : 19  ,
        pixel_to_hex(positions_white[9][0]  , positions_white[9][1],HEX_SIZE_Board,screen_width,screen_height)  : 20  ,
        pixel_to_hex(positions_white[10][0] , positions_white[10][1],HEX_SIZE_Board,screen_width,screen_height) : 21 
    }       

    # Return the number if the hex coordina te exists, or None otherwise    
    return hex_map.get((q, r), None)        
    #print(hex_to_pixel(-19, 1,HEX_SIZE_Boa rd)[0],hex_to_pixel(-19, 1,HEX_SIZE_Boa rd)[1])

# def reset_game():
#     from GUI import HEX_SIZE_Board
#     """
#     Resets the game state to start a new game.
#     This function should reset variables such as board state, turn trackers, etc.
#     """
#     global game_board, current_turn, scores
#     game_board = [[None for _ in range(HEX_SIZE_Board)] for _ in range(HEX_SIZE_Board)]  # Example for a grid-based game
#     current_turn = "white"  # Reset to the initial player
#     scores = {"white": 0, "black": 0}  # Example scores reset
#     # Add any other game-specific variables here
