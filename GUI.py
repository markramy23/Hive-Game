# Function to draw a single hexagon with its content (duplicated)
from Utilities import  *
import pygame
import math

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 20)

# Screen dimensions
HEX_SIZE_Board = 25  # Size of the hexagon
HEX_SIZE_MENU = 25 #Size of Menu Player
HEX_COLOR = (255, 255, 255)  # White (Fill Color)
BLACK =(0,0,0) # Black
BORDER_COLOR = (139,135,116)  # Black (Border Color)
SELECTED_COLOR = (255, 0, 0)  # Red
NEIGHBOR_COLOR = (0, 255, 0)  # Green
BACKGROUND_COLOR = (255, 255, 255)  # Black
WHITE_PLAYER = (230, 211, 160)  # White
BLACK_PLAYER = (27,27,27)  # Black
BORDER_COLOR_2 =(0,255,255)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
TEXT_COLOR = (255, 255, 255)
#Background
background = pygame.image.load("./images/bg2.jpg")
HomePage = pygame.image.load("./images/Home.png")
#Player background
player_background = pygame.image.load("./images/Player_background.png")
score_background = pygame.image.load("./images/background.png")

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
def draw_hexagon(surface, x, y, fill_color, border_color , hex_size):
    """Draw a single hexagon centered at (x, y) with a solid color and a border."""
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + hex_size * math.cos(angle)  #10 + 30 * 1/2 = 10 + 15 = 25 
        py = y + hex_size * math.sin(angle) 
        points.append((px, py)) #[(),(),()]
    # Draw the filled hexagon
    pygame.draw.polygon(surface, fill_color, points)
    # Draw the border of the hexagon
    pygame.draw.polygon(surface, border_color, points, width=3)  # Border width = 1 pixel

def draw_border(surface, x, y, border_color , hex_size):
    """Draw a single hexagon centered at (x, y) with a solid color and a border."""
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        px = x + hex_size * math.cos(angle)  #10 + 30 * 1/2 = 10 + 15 = 25 
        py = y + hex_size * math.sin(angle) 
        points.append((px, py)) #[(),(),()]
    # Draw the border of the hexagon
    pygame.draw.polygon(surface, border_color, points, width=3)  # Border width = 1 pixel


