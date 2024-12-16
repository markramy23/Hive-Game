from Hex_map import HexMap
from Available_positions import *
from Utilities import *
import random
import re
import pdb
import rules

''' Dictionary for the available positions for each piece '''
Pieces_Available_Positions = {
    "Queen": Available_Positions_Queen,
    "Ant": AvailablePositions_Ant,
    "Grasshopper": AvailablePositions_GrassHopper,
    "Beetle": AvailablePositions_Beetle,
    "Spider": Available_Positions_Spider

}

'''
Return the number of free pieces for a specific Player
args: 
    hex_map : HexMap object
    color : the color of the Player
    
return: the number of free pieces for the player
'''


def FreePieces(hex_map: HexMap, color):
    cnt = 0
    for (key, value) in list(hex_map.map.items()):  # for every piece in the hex_map
        if color == value[1]:  # if the color of the piece is the same as the player
            if value[0][:-1] == "Spider" or value[0][:-1] == "Ant":
                if len(Available_Positions_Queen(hex_map, key[0], key[1])) > 0:
                    cnt += 1
            elif len(Pieces_Available_Positions[value[0][:-1]](hex_map, key[0],
                                                               key[1])) > 0:  # if the piece has available positions
                cnt += 1  # increment the count

    return cnt


# import multiprocessing
# from typing import Dict, Tuple
# from concurrent.futures import ProcessPoolExecutor, as_completed
#
#
# def process_piece(hex_map: Dict, piece_key: Tuple, piece_value: Tuple, color: str) -> bool:
#     """
#     Process a single piece to check if it has available positions.
#
#     :param hex_map: The hex map dictionary
#     :param piece_key: The key of the piece in the map
#     :param piece_value: The value (piece details) associated with the key
#     :param color: The color to check against
#     :return: True if the piece has available positions, False otherwise
#     """
#     # If the piece color matches the player color
#     if color == piece_value[1]:
#         piece_type = piece_value[0][:-1]  # Remove potential suffix like '1', '2' etc.
#
#         # Special handling for Spider and Ant pieces
#         if piece_type in ["Spider", "Ant"]:
#             available_positions = Available_Positions_Queen(hex_map, piece_key[0], piece_key[1])
#             return len(available_positions) > 0
#
#         # For other piece types
#         available_positions = Pieces_Available_Positions[piece_type](hex_map, piece_key[0], piece_key[1])
#         return len(available_positions) > 0
#
#     return False
#
#
# def FreePieces(hex_map: HexMap, color: str) -> int:
#     """
#     Count free pieces in parallel with thread-safe counting.
#
#     :param hex_map: The hex map to process
#     :param color: The color of pieces to check
#     :return: Number of free pieces
#     """
#     # Use a thread-safe counter
#     manager = multiprocessing.Manager()
#     cnt = manager.Value('i', 0)
#
#     # Use a lock to ensure mutual exclusion when updating the counter
#     lock = manager.Lock()
#
#     def update_counter(is_free_piece):
#         """Increment counter in a thread-safe manner."""
#         if is_free_piece:
#             with lock:
#                 cnt.value += 1
#
#     # Use ProcessPoolExecutor for parallel processing
#     piece_keys =list(hex_map.map.keys())
#     piece_values = [value[:-1] for value in hex_map.map.values()]
#     with ProcessPoolExecutor() as executor:
#         # Submit all pieces for processing
#         futures = [
#             executor.submit(
#                 process_piece,
#                 hex_map,
#                 piece_key,
#                 piece_value,
#                 color
#             ) for piece_key , piece_value in zip(piece_keys,  piece_values)
#         ]
#
#         # Process results as they complete
#         for future in as_completed(futures):
#             update_counter(future.result())
#
#     return cnt.value


# Note: Assumes these functions exist in the current scope
# Available_Positions_Queen()
# Pieces_Available_Positions dictionary

'''
Check if the Queen is surrounded by the opponent's pieces
args: 
    color : the color of the Queen
    hex_map : HexMap object
return: True if the Queen is surrounded by the opponent's pieces, False otherwise
'''


