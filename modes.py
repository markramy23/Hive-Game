import pygame
from Hex_map import HexMap
from Utilities import *
from GUI import *
from Available_positions import *
from Windows import render_menu_window , Win_Lose_window
from Heuristics import nextMove, get_picec_type, piece_type_match, nextMove_alpha_beta, nextMove_alpha_beta_loser, \
    calculate_score

#constants
Human1_Name ="Player 1"
Human2_Name = "Player 2"
AI_Name = "Computer"
Human1_Color = "W"
Human2_Color = "B"
AI1_Color ="W"
AI2_Color = "B"
turn_start_time = 0

piece_images = {        
    "Ant": Ant,     
    "Grasshopper": GrassHopper,     
    "Spider": Spider,
    "Beetle": Beetle,
    "Queen": Queen,
}

pieces = {
    "Ant": 3,
    "Grasshopper": 3,
    "Spider": 2,
    "Beetle": 2,
    "Queen": 1
}

def check_game_result(screen,color_1,color_2,player_1,player_2,white_player_lost, black_player_lost,calledfrom,depth1,depth2):
    if white_player_lost and black_player_lost:    
        Win_Lose_window(screen,depth1,depth2,"No One",Match_result="Draw match",Called_from= calledfrom)
    elif black_player_lost:
        if(color_1 == "W"):
            winner_name = player_1
        elif(color_2 == "W"):
            winner_name = player_2
        Win_Lose_window(screen,depth1,depth2,winner_name,Match_result="White Won",Called_from= calledfrom)
        # Display WHITE winner and stop the game
    elif white_player_lost:
        if(color_1 == "B"):
            winner_name = player_1
        elif(color_2 == "B"):
            winner_name = player_2
        Win_Lose_window(screen,depth1,depth2,winner_name,Match_result="Black Won",Called_from= calledfrom)

def draw_Available_positions(screen, hex_map, position_list, hex_size, screen_width, screen_height, border_color):
    """
    Draws a border around each hexagonal position on the screen.

    Args:
        screen: The surface to draw on.
        hex_map: An object containing x and y offsets for the hex map.
        position_list: A list of positions to draw, where each position is a tuple (q, r).
        hex_size: The size of the hexagon.
        screen_width: The width of the screen.
        screen_height: The height of the screen.
        border_color: The color of the border to draw.
    """
    for position in position_list:
        # Convert hex coordinates to pixel coordinates
        x, y = hex_to_pixel(position[0], position[1], hex_size, screen_width, screen_height)
        
        # Apply map offset
        x += hex_map.x
        y += hex_map.y

        # Draw the border
        draw_border(screen, x, y, border_color, hex_size)

def Enter_Piece_From_Menu(result_menu, draw_flag, hex_map_on_menu, preselected_hex, selected_hex, hex_map):
    """
    Handles entering a piece from the menu and updating the available positions.

    Args:
        result_menu: The result obtained from the menu, containing piece details.
        draw_flag: A boolean indicating whether drawing is currently enabled.
        hex_map_on_menu: The hexagonal map for the menu.
        preselected_hex: Previously selected hexagonal coordinates.
        selected_hex: Currently selected hexagonal coordinates.
        hex_map: The main hexagonal map.

    Returns:
        Updated draw_flag, preselected_hex, and list of available positions.
    """
    name_on_menu, color_on_menu, img_on_menu = result_menu

    if not draw_flag or (result_menu is not None and hex_map_on_menu.get_piece(preselected_hex[0], preselected_hex[1]) is not None):
        result = hex_map_on_menu.get_piece(selected_hex[0], selected_hex[1])

        if result is not None:
            name_4, color_4_, img_4 = result
            name_4 = name_4[:-1]
            list_positions = AvailablePositions(hex_map, hex_map.Turn, name_4)
        else:
            list_positions = []

        draw_flag = True
        preselected_hex = selected_hex

    return draw_flag, preselected_hex, list_positions

def AI_Movement(hex_map, hex_map_on_menu, positions_black, positions_white, screen_width, screen_height, HEX_SIZE_Board, AI_Color,depth, turn_start_time, turn_duration):
    """
    Handles the AI movement logic.

    Args:
        hex_map: The hexagonal map object managing game logic.
        hex_map_on_menu: The menu representation of hex map pieces.
        positions_black: List of black piece positions.
        positions_white: List of white piece positions.
        screen_width: The width of the game screen.
        screen_height: The height of the game screen.
        HEX_SIZE_Board: The size of the hexagonal cells on the board.
        AI_Color: The color of the AI pieces ("W" for white, "B" for black).

    Returns:
        None
    """
    hex_number =None
    result = nextMove_alpha_beta(hex_map, hex_map_on_menu,depth, AI_Color)
    if result:
        move_add, current_q, current_r, next_q, next_r, name1, color1, img1 = result

        preselected_hex = (current_q, current_r)
        selected_hex = (next_q, next_r)

        if move_add == "move":
            if piece_type_match(name1, "Beetle"):
                hex_map.move_beetle(preselected_hex[0], preselected_hex[1], selected_hex[0], selected_hex[1])
            else:
                hex_map.move_piece(preselected_hex[0], preselected_hex[1], selected_hex[0], selected_hex[1])
        elif move_add == "add":
            hex_map.add_piece(selected_hex[0], selected_hex[1], name1, color1, img1)
            hex_map_on_menu.remove_piece(preselected_hex[0], preselected_hex[1])

        hex_number = general_get_hex_number(preselected_hex[0], preselected_hex[1], positions_black, positions_white, screen_width, screen_height)
        h2p_x, h2p_y = hex_to_pixel(*selected_hex, HEX_SIZE_Board, screen_width, screen_height)
    if hex_number:
        if hex_map.Turn == "W" and 10 < hex_number < 22:
            positions_white[hex_number - 11] = (h2p_x, h2p_y)
            hex_map.Turn = "B"
        elif hex_map.Turn == "B" and 10 < hex_number < 22 and name1 == "Beetle":
            positions_black[hex_number - 11] = (h2p_x, h2p_y)
            hex_map.Turn = "W"
        elif hex_map.Turn == "B" and -1 < hex_number < 11:
            positions_black[hex_number] = (h2p_x, h2p_y)
            hex_map.Turn = "W"
    elif not hex_number:
        if hex_map.Turn == "W":
            hex_map.Turn = "B"
        elif hex_map.Turn == "B":
            hex_map.Turn = "W"