def draw_text_centered(surface, text, x, y, font_size=20, color=(255, 255, 255)):
    """Draw text centered at (x, y)."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# def draw_single_hex(q, r, camera_x, camera_y, screen, hex_map, selected_hex):
#     """Draws a single hexagon at the specified (q, r) position."""
#     x, y = hex_to_pixel(q, r, HEX_SIZE_Board)
#     x += screen_width // 2 + camera_x  # Apply camera position
#     y += screen_height // 2 + camera_y

#     # Determine the fill color
#     fill_color = SELECTED_COLOR if (q, r) == selected_hex else HEX_COLOR

#     # Draw the hexagon
#     draw_hexagon(screen, x, y, fill_color, BORDER_COLOR, HEX_SIZE_Board)

#     # Draw the piece, if it exists
#     piece = hex_map.get_piece(q, r)
#     if piece:
#         draw_text_centered(screen, piece, x, y)

def draw_player(player1_name, player2_name, screen):
    # Get the window size after setting the display mode
    window_width, window_height = pygame.display.get_surface().get_size()
    player_background = pygame.image.load("./images/Player_background.png")
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
def display_avail(list, screen,screen_width,screen_height):
    for element in list:
        x, y = hex_to_pixel(element[0], element[1])
        x += screen_width // 2
        y += screen_height // 2
        draw_hexagon(screen, x, y, (255, 0, 255), BORDER_COLOR)

def draw_button(surface, text, rect, font_size=40, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
    """
    Draws a button on the surface and checks if it is hovered or clicked.

    Args:
        surface: The surface to draw on.
        text: The text to display on the button.
        rect: The rectangle defining the button's position and size.
        font_size: The font size of the text.
        color: The normal button color.
        hover_color: The button color when hovered.

    Returns:
        A tuple (is_hovered, is_clicked) where both are booleans.
    """
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    is_hovered = rect.collidepoint(mouse_pos)
    is_clicked = is_hovered and mouse_buttons[0]

    button_color = hover_color if is_hovered else color
    pygame.draw.rect(surface, button_color, rect, border_radius=10)
    draw_text_centered(surface, text, rect.centerx, rect.centery, font_size, TEXT_COLOR)

    return is_hovered, is_clicked

def draw_hexagons(positions, color1, color2,screen_width,screen_height,hex_map,screen,hex_map_on_menu):
    for x, y in positions:
        new_x = pixel_to_hex(x,y,HEX_SIZE_Board,screen_width,screen_height)[0]
        new_y = pixel_to_hex(x,y,HEX_SIZE_Board,screen_width,screen_height)[1]
        if(get_hex_number(pixel_to_hex(x,y,HEX_SIZE_Board,screen_width,screen_height)[0],pixel_to_hex(x,y,HEX_SIZE_Board,screen_width,screen_height)[1]) == None): 
            x+=hex_map.x
            y+=hex_map.y
            #print(x,y)
        #flag_to_draw = True
        result = hex_map.get_piece(new_x,new_y)
        if(result != None):
            name3 , color3 , img3 = result
            if(color3 == "W"):
                color1 = WHITE_PLAYER
            else:
                color1 = BLACK_PLAYER

        draw_hexagon(screen, x, y, color1, color2, HEX_SIZE_MENU) 
        q1, r1 = pixel_to_hex(x-hex_map.x, y-hex_map.y, HEX_SIZE_MENU,screen_width,screen_height)#Right q and r
        q, r = pixel_to_hex(x, y, HEX_SIZE_MENU,screen_width,screen_height)#Right q and r
        piece1 = hex_map_on_menu.get_piece(q, r)
        piece2 = hex_map.get_piece(q1,r1)
        if piece1:
            name, color, img = piece1
            if img:
                img_rect = img.get_rect(center=(x, y))
                screen.blit(img, img_rect)
        if piece2:
            name, color, img = piece2
            if img:
                img_rect = img.get_rect(center=(x, y))
                screen.blit(img, img_rect)
    
def Test_Map(screen, hex_map, selected_hex, HEX_SIZE_Board, HEX_COLOR, SELECTED_COLOR, BORDER_COLOR,screen_width,screen_height):

    '''Draws the hexagonal map on the screen.

    Args:
        screen (Surface): The Pygame screen surface to draw on.
        hex_map (HexMap): The hex map containing hex data.
        selected_hex (tuple): The coordinates of the selected hexagon.
        HEX_SIZE_Board (int): The size of the hexagons.
        HEX_COLOR (tuple): The color of the hexagons.
        SELECTED_COLOR (tuple): The color of the selected hexagon.
        BORDER_COLOR (tuple): The color of the hexagon borders.'''

    for q in range(-10  , 10):
        for r in range(-10, 10):
            x, y = hex_to_pixel(q, r, HEX_SIZE_Board,screen_width,screen_height)
            x+=hex_map.x
            y+=hex_map.y
            fill_color = HEX_COLOR

            if (q, r) == selected_hex:
                fill_color = SELECTED_COLOR

            draw_hexagon(screen, x, y, fill_color, BORDER_COLOR, HEX_SIZE_Board)

def draw_next_move(draw_flag, positions, hex_map, HEX_SIZE_Board, screen, screen_width, screen_height, BORDER_COLOR_2):
    if draw_flag:
        # Iterate through the list of positions
        for position in positions: 
            x, y = hex_to_pixel(position[0], position[1], HEX_SIZE_Board, screen_width, screen_height)
            x += hex_map.x
            y += hex_map.y
            draw_border(screen, x, y, BORDER_COLOR_2, HEX_SIZE_Board)