def isQueenSurrounded(color, hex_map: HexMap):
    for (key, value) in hex_map.map.items():  # for every piece in the hex_map
        if piece_type_match(value[0], "Queen") and color == value[1]:  # if the piece is a Queen and has the same color as the player
            # if value[0] == "Queen" and color == value[1]: #if the piece is a Queen and has the same color as the player
            if len(hex_map.get_neighbors(key[0], key[1])) == 6:  # if the Queen has 6 neighbors (surrounded) return True
                return True
            else:
                return False
    for key,value in hex_map.OutCasts:
        if value[0][:-1] == "Queen" and color == value[1]:
            if len(hex_map.get_neighbors(key[0],key[1])) == 6:  # if the Queen has 6 neighbors (surrounded) return True
                    return True
            else:
                    return False



''' 
Calculate the value of the board (Heuristics Value) based on the number of pieces around the opponent's Queen, 
the number of free pieces for each player, 
and the difference between the number of turns for each player
the value is calculated as follows:
    20 * (number of black pieces around the white Queen - number of white pieces around the black Queen) + 
    1 * (number of white turns - number of black turns) + 
    5 * (number of white free pieces - number of black free pieces)
The function returnes +ve value for whie player and -ve value for black player
args: 
    hex_map : HexMap object
    ActivePlayer : the color of the active player
return: the value of the board
'''
# def CalculateBoardValue(hex_map: HexMap, ActivePlayer):
#     whiteQueen = 0
#     blackQueen = 0
#     blackWon = isQueenSurrounded("W", hex_map) #check if the black Queen is surrounded
#     whiteWon = isQueenSurrounded("B", hex_map) #check if the white Queen is surrounded
#     #if both Queens are surrounded (Draw) treat it as lose so the ai shouldn't choose this move as the best move
#     if blackWon == True and whiteWon == True:
#         #if the active player is white return -ve infinity
#         if ActivePlayer == "W":
#             return (INTMIN)
#         else:
#             return (INTMAX)
#     #if the black player won return -ve infinity
#     elif blackWon == True:
#         return INTMIN
#     #if the white player won return +ve infinity
#     elif whiteWon == True:
#         return INTMAX
#     #get the positions of the white and black Queens
#     for (key, value) in hex_map.map.items():
#         if piece_type_match(value[0],"Queen") and value[1] == "W":
#         # if value[0] == "Queen" and value[1] == "W":
#             whiteQueen = (key, value)
#         elif piece_type_match(value[0],"Queen") and value[1] == "B":
#         # elif value[0] == "Queen" and value[1] == "B":
#             blackQueen = (key, value)
#
#     #count the number of black pieces around the white Queen and the number of white pieces around the black Queen
#     BlackHexesAround_WQ = []
#     if (whiteQueen != 0):
#         NonEmptyNeighbours_WQ = hex_map.get_neighbors(whiteQueen[0][0], whiteQueen[0][1])
#         for Neighbour in NonEmptyNeighbours_WQ:
#             if hex_map.get_piece(Neighbour[0], Neighbour[1])[1] == "B":
#                 BlackHexesAround_WQ.append(Neighbour)
#     #count the number of white pieces around the black Queen and the number of black pieces around the white Queen
#     whiteHexesAround_BQ = []
#     if (blackQueen != 0):
#         NonEmptyNeighbours_BQ = hex_map.get_neighbors(blackQueen[0][0], blackQueen[0][1])
#         for Neighbour in NonEmptyNeighbours_BQ:
#             if hex_map.get_piece(Neighbour[0], Neighbour[1])[1] == "W":
#                 whiteHexesAround_BQ.append(Neighbour)
#
#     #calculate the number of free pieces (pieces with available moves to play) for each player
#     numberOfWhiteFreePieces = FreePieces(hex_map, "W")
#     numberOfBlackFreePieces = FreePieces(hex_map, "B")
#     #calculate the value of the board
#     return 20 * (len(whiteHexesAround_BQ) - len(BlackHexesAround_WQ)) + 1 * (
#                 hex_map.White_turn_count - hex_map.Black_turn_count) + 5 * (
#                 numberOfWhiteFreePieces - numberOfBlackFreePieces)