def player_win_check(hex_map, positions_black, positions_white, screen_width, screen_height, HEX_SIZE_MENU):
    """
    Checks if a player has won the game by evaluating queen piece states.

    Args:
        hex_map: The hexagonal map object managing game logic.
        positions_black: List of black piece positions.
        positions_white: List of white piece positions.
        screen_width: The width of the game screen.
        screen_height: The height of the game screen.
        HEX_SIZE_MENU: The size of the hexagonal cells on the menu.

    Returns:
        A tuple (white_player_lost, black_player_lost) indicating if each player has lost.
    """
    white_queen_q, white_queen_r = pixel_to_hex(positions_white[10][0], positions_white[10][1], HEX_SIZE_MENU, screen_width, screen_height)
    black_queen_q, black_queen_r = pixel_to_hex(positions_black[10][0], positions_black[10][1], HEX_SIZE_MENU, screen_width, screen_height)

    white_queen_breakhive = does_removal_break_hive(hex_map.map, (white_queen_q, white_queen_r))
    black_queen_breakhive = does_removal_break_hive(hex_map.map, (black_queen_q, black_queen_r))

    white_player_lost = False
    black_player_lost = False

    if hex_map.queen_placed["W"] and hex_map.queen_placed["B"] and not white_queen_breakhive and not black_queen_breakhive:
        white_player_lost = hex_map.did_Player_Lose(white_queen_q, white_queen_r)
        black_player_lost = hex_map.did_Player_Lose(black_queen_q, black_queen_r)
    if hex_map.queen_placed["W"] and not white_queen_breakhive:
        white_player_lost = hex_map.did_Player_Lose(white_queen_q, white_queen_r)
    if hex_map.queen_placed["B"] and not black_queen_breakhive:
        black_player_lost = hex_map.did_Player_Lose(black_queen_q, black_queen_r)

    return white_player_lost, black_player_lost

