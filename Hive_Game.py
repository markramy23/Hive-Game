import pygame
import math
import copy 
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
    if not empty_neighbours:
        return result
    non_empty_neighbours = hex_map.get_neighbors(q, r)
    # print(empty_neighbours)
    for element in empty_neighbours:
        neighbors = hex_map.get_neighbors(element[0], element[1])
        neighbors.remove((q, r))
        if len(neighbors) != 0:
            flag = False
            for neighbor2 in neighbors:
                if neighbor2 in non_empty_neighbours:
                    flag = True
                    break
            if flag:
                result.append((element[0], element[1]))
    print(result)
    result = list(FreedomToMove(hex_map, empty_neighbours, result))
    print(result)
    return result

#Spider Available Positions
#Working (for now) (bugs may be found later) :(
def Available_Positions_Spider(hex_map, q, r):
    visited = set() #set to add all visited positions
    result = set()
    visited.add((q, r)) #consider the current position as visited to avoid backtracking to the same position
    temp = Available_Positions_Queen(hex_map, q, r)   #get all available positions as queen movement

    #for every initial position do a depth first search with depth of 3 to reach the end of all available positions
    for pos in temp:
        new_q = pos[0]
        new_r = pos[1]
        hex_map.move_piece(q, r,new_q, new_r)
        visited.add((new_q, new_r))
        temp2 = Available_Positions_Queen(hex_map, new_q, new_r)
        for pos2 in temp2:
            if pos2 in visited:
                continue
            new_q2 = pos2[0]
            new_r2 = pos2[1]
            hex_map.move_piece(new_q, new_r, new_q2, new_r2)
            visited.add((new_q2, new_r2))
            temp3 = Available_Positions_Queen(hex_map, new_q2, new_r2)
            visited.update(temp)
            for pos3 in temp3:
                if pos3 in visited:
                    continue
                result.add(pos3)
            hex_map.move_piece(new_q2, new_r2, new_q, new_r)
        hex_map.move_piece(new_q, new_r, q, r)
    return list(result)



SoldierAntVisited= set()
SoldierAntResult=set()
def AvailablePositions_Ant (hex_map, q, r):
    AvailablePositions_SoldierAnt(hex_map, q, r)
    SoldierAntResult.remove((q,r))
    result = copy.deepcopy(SoldierAntResult) ;
    SoldierAntResult.clear();
    SoldierAntVisited.clear();


    return list(result)


def AvailablePositions_SoldierAnt(hex_map, q, r):
    SoldierAntVisited.add((q,r)) ;
    children =Available_Positions_Queen(hex_map, q, r)
    if not children :
        return

    for child in children :
        SoldierAntResult.add(child)
        if child not in SoldierAntVisited :
            hex_map.move_piece(q, r, child[0], child[1])
            AvailablePositions_SoldierAnt(hex_map,child[0],child[1])
            hex_map.move_piece(child[0], child[1], q, r)


    return

def AmazingGrassHopper(hex_map, q, r,dq,dr):

    children=hex_map.get_neighbors(q,r)
    for child in children:
        if child[0] == (q+dq) and child[1]==(r+dr) :
            return AmazingGrassHopper(hex_map,(q+dq),(r+dr) ,dq,dr)
        else:
            return ((q+dq),(r+dr))



def AvailablePositions_GrassHopper (hex_map, q, r ):
    children= hex_map.get_neighbors(q,r)
    result =[]
    for child in children :
        result.append(AmazingGrassHopper(hex_map, child[0], child[1],child[0]-q,child[1]-r) )

    return result

def AvailablePositions_Beetle (hex_map, q, r ):
    results=Available_Positions_Queen(hex_map,q,r)
    results+=hex_map.get_neighbors(q,r)
    return results

# HexMap class to store pieces on the hex map
class HexMap:
    def __init__(self, x=0,y=0):
        self.x=0
        self.y=0
        self.map = {}
        self.queen_placed = {"W": False, "B": False}
        self.White_turn_count = 0
        self.Black_turn_count = 0
        self.Turn = "W"
        self.Length = 0
        self.OutCasts=[]

    def remove_piece(self, q, r):
        """
        Remove a piece from the board at the specified hex coordinates (q, r).

        Args:
            q: The q-coordinate of the hex.
            r: The r-coordinate of the hex.

        Returns:
            The removed piece as a tuple (name, color, Img), or None if no piece was found.
        """
        if (q, r) in self.map:
            # Retrieve and remove the piece
            name, color, Img = self.map.pop((q, r))
            self.Length -= 1

            # Update turn counters
            if color == "W":
                self.White_turn_count -= 1
                self.Turn = "B"  # Switch turn to the opposite color
            else:
                self.Black_turn_count -= 1
                self.Turn = "W"  # Switch turn to the opposite color

            # Update queen placed status
            if name == "Queen":
                self.queen_placed[color] = False

            return name, color, Img  # Return the removed piece details
        else:
            print(f"No piece found at ({q}, {r}) to remove.")
            return None
            
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

    def move_piece(self, q, r, new_q, new_r):
        self.map[(new_q, new_r)] = self.map.pop((q, r))

    def get_neighbors(self, q, r):
        """Returns a list of neighboring hexes for the given hex."""
        directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
        return [(q + dq, r + dr) for dq, dr in directions if (q + dq, r + dr) in self.map]
    
    def move_beetle(self,q,r,new_q,new_r):
        if (new_q,new_r) in self.map.keys() :
            self.OutCasts.append(  ( (new_q,new_r) , self.map[(new_q, new_r)] ) )
        self.map[(new_q, new_r)] = self.map.pop((q, r))
        for OutCast in self.OutCasts :
            if OutCast[0] == (q,r) :
                self.map[OutCast[0]]=OutCast[1]
    
    def find_piece(self, name):
        """Find the coordinates of a piece by its name."""
        for (q, r), piece_name in self.map.items():
            if piece_name == name:
                return q, r
        return None  # If the piece is not found
    
    def get_Empty_neighbors(self, q, r):
        """Returns a list of neighboring hexes for the given hex."""
        directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
        return [(q + dq, r + dr, self.map[(q, r)][1]) for dq, dr in directions if (q + dq, r + dr) not in self.map]

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