'''
Check if the game is over by checking if one of the Queens is surrounded
args: hex_map : HexMap object
return: True if the game is over, False otherwise
'''


def GameOver(hex_map: HexMap):
    # check if one of the Queens is surrounded
    blackDead = isQueenSurrounded("B", hex_map)
    whiteDead = isQueenSurrounded("W", hex_map)
    return blackDead or whiteDead


'''
claculate the heuristic value of the board based on the player
for the white player the value is calculated as the value of the board
for the black player the value is calculated as the negative value of the board
args:
    hex_map : HexMap object
    player : the color of the player
return: the value of the board based on the player
'''


def calculateValue(hex_map: HexMap, player):
    vlaue = CalculateBoardValue(hex_map, player)
    if (player == "W"):
        return vlaue
    else:
        return -vlaue


'''
Minimax algorithm to calculate the best move for the player
args:
    hex_map : hexmap representing the board
    depth : the depth of the search tree
    maximizingPlayer : a boolean to indicate if the player is maximizing or minimizing
    player : the color of the player
    hex_map_on_menu : hexmap representing the pieces not placed on the board yet
return: the value of the best move
'''


def minimax(hex_map: HexMap, depth, maximizingPlayer, root_player, active_player, hex_map_on_menu: HexMap):
    # if max depth was reached or game was over calculate the heuristics and return the value based on the player
    if GameOver(hex_map) or depth == 0:
        return calculateValue(hex_map, root_player)
    else:
        # generate the possible moves for the player
        moves = generateMoves(hex_map, active_player, hex_map_on_menu)
        # initialize the best value based on the player
        if maximizingPlayer:
            bestValue = INTMIN
        else:
            bestValue = INTMAX
        # for each move apply the move and calculate the value of the move
        for move in moves:
            # if move[5] == "Beetle1" and move[6] == "W":
            #     print("ostor ya rb")
            applyMove(hex_map, hex_map_on_menu, move)  # apply the move
            # value = minimax(hex_map, depth - 1, not maximizingPlayer, player, hex_map_on_menu) #recursive call to calculate the value of the move
            value = minimax(hex_map, depth - 1, not maximizingPlayer, root_player, get_next_player(active_player),
                            hex_map_on_menu)  # recursive call to calculate the value of the move

            if maximizingPlayer:
                bestValue = max(bestValue, value)  # update the best value
            else:
                bestValue = min(bestValue, value)  # update the best value
            # if move[5] == "Beetle1" and move[6] == "W":
            #     print("ostor ya rb")
            undoMove(hex_map, hex_map_on_menu, move)  # undo the move
        # return the best value
        return bestValue


def minimax_alpha_beta(hex_map: HexMap, depth, maximizingPlayer, root_player, active_player, alpha, beta,
                       hex_map_on_menu: HexMap):
    # Base case: if max depth is reached or game is over, calculate the heuristic value for the player
    if GameOver(hex_map) or depth == 0:
        return calculateValue(hex_map, root_player)

    moves = generateMoves(hex_map, active_player, hex_map_on_menu)
    # if(depth == 1):
    #     moves = sort_moves(hex_map, hex_map_on_menu, moves, root_player,maximizingPlayer)
    if maximizingPlayer:
        bestValue = alpha  # Start with alpha for maximizing player
    else:
        bestValue = beta  # Start with beta for minimizing player

    for move in moves:
        applyMove(hex_map, hex_map_on_menu, move)  # Apply the move
        '''#################################Debugging####################################'''
        # where_is_my_queen(hex_map)
        value = minimax_alpha_beta(hex_map, depth - 1, not maximizingPlayer, root_player,
                                   get_next_player(active_player), alpha, beta,
                                   hex_map_on_menu)  # Recursive call
        '''#################################Debugging####################################'''
        # where_is_my_queen(hex_map)
        undoMove(hex_map, hex_map_on_menu, move)  # Undo the move

        if maximizingPlayer:
            bestValue = max(bestValue, value)
            alpha = max(alpha, value)
        else:
            bestValue = min(bestValue, value)
            beta = min(beta, value)

        # Pruning
        if beta <= alpha:
            return bestValue  # Early return when pruning

    return bestValue


