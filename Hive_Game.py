import pygame

from Hex_map import HexMap
from Utilities import *
from Available_positions import *
import copy




def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hex Map GUI")
    clock = pygame.time.Clock()

    hex_map = HexMap()

    hex_map.add_piece(0, 0, "Queen", "W")
    hex_map.add_piece(1, 0, "Ant", "W")
    hex_map.add_piece(-1, 0, "Ant", "W")
    hex_map.add_piece(-1,-1, "Ant", "B")
    hex_map.add_piece(0,-2, "Ant", "B")
    hex_map.add_piece(2,-1, "Ant", "B")
    hex_map.add_piece(3,-2, "Ant", "B")
    hex_map.add_piece(3,-3, "Ant", "B")
    hex_map.add_piece(3,-4, "Spider", "B")
    hex_map.add_piece(0,-2, "Ant", "B")
    hex_map.add_piece(1,-3, "Ant", "B")
    hex_map.add_piece(1,-2, "Ant", "B")
    # hex_map.add_piece(0, 0, "Queen", "W")
    # hex_map.add_piece(1, 0, "Beetle", "B")
    # hex_map.add_piece(-1, 1, "Grasshopper", "W")
    # print(Available_Positions_Spider(hex_map, 3, 4))

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
        display_avail(Available_Positions_Spider(hex_map, 3, -4), screen)
        pygame.display.flip()
        clock.tick(30)  # Limit the frame rate to 30 FPS

    pygame.quit()


if __name__ == "__main__":
    main()