def hex_to_pixel(q, r,hex_size):
    """Convert hexagonal (q, r) coordinates to pixel coordinates (x, y)."""
    x = hex_size * (3/2 * q)
    y = hex_size * (math.sqrt(3) * (r + q / 2))
    x += screen_width // 2
    y +=screen_height // 2
    return x, y


def pixel_to_hex(x, y):
    """Convert pixel (x, y) coordinates to hexagonal (q, r) coordinates."""
    x -= WIDTH // 2
    y -= HEIGHT // 2
    q = (2 / 3 * x) / HEX_SIZE
    r = (-1 / 3 * x + math.sqrt(3) / 3 * y) / HEX_SIZE
    return hex_round(q, r)


def FreedomToMove(hex_map,Empty_Neighbours, AvailablePOSs):
    s = set() ;
    directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
    for AvailablePOS in AvailablePOSs :
        Empty_Neighbours_ForAvailablePOS =[]
        for  direction in directions:
            Empty_Neighbours_ForAvailablePOS.append((AvailablePOS[0]+direction[0] , AvailablePOS[1]+direction[1]) )
        for Empty_Neighbour_ForAvailablePOS in Empty_Neighbours_ForAvailablePOS :
            flag =0 ;
            for Empty_Neighbour in Empty_Neighbours :
                if Empty_Neighbour[0] == Empty_Neighbour_ForAvailablePOS[0] and  Empty_Neighbour[1] == Empty_Neighbour_ForAvailablePOS[1] :
                    s.add( AvailablePOS) ;
                    flag=1 ;
                    break ;

            if flag ==1 :
                break ;


    return s

def dfs(grid, current, visited):
    """Perform DFS to traverse the hive."""
    visited.add(current)
    for neighbor in get_neighbors(current, grid):
        if neighbor not in visited:
            dfs(grid, neighbor, visited)


def does_removal_break_hive(grid, removed_piece):
    """
    Determines if removing a piece breaks the hive.

    Args:
    - grid: A dictionary representing the hive { (q, r): piece }
    - removed_piece: The (q, r) coordinates of the piece to be removed.

    Returns:
    - True if removing the piece breaks the hive, False otherwise.
    """
    # Step 1: Identify neighbors of the removed piece
    neighbors = get_neighbors(removed_piece, grid)
    if len(neighbors) < 2:
        # Hive cannot break if the piece has less than 2 neighbors
        return False

    # Step 2: Temporarily remove the piece from the grid
    del grid[removed_piece]

    # Step 3: Start DFS from one neighbor
    start = neighbors[0]
    visited = set()
    dfs(grid, start, visited)

    # Step 4: Check if all other neighbors are reachable
    for neighbor in neighbors[1:]:
        if neighbor not in visited:
            # Not all neighbors are connected; hive is broken
            grid[removed_piece] = "Piece"  # Restore the piece
            return True

    # Step 5: Restore the removed piece and return the result
    grid[removed_piece] = "Piece"
    return False

# Function to draw a single hexagon with its content (duplicated)
def draw_single_hex(q, r, camera_x, camera_y, screen, hex_map, selected_hex):
    """Draws a single hexagon at the specified (q, r) position."""
    x, y = hex_to_pixel(q, r,HEX_SIZE_Board)
    x += screen_width // 2 + camera_x  # Apply camera position
    y += screen_height // 2 + camera_y

    # Determine the fill color
    fill_color = SELECTED_COLOR if (q, r) == selected_hex else HEX_COLOR

    # Draw the hexagon
    draw_hexagon(screen, x, y, fill_color, BORDER_COLOR,HEX_SIZE_Board)

    # Draw the piece, if it exists
    piece = hex_map.get_piece(q, r)
    if piece:
        draw_text_centered(screen, piece, x, y)

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




