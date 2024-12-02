import pygame
from GUI import *
from Hex_map import HexMap
from Utilities import *
from Available_positions import *

def main():
    global screen_width, screen_height

    pygame.init()


    # Set up a maximized window with minimize, maximize, and close icons
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    pygame.display.set_caption("Hive Game")
    clock = pygame.time.Clock()

    # Hex map objects
    hex_map_on_menu = HexMap()
    hex_map = HexMap()  # Hex_map_on_board

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
    def general_get_hex_number(q, r):
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

    def add_pieces(positions, color):
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

    add_pieces(positions_white, "W")
    add_pieces(positions_black, "B")

    def draw_hexagons(positions, color1, color2):
        for x, y in positions:
            if(get_hex_number(pixel_to_hex(x,y,HEX_SIZE_Board,screen_width,screen_height)[0],pixel_to_hex(x,y,HEX_SIZE_Board,screen_width,screen_height)[1]) == None): 
                x+=hex_map.x
                y+=hex_map.y
                #print(x,y)
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
    
    def Test_Map(screen, hex_map, selected_hex, HEX_SIZE_Board, HEX_COLOR, SELECTED_COLOR, BORDER_COLOR):
    
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

    #Initial Values
    selected_hex = (0, 0)
    preselected_hex = selected_hex #the previous value of selected_hex
    running = True
    dragging = False
    last_mouse_pos = (0, 0)
    draw_flag = False
    hex_number = 0 

    while running:
        
        screen.blit(background, (0, 0))
        #Draw hexagons
        #Test_Map(screen,hex_map,selected_hex,HEX_SIZE_Board,HEX_COLOR,SELECTED_COLOR,BORDER_COLOR)
        
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
                    #get the name and color and img of the selected piece
                    result_menu = hex_map_on_menu.get_piece(selected_hex[0],selected_hex[1]) 
                    result_board = hex_map.get_piece(selected_hex[0],selected_hex[1])
                    print("preselected")
                    print(preselected_hex,hex_map_on_menu.get_piece(preselected_hex[0], preselected_hex[1]))
                    print("selected")
                    print(selected_hex,hex_map.get_piece(selected_hex[0], selected_hex[1]))
                    
                    ########################## Code to enter the piece from menu to board ################################### 
                    if(result_menu != None):#to ensure that the currect selected piece is on menu
                        name_on_menu,color_on_menu,img_on_menu = result_menu
                        #print("000")
                        if(not draw_flag or (result_menu != None and hex_map_on_menu.get_piece(preselected_hex[0],preselected_hex[1]) != None)):#to handle the succesive clicks on multible pieces on menu
                            #print("111")
                            list = AvailablePositions(hex_map,hex_map.Turn)
                            draw_flag = True
                            preselected_hex = selected_hex
                    ########################## Code to enter the piece from board to board ################################### 
                    elif(result_board != None):
                        name_on_board,color_on_board,img_on_board = result_board
                        #print(color_on_board)
                        if(color_on_board != hex_map.Turn):
                            draw_flag=False
                            continue
                        name_on_board = name_on_board[:-1]
                        print("1010")
                        if((hex_map_on_menu.get_piece(preselected_hex[0],preselected_hex[1]) != None) and (hex_map_on_menu.get_piece(selected_hex[0],selected_hex[1]) == None)):
                            print("000")
                            preselected_hex=(0,0)
                        prevresult_on_board_1click = hex_map.get_piece(preselected_hex[0],preselected_hex[1])
                        if (prevresult_on_board_1click != None):
                            prev_name_board_1click , prev_color_board_1click , prev_img_board_1click = prevresult_on_board_1click 
                            prev_name_board_1click = prev_name_board_1click[:-1]
                        if(not draw_flag or (result_board != None and prevresult_on_board_1click != None)):  
                            draw_flag = True
                            flag = True

                            if(prev_name_board_1click == "Beetle"): 
                                   list = AvailablePositions_Beetle(hex_map,preselected_hex[0],preselected_hex[1])
                                   print(list)
                                   for element in list: 
                                        if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):
                                            #selected_hex = preselected_hex
                                            flag =False
                                            print(555)
                                            break
                                        else:
                                            flag = True 
                            else:
                                print(666)
                                preselected_hex = selected_hex  
                            if(flag == True):
                                print(444)
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
                                match name_on_board_3:
                                    case "Queen":
                                        list = Available_Positions_Queen(hex_map,preselected_hex[0],preselected_hex[1])
                                        
                                    case "Ant":
                                         list = AvailablePositions_Ant(hex_map,preselected_hex[0],preselected_hex[1])
                                        
                                    case "Grasshopper":
                                        list = AvailablePositions_GrassHopper(hex_map,preselected_hex[0],preselected_hex[1])
                                
                                    case "Spider":
                                            list = Available_Positions_Spider(hex_map,preselected_hex[0],preselected_hex[1])

                                    case "Beetle":
                                        list = AvailablePositions_Beetle(hex_map,preselected_hex[0],preselected_hex[1])
                            else:
                                draw_flag = False
                                  
                    if (draw_flag):
                        #print("222")  
                        for element in list:
                            #check 2 left clicking 
                            #print(element)
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
                                            print(777)
                                    if (name1 == "Beetle" and flag == False):
                                        print(111)
                                        hex_map.move_beetle(preselected_hex[0],preselected_hex[1],selected_hex[0],selected_hex[1])
                                    else:
                                        hex_map.add_piece(selected_hex[0],selected_hex[1],name,color,img)
                                        hex_map.remove_piece(preselected_hex[0],preselected_hex[1]) 
                                    print(f"outcast :{hex_map.OutCasts}")
                                    # print(f"Hex_Map :{hex_map.map}")
                                draw_flag=False
                                hex_number = general_get_hex_number(preselected_hex[0],preselected_hex[1])
                                
                                #print(preselected_hex)
                                #print(f"the hex number is : {hex_number,hex_map.Turn}")
                                preselected_hex= (0,0)
                                h2p_x,h2p_y = hex_to_pixel(*selected_hex,HEX_SIZE_Board,screen_width,screen_height)
                                if(hex_map.Turn == "W" and (hex_number>10 and hex_number<22)):
                                    # print(hex_number)
                                    # print(hex_map.Turn)
                                    positions_white[hex_number-11]=h2p_x,h2p_y
                                    hex_map.Turn = "B"
                                elif(hex_map.Turn == "B" and (hex_number>-1 and hex_number<11)):
                                    # print("555")
                                    # print(hex_number)
                                    # print(hex_map.Turn)
                                    positions_black[hex_number]=h2p_x,h2p_y
                                    hex_map.Turn = "W"
                                break
                            #Deselecting

                            elif(((hex_map_on_menu.get_piece(selected_hex[0],selected_hex[1]) == None) and (result == None)) and (selected_hex[0] != element[0] and selected_hex[1] != element[1])):
                                # for element1 in list:
                                #     if (selected_hex[0] == element[0] and selected_hex[1] == element[1]):

                                #print("444")
                                draw_flag = False
                                # preselected_hex = (0,0)
                                continue
                            
            # Call the change_map_position function to the map on board(hex_map)
            dragging, last_mouse_pos = change_map_position(
                event, dragging, last_mouse_pos,hex_map
            )
        
        
        if(draw_flag):
            #print("555")
            #print("Available Positions:", list)
            for hamada in list: 
                x,y = hex_to_pixel( hamada[0],hamada[1],HEX_SIZE_Board,screen_width,screen_height)
                x+=hex_map.x
                y+=hex_map.y
                draw_hexagon(screen,x,y, SELECTED_COLOR, BORDER_COLOR, HEX_SIZE_Board)

        
        draw_player("Ahmed Gamal", "Deatrex", "Human-Human", screen)
        #print(pixel_to_hex(768,432,HEX_SIZE_Board))
        #print(f"{positions_white}")
        draw_hexagons(positions_white, WHITE_PLAYER, BORDER_COLOR)
        draw_hexagons(positions_black, BLACK_PLAYER, BORDER_COLOR) 
        result = hex_map.get_piece(selected_hex[0],selected_hex[1])
        if(result != None):
            name_on_board_2 ,color_on_board_2,img_on_board_2 = result
            name_on_board_2 = name_on_board_2[:-1]
            if(draw_flag and name_on_board_2 == "Beetle"):
                for hamada in list: 
                    x,y = hex_to_pixel( hamada[0],hamada[1],HEX_SIZE_Board,screen_width,screen_height)
                    x+=hex_map.x
                    y+=hex_map.y
                    draw_hexagon(screen,x,y, SELECTED_COLOR, BORDER_COLOR, HEX_SIZE_Board)
            
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()


if __name__ == "__main__":
    main()




