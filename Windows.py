import pygame
from Hex_map import HexMap
from Utilities import *
from GUI import *
from Available_positions import *

# Constants
WIDTH, HEIGHT = 400, 350
BACKGROUND_COLOR = (34, 85, 34)  # Dark green
BUTTON_COLOR = (50, 50, 50)  # Dark gray for inactive buttons
ACTIVE_BUTTON_COLOR = (100, 100, 100)  # Lighter gray for hover
TEXT_COLOR = (200, 200, 100)  # Yellowish text
BACK_BUTTON_COLOR = (0, 80, 0)  # Dark green for back button
DISCONNECT_BUTTON_COLOR = (150, 0, 0)  # Dark red for disconnect button
FONT_SIZE = 30
BUTTON_HEIGHT = 50
Logo = pygame.image.load("./images/Logo_1.png")

def mainwindow(screen):
    from modes import Human_VS_Human , Human_VS_AI
    global screen_width, screen_height
    pygame.init()
    # Set up a maximized window with minimize, maximize, and close icons
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()

    human_button = pygame.Rect(screen_width // 2 - 200, 300, 400, 80)
    ai_button = pygame.Rect(screen_width // 2 - 200, 400, 400, 80)
    ai_vs_ai_button = pygame.Rect(screen_width // 2 - 200, 500, 400, 80)
    Quit_Button = pygame.Rect(screen_width // 2 - 200, 600, 400, 80)

    running = True
    while running:
        screen.fill((170, 170, 170))
        screen.blit(HomePage, (0, 0))
        #draw_text_centered(screen, "Hive Game", screen_width // 2, 250, font_size=60)
        #screen.blit(Logo, (screen_width // 2 -152, 30))
        human_hovered = draw_button(screen, "Human vs Human", human_button)
        ai_hovered = draw_button(screen, "Human vs AI", ai_button)
        ai_vs_ai_hovered = draw_button(screen, "AI vs AI", ai_vs_ai_button)
        Quit_hovered = draw_button(screen,"Exit Game",Quit_Button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if human_hovered:
                    Human_VS_Human(screen)
                elif ai_hovered:
                    Human_VS_AI(screen)
                elif ai_vs_ai_hovered:
                    print("AI vs AI selected!")
                elif Quit_hovered:
                    running =False
                    pygame.quit()

        pygame.display.flip()
        clock.tick(30)
        
def render_menu_window(parent_screen):
    """
    Renders a smaller overlay window over the parent screen.
    The smaller window contains buttons like "Continue," "Go to Main Menu," and "Exit Game."
    """
    pygame.init()
    overlay_surface = pygame.Surface((WIDTH, HEIGHT))  # Create a smaller overlay
    overlay_surface.fill((50, 50, 50))  # Background color for overlay
    overlay_rect = overlay_surface.get_rect(center=parent_screen.get_rect().center)  # Center it

    font = pygame.font.Font(None, FONT_SIZE)
    clock = pygame.time.Clock()
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    Continue_button = pygame.Rect(screen_width // 2 - 150, 295, screen_width // 8 + 100, BUTTON_HEIGHT + 25)
    Main_Menu_button = pygame.Rect(screen_width // 2 - 150, 395, screen_width // 8 + 100, BUTTON_HEIGHT + 25)
    Exit_Game_button = pygame.Rect(screen_width // 2 - 150, 495, screen_width // 8 + 100, BUTTON_HEIGHT + 25)
   

    running = True
    flag_break = False

    while running:
        # Render the dimmed parent screen as a background
        #parent_screen.fill((0, 0, 0, 150))  # Slightly transparent black overlay
        parent_screen.blit(overlay_surface, overlay_rect.topleft)  # Blit smaller window

        # Draw buttons
        draw_text_centered(parent_screen,"Hive Game", screen_width // 2, 230, font_size=60)
        Continue_hovered = draw_button(parent_screen, "Continue", Continue_button)
        Main_Menu_hovered = draw_button(parent_screen, "Go to Main Menu", Main_Menu_button)
        Exit_Game_hovered = draw_button(parent_screen, "Exit Game", Exit_Game_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running =False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Continue_hovered:
                    flag_break = True
                elif Main_Menu_hovered:
                    mainwindow(parent_screen)
                elif Exit_Game_hovered:
                    running =False
                    pygame.quit()
                    
        # Update the display
        pygame.display.flip()
        clock.tick(30)
        if(flag_break == True):
            break #break to function which called you