def Player_Turn(screen, font, hex_map, screen_width, player_background):
    """
    Displays the current player's turn on the screen.

    Args:
        screen: The screen surface to draw on.
        font: The font used for rendering text.
        hex_map: The main hexagonal map containing the current turn.
        screen_width: The width of the screen.
        player_background: The background image for the player turn display.
    """
    screen.blit(player_background, (screen_width // 2 - 125, -200))
    if hex_map.Turn == "W":
        Turn_Text = font.render("White Player Turn", True, BLACK)
    elif hex_map.Turn == "B":
        Turn_Text = font.render("Black Player Turn", True, BLACK)
    else:
        Turn_Text = font.render("Unknown Player Turn", True, BLACK)
    screen.blit(Turn_Text, (screen_width // 2 - 90, 15))

def PLayer_Score(screen, font, hex_map, screen_width, player_background,positions_white,positions_black):
    """
    Displays the current player's turn on the screen.

    Args:
        screen: The screen surface to draw on.
        font: The font used for rendering text.
        hex_map: The main hexagonal map containing the current turn.
        screen_width: The width of the screen.
        player_background: The background image for the player turn display.
    """
    from Heuristics import calculate_score
    global score_Black,score_White   
    # if Player_Color == "W":
    score_White = calculate_score(hex_map,"W")
    # elif Player_Color == "B":
    score_Black = calculate_score(hex_map,"B")
    screen.blit(player_background, (screen_width - 510, -200))
    screen.blit(player_background, (260, -200))
    try:
        Turn_Text_White = font.render(f"White Score: {score_White}", True, BLACK)
    except NameError:
        Turn_Text_White = font.render("White Score:0", True, BLACK)
    screen.blit(Turn_Text_White, (screen_width  - 450 , 15))

    try:
        Turn_Text_Black = font.render(f"Black Score:{score_Black}", True, BLACK)
    except NameError:
        Turn_Text_Black = font.render("Black Score:0", True, BLACK)
    screen.blit(Turn_Text_Black, (320, 15))
    
def Remaining_Turn_Time(turn_start_time,turn_duration):
    elapsed_time = pygame.time.get_ticks() - turn_start_time
    remaining_time = max(0, turn_duration - elapsed_time)
    print(f"Time remaining: {remaining_time} ms")
    return remaining_time

def Human_VS_Human(screen):
    # Hex map objects
    hex_map_on_menu = HexMap()
    hex_map = HexMap()  # Hex_map_on_board
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()
    # Define positions for the white and black pieces in pixels
    positions_white = [
        (hex_to_pixel(19, -18,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(19, -18,HEX_SIZE_Board,screen_width,screen_height)[1]) , #ANT1
        (hex_to_pixel(17, -17,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(17, -17,HEX_SIZE_Board,screen_width,screen_height)[1]) , #ANT2
        (hex_to_pixel(15, -16,HEX_SIZE_Board,screen_width,screen_height)[0],  hex_to_pixel(15, -16,HEX_SIZE_Board,screen_width,screen_height)[1]) , #ANT3
        (hex_to_pixel(19, -17,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(19, -17,HEX_SIZE_Board,screen_width,screen_height)[1]) , #GrassHopper1
        (hex_to_pixel(17, -16,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(17, -16,HEX_SIZE_Board,screen_width,screen_height)[1]) , #GrassHopper2
        (hex_to_pixel(15, -15,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(15, -15,HEX_SIZE_Board,screen_width,screen_height)[1]) , #GrassHopper3
        (hex_to_pixel(19, -16,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(19, -16,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Spider1
        (hex_to_pixel(17, -15,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(17, -15,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Spider2
        (hex_to_pixel(15, -14,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(15, -14,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Beetle1
        (hex_to_pixel(19, -15,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(19, -15,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Beetle2
        (hex_to_pixel(17, -14,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(17, -14,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Queen1
    ]
    
    positions_black = [
        (hex_to_pixel(-19, 1  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-19,  1 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #ANT1
        (hex_to_pixel(-17, 0  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-17,  0 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #ANT2
        (hex_to_pixel(-15, -1 ,HEX_SIZE_Board,screen_width,screen_height)[0]  ,hex_to_pixel(-15 , -1 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #ANT3
        (hex_to_pixel(-19, 2  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-19,  2 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #GrassHopper1
        (hex_to_pixel(-17, 1  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-17,  1 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #GrassHopper2
        (hex_to_pixel(-15, 0  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-15,  0 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #GrassHopper3
        (hex_to_pixel(-19, 3  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-19,  3 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Spider1
        (hex_to_pixel(-17, 2  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-17,  2 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Spider2
        (hex_to_pixel(-15, 1  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-15,  1 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Beetle1
        (hex_to_pixel(-19, 4  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-19,  4 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Beetle2
        (hex_to_pixel(-17, 3  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-17,  3 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Queen1
    ] 

    add_pieces(positions_white, "W",piece_images,pieces,screen_width,screen_height,hex_map_on_menu)
    add_pieces(positions_black, "B",piece_images,pieces,screen_width,screen_height,hex_map_on_menu)
    
    #Initial Values
    selected_hex = (0, 0)
    preselected_hex = selected_hex #the previous value of selected_hex
    running = True
    dragging = False
    last_mouse_pos = (0, 0)
    draw_flag = False
    hex_number = 0  
    white_player_lost = False
    black_player_lost = False

    while running:
        screen.blit(background, (0, 0))
        #Draw hexagons
        #Test_Map(screen,hex_map,selected_hex,HEX_SIZE_Board,HEX_COLOR,SELECTED_COLOR,BORDER_COLOR,screen_width,screen_height)
        
        check_game_result(screen,Human1_Color,Human2_Color,Human1_Name,Human2_Name,white_player_lost,black_player_lost,"Human_VS_Human",0,0)


        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    #to chech if the mouse click in the board range or menu range
                    if (mouse_x <=250 and mouse_y<=250) or (mouse_x >=screen_width-250 and mouse_y<=250):
                        selected_hex = pixel_to_hex(mouse_x - hex_map_on_menu.x, mouse_y - hex_map_on_menu.y, HEX_SIZE_Board,screen_width,screen_height)
                        # print(f"Selected Hex: {selected_hex},{hex_map_on_menu.get_piece(selected_hex[0], selected_hex[1])}")
                    else:
                        selected_hex = pixel_to_hex(mouse_x - hex_map.x, mouse_y - hex_map.y, HEX_SIZE_Board,screen_width,screen_height)
                        # print(f"Selected Hex: {selected_hex},{hex_map.get_piece(selected_hex[0], selected_hex[1])}")
                    
                    #Determine the values of list based on the state    
                        
                    #check first click    
                    new_mouse_x,new_mouse_y=hex_to_pixel(selected_hex[0],selected_hex[1],HEX_SIZE_Board,screen_width,screen_height)
                    
                    if(((new_mouse_x>screen_width-250 and new_mouse_y<250) and hex_map.Turn == 'B') or
                        ((new_mouse_x<250 and new_mouse_y<250) and hex_map.Turn == 'W')):
                        draw_flag = False
                        continue
                    #get the name , color and img of the selected piece
                    result_menu = hex_map_on_menu.get_piece(selected_hex[0],selected_hex[1]) 
                    result_board = hex_map.get_piece(selected_hex[0],selected_hex[1])
                    # print("preselected")
                    # print(preselected_hex,hex_map.get_piece(preselected_hex[0], preselected_hex[1]))
                    # print("selected")
                    # print(selected_hex,hex_map.get_piece(selected_hex[0], selected_hex[1]))
                    
                    ########################## Code to enter the piece from menu to board ################################### 
                    if(result_menu != None):#to ensure that the currect selected piece is on menu
                        draw_flag, preselected_hex, list = Enter_Piece_From_Menu(result_menu, draw_flag, hex_map_on_menu, preselected_hex, selected_hex, hex_map)
                    ########################## Code to enter the piece from board to board ################################### 
                    elif(result_board != None):
                        name_on_board,color_on_board,img_on_board = result_board
                        name_on_board=name_on_board[:-1]
                        flag_deselcet_or_not = True
                        prevresult_on_board_to_check_beetle = hex_map.get_piece(preselected_hex[0], preselected_hex[1])
                        if(prevresult_on_board_to_check_beetle !=None):
                            name_on_board_to_check_beetle,color_on_board_to_check_beetle,img_on_board_to_check_beetle = prevresult_on_board_to_check_beetle    
                            name_on_board_to_check_beetle = name_on_board_to_check_beetle[:-1]
                            #print(color_on_board)
                            if(name_on_board_to_check_beetle =="Beetle"):
                                    list = AvailablePositions_Beetle(hex_map,preselected_hex[0],preselected_hex[1])
                                    for element in list: 
                                                if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):
                                                    flag_deselcet_or_not =False
                        elif(color_on_board != hex_map.Turn and flag_deselcet_or_not == True):    
                            draw_flag=False
                            continue
                        name_on_board = name_on_board[:-1]
                        #print("1010")
                        if((hex_map_on_menu.get_piece(preselected_hex[0],preselected_hex[1]) != None) and (hex_map_on_menu.get_piece(selected_hex[0],selected_hex[1]) == None)):
                            #print("000")
                            preselected_hex=(100,100)
                        prevresult_on_board_1click = hex_map.get_piece(preselected_hex[0],preselected_hex[1])
                        
                        if(not draw_flag or result_board != None): 
                            draw_flag = True
                            flag = True
                            if (prevresult_on_board_1click != None):
                                prev_name_board_1click , prev_color_board_1click , prev_img_board_1click = prevresult_on_board_1click 
                                prev_name_board_1click = prev_name_board_1click[:-1]
                                if(prev_name_board_1click == "Beetle"): 
                                    list = AvailablePositions_Beetle(hex_map,preselected_hex[0],preselected_hex[1])
                                    #print(list)
                                    for element in list: 
                                            if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):
                                                #selected_hex = preselected_hex
                                                flag =False
                                                #print(555)
                                                break
                                            else:
                                                flag = True 
                                else:
                                   # print(666)
                                    preselected_hex = selected_hex  
                            if(flag == True):
                               # print(444)
                                preselected_hex = selected_hex 
                            
                            is_beetle_stacked = False
                            prevresult_on_board_1click = hex_map.get_piece(preselected_hex[0],preselected_hex[1])
                            if (prevresult_on_board_1click != None):
                                prev_name_board_1click , prev_color_board_1click , prev_img_board_1click = prevresult_on_board_1click 
                                prev_name_board_1click = prev_name_board_1click[:-1]
                            if(does_removal_break_hive(hex_map.map,preselected_hex) and prev_name_board_1click == "Beetle"):
                                for outcast in hex_map.OutCasts:
                                    if(outcast[0]==preselected_hex):
                                        is_beetle_stacked = True
                                        break
                                    else:
                                        is_beetle_stacked = False

                            if(not does_removal_break_hive(hex_map.map,preselected_hex) or is_beetle_stacked ):
                                name_on_board_3 ,color_on_board_3 ,img_on_board_3 = hex_map.get_piece(preselected_hex[0],preselected_hex[1])
                                name_on_board_3 = name_on_board_3[:-1]
                                if name_on_board_3 == "Queen":
                                    list = Available_Positions_Queen(hex_map, preselected_hex[0], preselected_hex[1])

                                elif name_on_board_3 == "Ant":
                                    list = AvailablePositions_Ant(hex_map, preselected_hex[0], preselected_hex[1])

                                elif name_on_board_3 == "Grasshopper":
                                    list = AvailablePositions_GrassHopper(hex_map, preselected_hex[0],
                                                                          preselected_hex[1])

                                elif name_on_board_3 == "Spider":
                                    list = Available_Positions_Spider(hex_map, preselected_hex[0], preselected_hex[1])

                                elif name_on_board_3 == "Beetle":
                                    list = AvailablePositions_Beetle(hex_map, preselected_hex[0], preselected_hex[1])

                            else:
                                draw_flag = False
                                    
                    if (draw_flag):
                        #print("222")  
                        for element in list:
                            #check 2 left clicking 
                           # print(element)
                            result = hex_map.get_piece(selected_hex[0],selected_hex[1])
                            if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):
                                #print(preselected_hex)
                                prevresult_on_menu = hex_map_on_menu.get_piece(preselected_hex[0],preselected_hex[1])
                                prevresult_on_board = hex_map.get_piece(preselected_hex[0],preselected_hex[1])
                                if(prevresult_on_menu != None):#Check if the prev selected on menu 
                                    #print("444")
                                    name , color , img = prevresult_on_menu
                                    hex_map.add_piece(selected_hex[0],selected_hex[1],name,color,img)
                                    hex_map_on_menu.remove_piece(preselected_hex[0],preselected_hex[1])
                                if(prevresult_on_board != None):#Check if the prev selected on board 
                                    name , color , img = prevresult_on_board
                                    name1 = name[:-1]
                                    for outcost in hex_map.OutCasts:
                                        if(outcost[0] == preselected_hex):
                                            flag =False
                                           # print(777)
                                    if (name1 == "Beetle" and flag == False):
                                       # print(111)
                                        hex_map.move_beetle(preselected_hex[0],preselected_hex[1],selected_hex[0],selected_hex[1])
                                    else:
                                        hex_map.add_piece(selected_hex[0],selected_hex[1],name,color,img)
                                        hex_map.remove_piece(preselected_hex[0],preselected_hex[1]) 
                                    #print(f"outcast :{hex_map.OutCasts}")
                                    # print(f"Hex_Map :{hex_map.map}")
                                draw_flag=False
                                hex_number = general_get_hex_number(preselected_hex[0],preselected_hex[1],positions_black,positions_white,screen_width,screen_height)
                                
                                #print(preselected_hex)
                                #print(f"the hex number is : {hex_number,hex_map.Turn}")
                                preselected_hex= (100,100)

                                h2p_x,h2p_y = hex_to_pixel(*selected_hex,HEX_SIZE_Board,screen_width,screen_height)
                                if(hex_map.Turn == "W" and (hex_number>10 and hex_number<22)):
                                    positions_white[hex_number-11]=h2p_x,h2p_y
                                    hex_map.Turn = "B"
                                elif(hex_map.Turn == "B" and (hex_number>10 and hex_number<22) and name1 == "Beetle"):
                                    positions_black[hex_number-11]=h2p_x,h2p_y
                                    hex_map.Turn = "W"
                                elif(hex_map.Turn == "B" and (hex_number>-1 and hex_number<11)):
                                    positions_black[hex_number]=h2p_x,h2p_y
                                    hex_map.Turn = "W"
                                
                                # Player Win Check
                                white_player_lost , black_player_lost =player_win_check(hex_map, positions_black, positions_white, screen_width, screen_height, HEX_SIZE_MENU)


                                break
                            #Deselecting

                            elif(((hex_map_on_menu.get_piece(selected_hex[0],selected_hex[1]) == None) and (result == None)) and (selected_hex[0] != element[0] and selected_hex[1] != element[1])):
                                # for element1 in list:
                                #     if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):

                                #print("444")
                                draw_flag = False
                                # preselected_hex = (0,0)
                                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check for the Esc key
                    render_menu_window(screen)
                            
            # Call the change_map_position function to the map on board(hex_map)
            dragging, last_mouse_pos = change_map_position(
                event, dragging, last_mouse_pos,hex_map
            )
        
        if draw_flag:
            draw_Available_positions(screen, hex_map, list, HEX_SIZE_Board, screen_width, screen_height, BORDER_COLOR_2)

        draw_player(Human1_Name, Human2_Name,screen)
        draw_hexagons(positions_black, BLACK_PLAYER, BORDER_COLOR,screen_width,screen_height,hex_map,screen,hex_map_on_menu) 
        draw_hexagons(positions_white, WHITE_PLAYER, BORDER_COLOR,screen_width,screen_height,hex_map,screen,hex_map_on_menu)
        Player_Turn(screen, font, hex_map, screen_width, player_background)
        PLayer_Score(screen, font, hex_map, screen_width, player_background,positions_white,positions_black)
        PLayer_Score(screen, font, hex_map, screen_width, player_background,positions_white,positions_black)


            
        result = hex_map.get_piece(selected_hex[0],selected_hex[1])
        if(result != None):
            name_on_board_2 ,color_on_board_2,img_on_board_2 = result
            name_on_board_2 = name_on_board_2[:-1]
            if(draw_flag and name_on_board_2 == "Beetle"):
                for hamada in list: 
                    x,y = hex_to_pixel( hamada[0],hamada[1],HEX_SIZE_Board,screen_width,screen_height)
                    x+=hex_map.x
                    y+=hex_map.y
                    draw_border(screen,x,y, BORDER_COLOR_2, HEX_SIZE_Board)
            
        pygame.display.flip()
        clock.tick(30)

def Human_VS_AI(screen,depth):
    # Hex map objects
    hex_map_on_menu = HexMap()
    hex_map = HexMap()  # Hex_map_on_board
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()
    # Define positions for the white and black pieces in pixels
    positions_white = [
        (hex_to_pixel(19, -18, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(19, -18, HEX_SIZE_Board, screen_width, screen_height)[1]),  # ANT1
        (hex_to_pixel(17, -17, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(17, -17, HEX_SIZE_Board, screen_width, screen_height)[1]),  # ANT2
        (hex_to_pixel(15, -16, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(15, -16, HEX_SIZE_Board, screen_width, screen_height)[1]),  # ANT3
        (hex_to_pixel(19, -17, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(19, -17, HEX_SIZE_Board, screen_width, screen_height)[1]),  # GrassHopper1
        (hex_to_pixel(17, -16, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(17, -16, HEX_SIZE_Board, screen_width, screen_height)[1]),  # GrassHopper2
        (hex_to_pixel(15, -15, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(15, -15, HEX_SIZE_Board, screen_width, screen_height)[1]),  # GrassHopper3
        (hex_to_pixel(19, -16, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(19, -16, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Spider1
        (hex_to_pixel(17, -15, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(17, -15, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Spider2
        (hex_to_pixel(15, -14, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(15, -14, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Beetle1
        (hex_to_pixel(19, -15, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(19, -15, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Beetle2
        (hex_to_pixel(17, -14, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(17, -14, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Queen1
    ]

    positions_black = [
        (hex_to_pixel(-19, 1, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-19, 1, HEX_SIZE_Board, screen_width, screen_height)[1]),  # ANT1
        (hex_to_pixel(-17, 0, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-17, 0, HEX_SIZE_Board, screen_width, screen_height)[1]),  # ANT2
        (hex_to_pixel(-15, -1, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-15, -1, HEX_SIZE_Board, screen_width, screen_height)[1]),  # ANT3
        (hex_to_pixel(-19, 2, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-19, 2, HEX_SIZE_Board, screen_width, screen_height)[1]),  # GrassHopper1
        (hex_to_pixel(-17, 1, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-17, 1, HEX_SIZE_Board, screen_width, screen_height)[1]),  # GrassHopper2
        (hex_to_pixel(-15, 0, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-15, 0, HEX_SIZE_Board, screen_width, screen_height)[1]),  # GrassHopper3
        (hex_to_pixel(-19, 3, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-19, 3, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Spider1
        (hex_to_pixel(-17, 2, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-17, 2, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Spider2
        (hex_to_pixel(-15, 1, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-15, 1, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Beetle1
        (hex_to_pixel(-19, 4, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-19, 4, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Beetle2
        (hex_to_pixel(-17, 3, HEX_SIZE_Board, screen_width, screen_height)[0],
         hex_to_pixel(-17, 3, HEX_SIZE_Board, screen_width, screen_height)[1]),  # Queen1
    ]

    add_pieces(positions_white, "W", piece_images, pieces, screen_width, screen_height, hex_map_on_menu)
    add_pieces(positions_black, "B", piece_images, pieces, screen_width, screen_height, hex_map_on_menu)

    # Initial Values
    selected_hex = (0, 0)
    preselected_hex = selected_hex  # the previous value of selected_hex
    running = True
    dragging = False
    last_mouse_pos = (0, 0)
    draw_flag = False
    hex_number = 0
    white_player_lost = False
    black_player_lost = False
    turn_duration = 20000 #time for easy-medium
    if(depth == 3):
        turn_duration = 30000
    while running:
        screen.blit(background, (0, 0))
        # Draw hexagons
        # Test_Map(screen,hex_map,selected_hex,HEX_SIZE_Board,HEX_COLOR,SELECTED_COLOR,BORDER_COLOR,screen_width,screen_height)

        check_game_result(screen,Human1_Color,AI2_Color,Human1_Name,AI_Name,white_player_lost,black_player_lost,"Human_VS_AI",depth,0)
        if (hex_map.Turn == AI2_Color):
            turn_start_time = pygame.time.get_ticks()
            AI_Movement(hex_map, hex_map_on_menu, positions_black, positions_white, screen_width, screen_height, HEX_SIZE_Board, AI2_Color,depth, turn_start_time, turn_duration)

        else:
            # Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        # to chech if the mouse click in the board range or menu range
                        if (mouse_x <= 250 and mouse_y <= 250) or (mouse_x >= screen_width - 250 and mouse_y <= 250):
                            selected_hex = pixel_to_hex(mouse_x - hex_map_on_menu.x, mouse_y - hex_map_on_menu.y,
                                                        HEX_SIZE_Board, screen_width, screen_height)
                            # print(f"Selected Hex: {selected_hex},{hex_map_on_menu.get_piece(selected_hex[0], selected_hex[1])}")
                        else:
                            selected_hex = pixel_to_hex(mouse_x - hex_map.x, mouse_y - hex_map.y, HEX_SIZE_Board,
                                                        screen_width, screen_height)
                            # print(f"Selected Hex: {selected_hex},{hex_map.get_piece(selected_hex[0], selected_hex[1])}")

                        # Determine the values of list based on the state

                        # check first click
                        new_mouse_x, new_mouse_y = hex_to_pixel(selected_hex[0], selected_hex[1], HEX_SIZE_Board,
                                                                screen_width, screen_height)

                        if (((new_mouse_x > screen_width - 250 and new_mouse_y < 250) and hex_map.Turn == 'B') or
                                ((new_mouse_x < 250 and new_mouse_y < 250) and hex_map.Turn == 'W')):
                            draw_flag = False
                            continue
                        # get the name and color and img of the selected piece
                        result_menu = hex_map_on_menu.get_piece(selected_hex[0], selected_hex[1])
                        result_board = hex_map.get_piece(selected_hex[0], selected_hex[1])
                        # print("preselected")
                        # print(preselected_hex,hex_map.get_piece(preselected_hex[0], preselected_hex[1]))
                        # print("selected")
                        # print(selected_hex,hex_map.get_piece(selected_hex[0], selected_hex[1]))

                        ########################## Code to enter the piece from menu to board ###################################
                        if (hex_map.Turn == Human1_Color):
                            if (result_menu != None):  # to ensure that the currect selected piece is on menu
                                draw_flag, preselected_hex, list = Enter_Piece_From_Menu(result_menu, draw_flag, hex_map_on_menu, preselected_hex, selected_hex, hex_map)
                            ########################## Code to enter the piece from board to board ###################################
                            elif (result_board != None):
                                name_on_board, color_on_board, img_on_board = result_board
                                name_on_board = name_on_board[:-1]
                                flag_deselcet_or_not = True
                                prevresult_on_board_to_check_beetle = hex_map.get_piece(preselected_hex[0],
                                                                                        preselected_hex[1])
                                if (prevresult_on_board_to_check_beetle != None):
                                    name_on_board_to_check_beetle, color_on_board_to_check_beetle, img_on_board_to_check_beetle = prevresult_on_board_to_check_beetle
                                    name_on_board_to_check_beetle = name_on_board_to_check_beetle[:-1]
                                    # print(color_on_board)
                                    if (name_on_board_to_check_beetle == "Beetle"):
                                        list = AvailablePositions_Beetle(hex_map, preselected_hex[0],
                                                                         preselected_hex[1])
                                        for element in list:
                                            if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):
                                                flag_deselcet_or_not = False
                                elif (color_on_board != hex_map.Turn and flag_deselcet_or_not == True):
                                    draw_flag = False
                                    continue
                                name_on_board = name_on_board[:-1]
                                # print("1010")
                                if ((hex_map_on_menu.get_piece(preselected_hex[0], preselected_hex[1]) != None) and (
                                        hex_map_on_menu.get_piece(selected_hex[0], selected_hex[1]) == None)):
                                    # print("000")
                                    preselected_hex = (100, 100)
                                prevresult_on_board_1click = hex_map.get_piece(preselected_hex[0], preselected_hex[1])

                                if (not draw_flag or result_board != None):
                                    draw_flag = True
                                    flag = True
                                    if (prevresult_on_board_1click != None):
                                        prev_name_board_1click, prev_color_board_1click, prev_img_board_1click = prevresult_on_board_1click
                                        prev_name_board_1click = prev_name_board_1click[:-1]
                                        if (prev_name_board_1click == "Beetle"):
                                            list = AvailablePositions_Beetle(hex_map, preselected_hex[0],
                                                                             preselected_hex[1])
                                            #  print(list)
                                            for element in list:
                                                if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):
                                                    # selected_hex = preselected_hex
                                                    flag = False
                                                    # print(555)
                                                    break
                                                else:
                                                    flag = True
                                        else:
                                            # print(666)
                                            preselected_hex = selected_hex
                                    if (flag == True):
                                        # print(444)
                                        preselected_hex = selected_hex

                                    is_beetle_stacked = False
                                    prevresult_on_board_1click = hex_map.get_piece(preselected_hex[0],
                                                                                   preselected_hex[1])
                                    if (prevresult_on_board_1click != None):
                                        prev_name_board_1click, prev_color_board_1click, prev_img_board_1click = prevresult_on_board_1click
                                        prev_name_board_1click = prev_name_board_1click[:-1]
                                    if (does_removal_break_hive(hex_map.map,
                                                                preselected_hex) and prev_name_board_1click == "Beetle"):
                                        for outcast in hex_map.OutCasts:
                                            if (outcast[0] == preselected_hex):
                                                is_beetle_stacked = True
                                                break
                                            else:
                                                is_beetle_stacked = False

                                    if (not does_removal_break_hive(hex_map.map, preselected_hex) or is_beetle_stacked):
                                        name_on_board_3, color_on_board_3, img_on_board_3 = hex_map.get_piece(
                                            preselected_hex[0], preselected_hex[1])
                                        name_on_board_3 = name_on_board_3[:-1]

                                        if name_on_board_3 == "Queen":
                                            list = Available_Positions_Queen(hex_map, preselected_hex[0],
                                                                             preselected_hex[1])

                                        elif name_on_board_3 == "Ant":
                                            list = AvailablePositions_Ant(hex_map, preselected_hex[0],
                                                                          preselected_hex[1])

                                        elif name_on_board_3 == "Grasshopper":
                                            list = AvailablePositions_GrassHopper(hex_map, preselected_hex[0],
                                                                                  preselected_hex[1])

                                        elif name_on_board_3 == "Spider":
                                            list = Available_Positions_Spider(hex_map, preselected_hex[0],
                                                                              preselected_hex[1])

                                        elif name_on_board_3 == "Beetle":
                                            list = AvailablePositions_Beetle(hex_map, preselected_hex[0],
                                                                             preselected_hex[1])

                                    else:
                                        draw_flag = False

                        ###################################################Draw#############################
                        if (draw_flag):
                            # print("222")
                            for element in list:
                                # check 2 left clicking
                                print(element)
                                result = hex_map.get_piece(selected_hex[0], selected_hex[1])
                                if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):
                                    # print(preselected_hex)
                                    prevresult_on_menu = hex_map_on_menu.get_piece(preselected_hex[0],
                                                                                   preselected_hex[1])
                                    prevresult_on_board = hex_map.get_piece(preselected_hex[0], preselected_hex[1])
                                    if (prevresult_on_menu != None):  # Check if the prev selected on menu
                                        # print("444")
                                        name, color, img = prevresult_on_menu
                                        hex_map.add_piece(selected_hex[0], selected_hex[1], name, color, img)
                                        hex_map_on_menu.remove_piece(preselected_hex[0], preselected_hex[1])
                                    if (prevresult_on_board != None):  # Check if the prev selected on board
                                        name, color, img = prevresult_on_board
                                        name1 = name[:-1]
                                        for outcost in hex_map.OutCasts:
                                            if (outcost[0] == preselected_hex):
                                                flag = False
                                            # print(777)
                                        if (name1 == "Beetle" and flag == False):
                                            # print(111)
                                            hex_map.move_beetle(preselected_hex[0], preselected_hex[1], selected_hex[0],
                                                                selected_hex[1])
                                        else:
                                            hex_map.add_piece(selected_hex[0], selected_hex[1], name, color, img)
                                            hex_map.remove_piece(preselected_hex[0], preselected_hex[1])
                                            #  print(f"outcast :{hex_map.OutCasts}")
                                        # print(f"Hex_Map :{hex_map.map}")
                                    draw_flag = False
                                    hex_number = general_get_hex_number(preselected_hex[0], preselected_hex[1],
                                                                        positions_black, positions_white, screen_width,
                                                                        screen_height)

                                    # print(preselected_hex)
                                    # print(f"the hex number is : {hex_number,hex_map.Turn}")
                                    preselected_hex = [100, 100]

                                    h2p_x, h2p_y = hex_to_pixel(*selected_hex, HEX_SIZE_Board, screen_width,
                                                                screen_height)
                                    if (hex_map.Turn == "W" and (hex_number > 10 and hex_number < 22)):
                                        positions_white[hex_number - 11] = h2p_x, h2p_y
                                        hex_map.Turn = "B"
                                    elif (hex_map.Turn == "B" and (
                                            hex_number > 10 and hex_number < 22) and name1 == "Beetle"):
                                        positions_black[hex_number - 11] = h2p_x, h2p_y
                                        hex_map.Turn = "W"
                                    elif (hex_map.Turn == "B" and (hex_number > -1 and hex_number < 11)):
                                        positions_black[hex_number] = h2p_x, h2p_y
                                        hex_map.Turn = "W"

                                    # 1 for white win,
                                    # 2 for black win
                                    # 3 for Draw
                                    # if ( (not white_queen_breakhive) and (not black_queen_breakhive) and (hex_map.queen_placed["W"]) and (hex_map.queen_placed["B"]) and white_player_lost and black_player_lost):
                                    #     flag_winner = 3
                                    # elif ( (not white_queen_breakhive) and (hex_map.queen_placed["W"]) and white_player_lost ):
                                    #     flag_winner = 2
                                    # elif ( (not black_queen_breakhive) and (hex_map.queen_placed["B"]) and black_player_lost ):
                                    #     flag_winner = 1

                                    break
                                # Deselecting

                                elif (((hex_map_on_menu.get_piece(selected_hex[0], selected_hex[1]) == None) and (
                                        result == None)) and (
                                              selected_hex[0] != element[0] and selected_hex[1] != element[1])):
                                    # for element1 in list:
                                    #     if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):

                                    # print("444")
                                    draw_flag = False
                                    # preselected_hex = (0,0)
                                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Check for the Esc key
                        render_menu_window(screen)

                # Call the change_map_position function to the map on board(hex_map)
                dragging, last_mouse_pos = change_map_position(
                    event, dragging, last_mouse_pos, hex_map
                )
        
        # Player Win Check
        white_player_lost , black_player_lost =player_win_check(hex_map, positions_black, positions_white, screen_width, screen_height, HEX_SIZE_MENU)


        if draw_flag:
            # Iterate through the list of positions
            for position in list:
                x, y = hex_to_pixel(position[0], position[1], HEX_SIZE_Board, screen_width, screen_height)
                x += hex_map.x
                y += hex_map.y
                draw_border(screen, x, y, BORDER_COLOR_2, HEX_SIZE_Board)

        # print(pixel_to_hex(768,432,HEX_SIZE_Board))
        # print(f"{positions_white}")
        # if(hex_map.Turn == "W"):
        #     draw_hexagons(positions_white, WHITE_PLAYER, BORDER_COLOR)
        #     draw_hexagons(positions_black, BLACK_PLAYER, BORDER_COLOR)
        # else:
        draw_player(Human1_Name, AI_Name, screen)
        draw_hexagons(positions_black, BLACK_PLAYER, BORDER_COLOR, screen_width, screen_height, hex_map, screen,
                      hex_map_on_menu)
        draw_hexagons(positions_white, WHITE_PLAYER, BORDER_COLOR, screen_width, screen_height, hex_map, screen,
                      hex_map_on_menu)
        Player_Turn(screen, font, hex_map, screen_width, player_background) 
        PLayer_Score(screen, font, hex_map, screen_width, player_background,positions_white,positions_black)
        PLayer_Score(screen, font, hex_map, screen_width, player_background,positions_white,positions_black)         

        result = hex_map.get_piece(selected_hex[0], selected_hex[1])
        if (result != None):
            name_on_board_2, color_on_board_2, img_on_board_2 = result
            name_on_board_2 = name_on_board_2[:-1]
            if (draw_flag and name_on_board_2 == "Beetle"):
                for hamada in list:
                    x, y = hex_to_pixel(hamada[0], hamada[1], HEX_SIZE_Board, screen_width, screen_height)
                    x += hex_map.x
                    y += hex_map.y
                    draw_border(screen, x, y, BORDER_COLOR_2, HEX_SIZE_Board)

        pygame.display.flip()
        clock.tick(30)

def AI_VS_AI(screen,depth1,depth2):
    # Hex map objects
    hex_map_on_menu = HexMap()
    hex_map = HexMap()  # Hex_map_on_board
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()

    # Define positions for the white and black pieces in pixels
    positions_white = [
        (hex_to_pixel(19, -18,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(19, -18,HEX_SIZE_Board,screen_width,screen_height)[1]) , #ANT1
        (hex_to_pixel(17, -17,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(17, -17,HEX_SIZE_Board,screen_width,screen_height)[1]) , #ANT2
        (hex_to_pixel(15, -16,HEX_SIZE_Board,screen_width,screen_height)[0],  hex_to_pixel(15, -16,HEX_SIZE_Board,screen_width,screen_height)[1]) , #ANT3
        (hex_to_pixel(19, -17,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(19, -17,HEX_SIZE_Board,screen_width,screen_height)[1]) , #GrassHopper1
        (hex_to_pixel(17, -16,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(17, -16,HEX_SIZE_Board,screen_width,screen_height)[1]) , #GrassHopper2
        (hex_to_pixel(15, -15,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(15, -15,HEX_SIZE_Board,screen_width,screen_height)[1]) , #GrassHopper3
        (hex_to_pixel(19, -16,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(19, -16,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Spider1
        (hex_to_pixel(17, -15,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(17, -15,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Spider2
        (hex_to_pixel(15, -14,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(15, -14,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Beetle1
        (hex_to_pixel(19, -15,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(19, -15,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Beetle2
        (hex_to_pixel(17, -14,HEX_SIZE_Board,screen_width,screen_height)[0] , hex_to_pixel(17, -14,HEX_SIZE_Board,screen_width,screen_height)[1]) , #Queen1
    ]
    
    positions_black = [
        (hex_to_pixel(-19, 1  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-19,  1 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #ANT1
        (hex_to_pixel(-17, 0  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-17,  0 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #ANT2
        (hex_to_pixel(-15, -1 ,HEX_SIZE_Board,screen_width,screen_height)[0]  ,hex_to_pixel(-15 , -1 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #ANT3
        (hex_to_pixel(-19, 2  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-19,  2 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #GrassHopper1
        (hex_to_pixel(-17, 1  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-17,  1 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #GrassHopper2
        (hex_to_pixel(-15, 0  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-15,  0 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #GrassHopper3
        (hex_to_pixel(-19, 3  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-19,  3 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Spider1
        (hex_to_pixel(-17, 2  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-17,  2 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Spider2
        (hex_to_pixel(-15, 1  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-15,  1 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Beetle1
        (hex_to_pixel(-19, 4  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-19,  4 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Beetle2
        (hex_to_pixel(-17, 3  ,HEX_SIZE_Board,screen_width,screen_height)[0]  , hex_to_pixel(-17,  3 , HEX_SIZE_Board,screen_width,screen_height)[1])  , #Queen1
    ]
    
    add_pieces(positions_white, "W",piece_images,pieces,screen_width,screen_height,hex_map_on_menu)
    add_pieces(positions_black, "B",piece_images,pieces,screen_width,screen_height,hex_map_on_menu)
    
    #Initial Values
    #selected_hex = (0, 0)
    #preselected_hex = selected_hex #the previous value of selected_hex
    running = True
    dragging = False
    last_mouse_pos = (0, 0)
    # draw_flag = False
    # hex_number = 0  
    white_player_lost = False
    black_player_lost = False
    turn_duration_player1 = 20000
    turn_duration_player2 = 20000
    if(depth1 == 3):
        turn_duration_player1 = 30000
    if(depth2 == 3):
        turn_duration_player2 = 30000
    while running:
        screen.blit(background, (0, 0))
        #Draw hexagons
        #Test_Map(screen,hex_map,selected_hex,HEX_SIZE_Board,HEX_COLOR,SELECTED_COLOR,BORDER_COLOR,screen_width,screen_height)
        
        check_game_result(screen,AI1_Color,AI2_Color,AI_Name,AI_Name,white_player_lost,black_player_lost,"AI_VS_AI",depth1,depth2)
        if(hex_map.Turn == AI1_Color):
            turn_start_time = pygame.time.get_ticks()
            AI_Movement(hex_map, hex_map_on_menu, positions_black, positions_white, screen_width, screen_height, HEX_SIZE_Board, AI1_Color,depth1,turn_start_time,turn_duration_player1)

        elif(hex_map.Turn == AI2_Color):
            turn_start_time = pygame.time.get_ticks()
            AI_Movement(hex_map, hex_map_on_menu, positions_black, positions_white, screen_width, screen_height, HEX_SIZE_Board, AI2_Color,depth2,turn_start_time,turn_duration_player2)

        #Player Win Check
        white_player_lost , black_player_lost =player_win_check(hex_map, positions_black, positions_white, screen_width, screen_height, HEX_SIZE_MENU)

        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    #to chech if the mouse click in the board range or menu range
                    if (mouse_x <=250 and mouse_y<=250) or (mouse_x >=screen_width-250 and mouse_y<=250):
                        selected_hex = pixel_to_hex(mouse_x - hex_map_on_menu.x, mouse_y - hex_map_on_menu.y, HEX_SIZE_Board,screen_width,screen_height)
                        # print(f"Selected Hex: {selected_hex},{hex_map_on_menu.get_piece(selected_hex[0], selected_hex[1])}")
                    else:
                        selected_hex = pixel_to_hex(mouse_x - hex_map.x, mouse_y - hex_map.y, HEX_SIZE_Board,screen_width,screen_height)
                        # print(f"Selected Hex: {selected_hex},{hex_map.get_piece(selected_hex[0], selected_hex[1])}")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check for the Esc key
                    render_menu_window(screen)
                            
            # Call the change_map_position function to the map on board(hex_map)
            dragging, last_mouse_pos = change_map_position(
                event, dragging, last_mouse_pos,hex_map
            )
        
        draw_player(AI_Name, AI_Name,screen)
        draw_hexagons(positions_black, BLACK_PLAYER, BORDER_COLOR,screen_width,screen_height,hex_map,screen,hex_map_on_menu) 
        draw_hexagons(positions_white, WHITE_PLAYER, BORDER_COLOR,screen_width,screen_height,hex_map,screen,hex_map_on_menu)
        Player_Turn(screen, font, hex_map, screen_width, player_background)
        PLayer_Score(screen, font, hex_map, screen_width, player_background,positions_white,positions_black)
        PLayer_Score(screen, font, hex_map, screen_width, player_background,positions_white,positions_black)


            
        pygame.display.flip()
        clock.tick(30)
