import pygame
from Windows import mainwindow 

def main():
    global screen_width, screen_height
    pygame.init()
    # Set up a maximized window with minimize, maximize, and close icons
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()
    mainwindow(screen)
    pygame.quit()

if __name__ == "__main__":
    main()

    #1-score
    #2-updates
    #3-time
    #4-if there are no available moves skip