'''
Generate the possible moves for the player
args:
    hex_map : hexmap representing the board
    Player : the color of the player
    hex_map_on_menu : hexmap representing the pieces not placed on the board yet
return: a list of possible moves
'''


def generateMoves(hex_map: HexMap, Player, hex_map_on_menu: HexMap):
    Result = []
    for (key, value) in list(hex_map.map.items()):
        if not does_removal_break_hive(hex_map.map, key):
            if Player == value[1]:
                print(value[0][:-1])
                for Pos in Pieces_Available_Positions[value[0][:-1]](hex_map, key[0], key[1]):
                    Result.append(("move", key[0], key[1], Pos[0], Pos[1], value[0], value[1], value[2]))
    for (key, value) in hex_map_on_menu.map.items():
        if Player == value[1]:
            for Pos in AvailablePositions(hex_map, Player, value[0]):
                Result.append(("add", key[0], key[1], Pos[0], Pos[1], value[0], value[1], value[2]))

    # Result contains tuples of ("move" or "add",Current q , Current r , next q , next r , name, color )
    return Result


def applyMove(hex_map: HexMap, hex_map_on_menu: HexMap, move):
    if (move[0] == "move"):
        if move[5][:-1] == "Beetle":
            hex_map.move_beetle(move[1], move[2], move[3], move[4])
        else:
            hex_map.move_piece(move[1], move[2], move[3], move[4])

    elif (move[0] == "add"):
        hex_map.add_piece(move[3], move[4], move[5], move[6], move[7])
        hex_map_on_menu.remove_piece(move[1], move[2])


def undoMove(hex_map: HexMap, hex_map_on_menu: HexMap, move):
    # hex_map.move_piece(move[2], move[3], move[0], move[1])

    if (move[0] == "move"):
        if move[5][:-1] == "Beetle":
            hex_map.move_beetle(move[3], move[4], move[1], move[2])
        else:
            hex_map.move_piece(move[3], move[4], move[1], move[2])
    elif (move[0] == "add"):
        #  remove_piece(self, q, r):
        hex_map.remove_piece(move[3], move[4])
        hex_map_on_menu.add_piece(move[1], move[2], move[5], move[6], move[7])


def nextMove(hex_map, hex_map_on_menu: HexMap, depth, player):
    moves = generateMoves(hex_map, player, hex_map_on_menu)
    bestValue = INTMIN
    bestMove = []
    for move in moves:

        applyMove(hex_map, hex_map_on_menu, move)
        # value = minimax(hex_map, depth - 1, False, player, hex_map_on_menu)
        value = minimax(hex_map, depth - 1, False, player, get_next_player(player), hex_map_on_menu)
        if (value > bestValue or value == bestValue and random.choice([True, False])):
            bestValue = value
            bestMove = move

        undoMove(hex_map, hex_map_on_menu, move)

    return bestMove


def nextMove_alpha_beta(hex_map, hex_map_on_menu: HexMap, depth, player):
    moves = generateMoves(hex_map, player, hex_map_on_menu)
    # print("moves", moves)
    # moves = sort_moves(hex_map, hex_map_on_menu, moves, player,True)
    # print("sorted moves", moves)
    bestValue = INTMIN
    bestMove = []
    alpha = INTMIN
    beta = INTMAX
    for move in moves:
        applyMove(hex_map, hex_map_on_menu, move)

        value = minimax_alpha_beta(hex_map, depth - 1, False, player, get_next_player(player), alpha, beta,
                                   hex_map_on_menu)
        if (value > bestValue or value == bestValue and random.choice([True, False])):
            bestValue = value
            bestMove = move

        undoMove(hex_map, hex_map_on_menu, move)
    return bestMove


