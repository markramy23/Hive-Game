# HexMap class to store pieces on the hex map
class HexMap:
    def __init__(self):
        self.map = {}
        self.queen_placed = {"W": False, "B": False}
        self.White_turn_count = 0
        self.Black_turn_count = 0
        self.Turn = "W"
        self.Length = 0
        self.OutCasts = []

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

    def move_beetle(self, q, r, new_q, new_r):
        if (new_q, new_r) in self.map.keys():
            self.OutCasts.append(((new_q, new_r), self.map[(new_q, new_r)]))
        self.map[(new_q, new_r)] = self.map.pop((q, r))
        for OutCast in self.OutCasts:
            if OutCast[0] == (q, r):
                self.map[OutCast[0]] = OutCast[1]

    def get_Empty_neighbors(self, q, r):
        """Returns a list of neighboring hexes for the given hex."""
        directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
        return [(q + dq, r + dr, self.map[(q, r)][1]) for dq, dr in directions if (q + dq, r + dr) not in self.map]
