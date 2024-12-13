# HexMap class to store pieces on the hex-map
class HexMap:
    def __init__(self):
        self.x=0
        self.y=0
        self.map = {}
        self.queen_placed = {"W": False, "B": False}
        self.White_turn_count = 0
        self.Black_turn_count = 0
        self.Turn = "W"
        self.Length = 0
        self.OutCasts = []

    def add_piece(self, q, r, name, color, Img):
        self.Length += 1
        self.map[(q, r)] = (name, color, Img)
        name = name[:-1]
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
                self.Turn = "W"  # Switch turn to the opposite color
            else:
                self.Black_turn_count -= 1
                self.Turn = "B"  # Switch turn to the opposite color

            # Update queen placed status
            if name[:-1] == "Queen":
                self.queen_placed[color] = False

            return name, color, Img  # Return the removed piece details
        else:
            print(f"No piece found at ({q}, {r}) to remove.")
            return None

    
    def get_piece(self, q, r):
        """Retrieve the name  color and img of the piece at the specified coordinates."""
        piece = self.map.get((q, r))
        if piece:
            #print(piece)
            name, color, img = piece  # Extract name and color from the tuple
            
            return name, color , img
        return None  # Return None if no piece exists at the specified coordinates

    def move_piece(self, q, r, new_q, new_r):
        self.map[(new_q, new_r)] = self.map.pop((q, r))

    def get_neighbors(self, q, r):
        """Returns a list of neighboring hexes for the given hex."""
        directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
        return [(q + dq, r + dr) for dq, dr in directions if (q + dq, r + dr) in self.map]
    # q,r = beetle1, qnew,rnew = beetle2
    def move_beetle(self, q, r, new_q, new_r):
        if (new_q, new_r) in self.map.keys():
            self.OutCasts.append(((new_q, new_r), self.map[(new_q, new_r)]))
        self.map[(new_q, new_r)] = self.map.pop((q, r))
        for OutCast in reversed(self.OutCasts):
            if OutCast[0] == (q, r):
                self.map[OutCast[0]] = OutCast[1]
                self.OutCasts.remove(OutCast)
                break

    def get_Empty_neighbors(self, q, r):
        """Returns a list of neighboring hexes for the given hex."""
        directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
        return [(q + dq, r + dr, self.map[(q, r)][1]) for dq, dr in directions if (q + dq, r + dr) not in self.map]
    
    # def did_Player_Lose(self,Queen_q,Queen_r):
    #     empty_cells = get_Empty_neighbors(self,Queen_q,Queen_r)
    #     if (empty_cells < 2):
    #         return True
    #     elif(empty_cells >= 4):
    #         return False
    #     else:
    #         directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
    #         # for i, outer_point in enumerate(empty_cells):
    #         #     for inner_point in empty_cells[i+1:]:
    #         for i in range(6):
    #             if( self.map[Queen_q+directions[i][0] , Queen_r+directions[i][1]]) and self.map[Queen_q+directions[i+1][0] , Queen_r+directions[i+1][1]] :
                    

    def did_Player_Lose(self, Queen_q, Queen_r):
        """
        Check if there are two neighboring free places in a hexagonal grid.
        
        Args:
        free_places (list of tuple): List of free hexagon coordinates (q, r).
        
        Returns:
        bool: True if there are two neighboring free places, False otherwise.
        """
        empty_cells = self.get_Empty_neighbors(Queen_q,Queen_r)
        if (len(empty_cells) > 0):
            return False
        else:
            return True