def nextMove_alpha_beta_loser(hex_map, hex_map_on_menu: HexMap, depth, player):
    moves = generateMoves(hex_map, player, hex_map_on_menu)
    # print("moves", moves)
    # moves = sort_moves(hex_map, hex_map_on_menu, moves, player,True)
    # print("sorted moves", moves)
    bestValue = INTMAX
    bestMove = []
    alpha = INTMIN
    beta = INTMAX
    for move in moves:

        applyMove(hex_map, hex_map_on_menu, move)

        value = minimax_alpha_beta(hex_map, depth - 1, True, player, get_next_player(player), alpha, beta,
                                   hex_map_on_menu)
        if (value < bestValue or value == bestValue and random.choice([True, False])):
            bestValue = value
            bestMove = move

        undoMove(hex_map, hex_map_on_menu, move)
    return bestMove


'''
Return the type of the piece
args: 
    piece_name : the name of the piece
return: the type of the piece
'''
def get_picec_type(piece_name):
    return re.sub(r'\d+', '', piece_name)


def piece_type_match(piece_name, piece_type):
    return get_picec_type(piece_name).casefold() == piece_type.casefold()


def get_next_player(player):
    if player == "W":
        return "B"
    else:
        return "W"


def where_is_my_queen(hex_map: HexMap):
    flag = False
    for (key, value) in hex_map.map.items():
        if value[0] == "Queen1" and value[1] == "W":
            flag = True
            break

    if not flag:
        for element in hex_map.OutCasts:
            if element[1][0] == "Queen1" and element[1][1] == "W":
                flag = True
                break
    if not flag:
        print("Queen not found")


def sort_moves(hex_map, hex_map_on_menu, moves, root_player, maximizingPlayer):
    # Sort the moves based on the value of the board after applying the move
    sorted_moves = []
    for move in moves:
        applyMove(hex_map, hex_map_on_menu, move)
        value = CalculateBoardValue(hex_map, root_player)
        sorted_moves.append((move, value))
        undoMove(hex_map, hex_map_on_menu, move)
    print("Maximizing Player?: ", maximizingPlayer)
    print(sorted_moves)
    sorted_moves.sort(key=lambda x: x[1], reverse=maximizingPlayer)
    print(sorted_moves)
    return [move[0] for move in sorted_moves]


def CalculateValueOfPieces(hex_map: HexMap, Player):
    Score = 0
    for (key, value) in hex_map.map.items():
        if value[1] == Player:
            if value[0][1] == "Q":
                Score += 9
            elif value[0][1] == "S":
                Score += 3
            elif value[0][1] == "A":
                Score += 4
            elif value[0][1] == "G":
                Score += 2
            elif value[0][1] == "B":
                Score += 5
    return Score


