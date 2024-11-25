import pygame
import math

# Constants
WIDTH = 800
HEIGHT = 600
HEX_SIZE = 30  # Size of the hexagon
HEX_COLOR = (255, 255, 255)  # White (Fill Color)
BORDER_COLOR = (0, 0, 0)  # Black (Border Color)
SELECTED_COLOR = (255, 0, 0)  # Red
NEIGHBOR_COLOR = (0, 255, 0)  # Green
BACKGROUND_COLOR = (0, 0, 0)  # Black
def AvailablePositions(hex_map, turn):
    result = []
    s = set();
    if turn == "W":
        if hex_map.Length == 0:
            return True
        elif hex_map.Length ==1 :
            keys = list(hex_map.map.keys())
            return  hex_map.get_Empty_neighbors(keys[0][0],keys[0][1] )
        else:
            keys = list(hex_map.map.keys())
            List = []
            for key in keys:
                List += hex_map.get_Empty_neighbors(key[0], key[1])
                for element in List:
                    s.add((element[0], element[1]))

            for element in s:
                flag = 0
                for element2 in List:
                    if (element[0] == element2[0]) and (element[1] == element2[1]) and element2[2] == "B":
                        flag = 1
                if flag == 0:
                    result.append((element[0], element[1]))

    if turn == "B":
        if hex_map.Length == 0:
            return True
        elif hex_map.Length == 1:
            keys = list(hex_map.map.keys())
            return hex_map.get_Empty_neighbors(keys[0][0], keys[0][1])
        else:
            keys = list(hex_map.map.keys())
            List = []
            for key in keys:
                List += hex_map.get_Empty_neighbors(key[0], key[1])
                for element in List:
                    s.add((element[0], element[1]))

            for element in s:
                flag = 0
                for element2 in List:
                    if (element[0] == element2[0]) and (element[1] == element2[1]) and (element2[2] == "W"):
                        flag = 1
                if flag == 0:
                    result.append((element[0], element[1]))

    return result
    
# Queen available positions
# to be modified when will_break_the_hive() is implemented
def Available_Positions_Queen(hex_map, q, r):
    result = []
    empty_neighbours = hex_map.get_Empty_neighbors(q, r)
    print(empty_neighbours)
    for element in empty_neighbours:
        neighbors = hex_map.get_neighbors(element[0], element[1])
        neighbors.remove((q, r))
        if len(neighbors) != 0:
            result.append((element[0], element[1]))
        print(neighbors)

    return result
    
# HexMap class to store pieces on the hex map
class HexMap:
    def __init__(self):
        self.map = {}
        self.queen_placed = {"W": False, "B": False}
        self.White_turn_count = 0
        self.Black_turn_count = 0
        self.Turn = "W"
        self.Length = 0

    def add_piece(self, q, r, name, color):
        self.Length += 1
        self.map[(q, r)] = (name, color)
        if color == "W":
            self.White_turn_count += 1
            self.Turn = "W"
        else:
            self.Black_turn_count += 1
            self.Turn = "B"
        if name == "Queen":
            if color == "W":
                self.queen_placed["W"] = True
            else:
                self.queen_placed["B"] = True

    def get_piece(self, q, r):
        return self.map.get((q, r), None)

    def get_neighbors(self, q, r):
        """Returns a list of neighboring hexes for the given hex."""
        directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
        return [(q + dq, r + dr) for dq, dr in directions if (q + dq, r + dr) in self.map]

    def get_Empty_neighbors(self, q, r):
        """Returns a list of neighboring hexes for the given hex."""
        directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
        return [(q + dq, r + dr, self.map[(q, r)][1]) for dq, dr in directions if (q + dq, r + dr) not in self.map]


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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hex Map GUI")
    clock = pygame.time.Clock()

    hex_map = HexMap()

    hex_map.add_piece(0, 0, "Queen", "W")

    print(AvailablePositions(hex_map, "B"))

    selected_hex = None

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Draw hexagons
        for q in range(-5, 6):
            for r in range(-5, 6):
                x, y = hex_to_pixel(q, r)
                x += WIDTH // 2
                y += HEIGHT // 2
                fill_color = HEX_COLOR

                if (q, r) == selected_hex:
                    fill_color = SELECTED_COLOR

                draw_hexagon(screen, x, y, fill_color, BORDER_COLOR)

                piece = hex_map.get_piece(q, r)

                if piece:
                    draw_text_centered(screen, piece[0], x, y)

        # Highlight neighbors
        if selected_hex:
            neighbors = hex_map.get_neighbors(*selected_hex)
            for neighbor in neighbors:
                nq, nr = neighbor
                nx, ny = hex_to_pixel(nq, nr)
                nx += WIDTH // 2
                ny += HEIGHT // 2
                draw_hexagon(screen, nx, ny, NEIGHBOR_COLOR, BORDER_COLOR)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_hex = pixel_to_hex(mouse_x, mouse_y)  # Get Q,r of the Selected Hex
                print(f"Selected Hex: {selected_hex}")
        display_avail(AvailablePositions(hex_map, "B"), screen)

        pygame.display.flip()
        clock.tick(30)  # Limit the frame rate to 30 FPS

    pygame.quit()


if __name__ == "__main__":
    main()




