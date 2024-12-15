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
    from modes import Human_VS_Human , Human_VS_AI ,AI_VS_AI
    global screen_width, screen_height
    pygame.init()
    # Set up a maximized window with minimize, maximize, and close icons
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()

    human_button        = pygame.Rect(screen_width // 2 - 200, 300, 400, 80)
    ai_button           = pygame.Rect(screen_width // 2 - 200, 400, 400, 80)
    ai_vs_ai_button     = pygame.Rect(screen_width // 2 - 200, 500, 400, 80)
    Change_names_Button = pygame.Rect(screen_width // 2 - 200, 600, 400, 80)
    Quit_Button         = pygame.Rect(screen_width // 2 - 200, 700, 400, 80)


    running = True
    while running:
        screen.fill((170, 170, 170))
        screen.blit(HomePage, (0, 0))
        #draw_text_centered(screen, "Hive Game", screen_width // 2, 250, font_size=60)
        #screen.blit(Logo, (screen_width // 2 -152, 30))
        human_hovered,is_clicked        = draw_button( screen , "Human vs Human"       , human_button        )
        ai_hovered,is_clicked           = draw_button( screen , "Human vs Computer"    , ai_button           )
        ai_vs_ai_hovered,is_clicked     = draw_button( screen , "Computer vs Computer" , ai_vs_ai_button     )
        Change_names_hovered,is_clicked = draw_button( screen , "Change Names"         , Change_names_Button )
        Quit_hovered,is_clicked         = draw_button( screen , "Exit Game"            , Quit_Button         )

        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if human_hovered:
                    Human_VS_Human(screen)
                elif ai_hovered:
                    Difficulty_Human_vs_AI(screen)
                elif ai_vs_ai_hovered:
                    Difficulty_AI_vs_AI(screen)
                elif Change_names_hovered:
                    change_names_window(screen)
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
        Continue_hovered,is_clicked = draw_button(parent_screen, "Continue", Continue_button)
        Main_Menu_hovered,is_clicked = draw_button(parent_screen, "Go to Main Menu", Main_Menu_button)
        Exit_Game_hovered,is_clicked = draw_button(parent_screen, "Exit Game", Exit_Game_button)

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

def Win_Lose_window(parent_screen,depth1,depth2,winner_name,Match_result,Called_from):
    """
    Renders a smaller overlay window over the parent screen.
    The smaller window contains buttons like "Continue," "Go to Main Menu," and "Exit Game."
    """
    from modes import Human_VS_Human , Human_VS_AI ,AI_VS_AI
    pygame.init()
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    
    overlay_surface = pygame.Surface((screen_width, screen_height//8))  # Create a smaller overlay
    overlay_surface.fill((250, 250, 250))  # Background color for overlay
    overlay_rect = overlay_surface.get_rect(topleft=(0, 0))  # top it

    overlay_surface_2 = pygame.Surface((WIDTH, HEIGHT))  # Create a smaller overlay
    overlay_surface_2.fill((50, 50, 50))  # Background color for overlay
    overlay_rect_2 = overlay_surface_2.get_rect(center=parent_screen.get_rect().center)  # Center it

    # over_font = pygame.font.Font('freesansbold.ttf',64)
    # main_font = pygame.font.Font('freesansbold.ttf',20)
    clock = pygame.time.Clock()
    Main_Menu_button = pygame.Rect(screen_width // 2 - 230, 50 , screen_width // 10 , BUTTON_HEIGHT - 15)
    play_again_button  = pygame.Rect(screen_width // 2 -50  , 50 , screen_width // 10 , BUTTON_HEIGHT - 15)
    Exit_Game_button = pygame.Rect(screen_width // 2 + 130, 50 , screen_width // 10 , BUTTON_HEIGHT - 15)
   

    running = True
    flag_break = False

    while running:
        # Render the dimmed parent screen as a background
        #parent_screen.fill((0, 0, 0, 150))  # Slightly transparent black overlay
        parent_screen.blit(overlay_surface, overlay_rect.topleft)  # Blit smaller window
        parent_screen.blit(overlay_surface_2,overlay_rect_2.topleft)

        # Draw buttons
        draw_text_centered(parent_screen, "End of Game: " + winner_name + " Wins", screen_width // 2, 30, font_size=30,color=(0,0,0))
        
        Main_Menu_hovered,is_clicked = draw_button( parent_screen , "Go to Main Menu", Main_Menu_button,font_size=25 )
        play_again_hovered,is_clicked  = draw_button( parent_screen , "Play again"     , play_again_button,font_size=25  )
        Exit_Game_hovered,is_clicked = draw_button( parent_screen , "Exit Game"      , Exit_Game_button,font_size=25 )

        draw_text_centered(parent_screen, Match_result, screen_width // 2, screen_height // 2, font_size=50,color=(250,250,250))

        # Draw a line under the buttons
        # pygame.draw.line(
        #     parent_screen, 
        #     (50, 50, 50),  # Line color (gray)
        #     (0, 150),  # Start position
        #     (screen_width, 150),  # End position
        #     1  # Line thickness
        # )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running =False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_hovered:
                    if (Called_from == "Human_VS_Human"):
                        Human_VS_Human(parent_screen)
                    elif (Called_from == "Human_VS_AI"):
                        Human_VS_AI(parent_screen,depth1)
                    elif (Called_from == "AI_VS_AI"):
                        AI_VS_AI(parent_screen,depth1,depth2)
                elif Main_Menu_hovered:
                    mainwindow(parent_screen)
                elif Exit_Game_hovered:
                    running =False
                    pygame.quit()
                    
        # Update the display
        pygame.display.flip()
        clock.tick(30)
        # if(flag_break == True):
        #     break #break to function which called you
import pygame
import time


def change_names_window(screen):
    """
    Opens a new window to change the names of the players.
    """
    from modes import Human1_Name, Human2_Name  # Importing the variables from modes
    import modes  # Importing the module to reassign updated values

    pygame.init()
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h

    # Create a new window
    pygame.display.set_caption("Change Names")

    # Fonts and colors
    font = pygame.font.Font('freesansbold.ttf', 20)
    bg_color = (200, 200, 200)
    text_color = (0, 0, 0)
    input_box_color = (255, 255, 255)

    # Input boxes for names
    human1_box = pygame.Rect(screen_width // 2, 80, 200, 40)
    human2_box = pygame.Rect(screen_width // 2, 140, 200, 40)

    # Text input states
    active_box = None
    human1_input = Human1_Name
    human2_input = Human2_Name

    # Cursor properties
    cursor_visible = True
    cursor_timer = time.time()
    cursor_color = text_color

    # Buttons
    save_button = pygame.Rect(screen_width // 2, 220, 100, 40)

    running = True
    while running:
        screen.fill(bg_color)
        screen.blit(background,(0,0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return  # Exit the function

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if user clicked an input box
                if human1_box.collidepoint(event.pos):
                    active_box = "human1"
                elif human2_box.collidepoint(event.pos):
                    active_box = "human2"
                elif save_button.collidepoint(event.pos):
                    # Save the names and update global variables
                    modes.Human1_Name = human1_input
                    modes.Human2_Name = human2_input
                    running = False
                else:
                    active_box = None

            elif event.type == pygame.KEYDOWN:
                if active_box == "human1":
                    if event.key == pygame.K_BACKSPACE:
                        human1_input = human1_input[:-1]
                    else:
                        human1_input += event.unicode
                elif active_box == "human2":
                    if event.key == pygame.K_BACKSPACE:
                        human2_input = human2_input[:-1]
                    else:
                        human2_input += event.unicode
                elif event.key == pygame.K_ESCAPE:  # Check for the Esc key
                    mainwindow(screen)

        # Cursor blinking logic
        if time.time() - cursor_timer > 0.5:  # Blink every 0.5 seconds
            cursor_visible = not cursor_visible
            cursor_timer = time.time()

        # Draw input boxes
        pygame.draw.rect(screen, input_box_color, human1_box)
        pygame.draw.rect(screen, input_box_color, human2_box)

        # Draw text inside input boxes
        human1_text = font.render(human1_input, True, text_color)
        human2_text = font.render(human2_input, True, text_color)
        screen.blit(human1_text, (human1_box.x + 5, human1_box.y + 10))
        screen.blit(human2_text, (human2_box.x + 5, human2_box.y + 10))

        # Draw cursor if active
        if active_box == "human1" and cursor_visible:
            cursor_pos = font.size(human1_input)[0] + human1_box.x + 5
            pygame.draw.line(screen, cursor_color, (cursor_pos, human1_box.y + 10),
                             (cursor_pos, human1_box.y + 30), 2)
        elif active_box == "human2" and cursor_visible:
            cursor_pos = font.size(human2_input)[0] + human2_box.x + 5
            pygame.draw.line(screen, cursor_color, (cursor_pos, human2_box.y + 10),
                             (cursor_pos, human2_box.y + 30), 2)

        # Draw labels
        human1_label = font.render("White Player:", True, text_color)
        human2_label = font.render("Black Player:", True, text_color)
        screen.blit(human1_label, (human1_box.x - 140, human1_box.y + 10))
        screen.blit(human2_label, (human2_box.x - 140, human2_box.y + 10))

        # Draw save button
        pygame.draw.rect(screen, (0, 150, 0), save_button)
        save_text = font.render("Save", True, (255, 255, 255))
        screen.blit(save_text, (save_button.x + 20, save_button.y + 10))

        # Update the display
        pygame.display.flip()

def Difficulty_Human_vs_AI(screen):
    from modes import  Human_VS_AI 
    global screen_width, screen_height
    pygame.init()
    # Set up a maximized window with minimize, maximize, and close icons
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()

    Easy_button   = pygame.Rect(screen_width // 2 - 200, 300, 400, 80)
    Medium_button = pygame.Rect(screen_width // 2 - 200, 400, 400, 80)
    Hard_button   = pygame.Rect(screen_width // 2 - 200, 500, 400, 80)
    mainW_Button  = pygame.Rect(screen_width // 2 - 200, 600, 400, 80)
    Quit_Button   = pygame.Rect(screen_width // 2 - 200, 700, 400, 80)

    running = True
    while running:
        screen.fill((170, 170, 170))
        screen.blit(HomePage, (0, 0))
        #draw_text_centered(screen, "Hive Game", screen_width // 2, 250, font_size=60)
        #screen.blit(Logo, (screen_width // 2 -152, 30))
        Easy_hovered,is_clicked   = draw_button( screen , "Easy"            , Easy_button   )
        Medium_hovered,is_clicked = draw_button( screen , "Medium"          , Medium_button )
        Hard_hovered,is_clicked   = draw_button( screen , "HARD"            , Hard_button   )
        MAINW_hovered,is_clicked  = draw_button( screen , "Go to Main Menu" , mainW_Button  )
        Quit_hovered,is_clicked   = draw_button( screen , "Exit Game"       , Quit_Button   )
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Easy_hovered:
                    Human_VS_AI(screen,1)
                elif Medium_hovered:
                    Human_VS_AI(screen,2)
                elif Hard_hovered:
                    Human_VS_AI(screen,3)
                elif MAINW_hovered:
                    mainwindow(screen)
                elif Quit_hovered:
                    running =False
                    pygame.quit()

        pygame.display.flip()
        clock.tick(30)

def Difficulty_AI_vs_AI(screen):
    from modes import AI_VS_AI
    global screen_width, screen_height
    pygame.init()
    # Set up a maximized window with minimize, maximize, and close icons
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()

    # Define buttons
    Easy_button1 = pygame.Rect(screen_width // 2 - 425, 300, 400, 80)
    Medium_button1 = pygame.Rect(screen_width // 2 - 425, 400, 400, 80)
    Hard_button1 = pygame.Rect(screen_width // 2 - 425, 500, 400, 80)
    Easy_button2 = pygame.Rect(screen_width // 2 + 25, 300, 400, 80)
    Medium_button2 = pygame.Rect(screen_width // 2 + 25, 400, 400, 80)
    Hard_button2 = pygame.Rect(screen_width // 2 + 25, 500, 400, 80)
    mainW_Button  = pygame.Rect(screen_width // 2 - 200, 600, 400, 80)
    Quit_Button = pygame.Rect(screen_width // 2 - 200, 700, 400, 80)

    selected_white_difficulty = None
    selected_black_difficulty = None
    running = True

    while running:
        screen.fill((170, 170, 170))
        screen.blit(HomePage, (0, 0))
        draw_text_centered(screen, "White Computer", screen_width // 2 - 225, 250, font_size=60)
        draw_text_centered(screen, "Black Computer", screen_width // 2 + 225, 250, font_size=60)

        # Draw buttons
        Easy_hovered1, Easy_clicked1 = draw_button(screen, "Easy", Easy_button1)
        Medium_hovered1, Medium_clicked1 = draw_button(screen, "Medium", Medium_button1)
        Hard_hovered1, Hard_clicked1 = draw_button(screen, "HARD", Hard_button1)
        Easy_hovered2, Easy_clicked2 = draw_button(screen, "Easy", Easy_button2)
        Medium_hovered2, Medium_clicked2 = draw_button(screen, "Medium", Medium_button2)
        Hard_hovered2, Hard_clicked2 = draw_button(screen, "HARD", Hard_button2)
        MAINW_hovered,is_clicked  = draw_button( screen , "Go to Main Menu" , mainW_Button  )
        Quit_hovered, Quit_clicked = draw_button(screen, "Exit Game", Quit_Button)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Easy_hovered1:
                    selected_white_difficulty = 1
                elif Medium_hovered1:
                    selected_white_difficulty = 2
                elif Hard_hovered1:
                    selected_white_difficulty = 3

                if Easy_hovered2:
                    selected_black_difficulty = 1
                elif Medium_hovered2:
                    selected_black_difficulty = 2
                elif Hard_hovered2:
                    selected_black_difficulty = 3
                elif MAINW_hovered:
                    mainwindow(screen)
                elif Quit_hovered:
                    running = False
                    pygame.quit()
        if selected_white_difficulty and selected_black_difficulty:
            AI_VS_AI(screen, selected_white_difficulty, selected_black_difficulty)

        pygame.display.flip()
        clock.tick(30)