''' 
Calculate the value of the board (Heuristics Value) based on the number of pieces around the opponent's Queen, 
the number of free pieces for each player, 
and the difference between the number of turns for each player
the value is calculated as follows:
    20 * (number of black pieces around the white Queen - number of white pieces around the black Queen) + 
    1 * (number of white turns - number of black turns) + 
    5 * (number of white free pieces - number of black free pieces)
The function returnes +ve value for whie player and -ve value for black player
args: 
    hex_map : HexMap object
    ActivePlayer : the color of the active player
return: the value of the board
'''
def CalculateBoardValue(hex_map: HexMap, ActivePlayer):
    whiteQueen = 0
    blackQueen = 0
    blackWon = isQueenSurrounded("W", hex_map)  # check if the black Queen is surrounded
    whiteWon = isQueenSurrounded("B", hex_map)  # check if the white Queen is surrounded
    # if both Queens are surrounded (Draw) treat it as lose so the ai shouldn't choose this move as the best move
    if blackWon == True and whiteWon == True:
        # if the active player is white return -ve infinity
        if ActivePlayer == "W":
            return (INTMIN)
        else:
            return (INTMAX)
    # if the black player won return -ve infinity
    elif blackWon == True:
        return INTMIN
    # if the white player won return +ve infinity
    elif whiteWon == True:
        return INTMAX
    # get the positions of the white and black Queens
    for (key, value) in hex_map.map.items():
        if piece_type_match(value[0], "Queen") and value[1] == "W":
            # if value[0] == "Queen" and value[1] == "W":
            whiteQueen = (key, value)
        elif piece_type_match(value[0], "Queen") and value[1] == "B":
            # elif value[0] == "Queen" and value[1] == "B":
            blackQueen = (key, value)

    # count the number of black pieces around the white Queen and the number of white pieces around the black Queen
    BlackHexesAround_WQ = []
    if (whiteQueen != 0):
        NonEmptyNeighbours_WQ = hex_map.get_neighbors(whiteQueen[0][0], whiteQueen[0][1])
        for Neighbour in NonEmptyNeighbours_WQ:
            if hex_map.get_piece(Neighbour[0], Neighbour[1])[1] == "B":
                BlackHexesAround_WQ.append(Neighbour)
    # count the number of white pieces around the black Queen and the number of black pieces around the white Queen
    whiteHexesAround_BQ = []
    if (blackQueen != 0):
        NonEmptyNeighbours_BQ = hex_map.get_neighbors(blackQueen[0][0], blackQueen[0][1])
        for Neighbour in NonEmptyNeighbours_BQ:
            if hex_map.get_piece(Neighbour[0], Neighbour[1])[1] == "W":
                whiteHexesAround_BQ.append(Neighbour)

    # calculate the number of free pieces (pieces with available moves to play) for each player
    numberOfWhiteFreePieces = FreePieces(hex_map, "W")
    numberOfBlackFreePieces = FreePieces(hex_map, "B")
    ############################################################################################
    ScoresOfWhitePieces = CalculateValueOfPieces(hex_map, "W")
    ScoresOfBlackPieces = CalculateValueOfPieces(hex_map, "B")
    # calculate the value of the board
    return 20 * (len(whiteHexesAround_BQ) - len(BlackHexesAround_WQ)) + 1 * (
            hex_map.White_turn_count - hex_map.Black_turn_count) + 5 * (
            numberOfWhiteFreePieces - numberOfBlackFreePieces) + 1 * (ScoresOfWhitePieces - ScoresOfBlackPieces)


def next_move_iterative_deepening(hex_map, hex_map_on_menu, turn_start_time,turn_duration, player):
    from modes import Remaining_Turn_Time
    depth = 2
    best_move = None
    while Remaining_Turn_Time(turn_start_time, turn_duration):
        if player == "W":
            best_move = nextMove_alpha_beta(hex_map, hex_map_on_menu, depth, player)
        else:
            best_move = nextMove_alpha_beta_loser(hex_map, hex_map_on_menu, depth, player)
        depth += 1
    return best_move

def calculate_score(hex_map:HexMap,player):
    piece_scores = {
        "Queen": 9,
        "Ant": 4,
        "Grasshopper": 2,
        "Beetle": 5,
        "Spider": 3
    }
    score = 0
    empty_cells = 0
    for key,value in hex_map.map.items():
        if value[1] == player:#COLOR
            score += piece_scores[value[0][:-1]]
    if(player == "W" and hex_map.queen_placed["B"]):
        for key,value in hex_map.map.items():
            if value[0][:-1] == "Queen" and value[1]=="B":#NAME
                empty_cells = len(hex_map.get_Empty_neighbors(key[0],key[1]))
    elif(player == "B" and hex_map.queen_placed["W"]):
        for key, value in hex_map.map.items():
            if value[0][:-1] == "Queen" and value[1] == "W":
                empty_cells = len(hex_map.get_Empty_neighbors(key[0], key[1]))

    return score-(empty_cells*2)
