from Hex_map import HexMap
from Available_positions import *
from Utilities import *
import random
Pieces_Available_Positions={
    "Queen" : Available_Positions_Queen ,
    "Ant"   : AvailablePositions_Ant ,
    "Grasshopper" : AvailablePositions_GrassHopper ,
    "Beetle"      : AvailablePositions_Beetle ,
    "Spider"      : Available_Positions_Spider

}




def FreePieces (hex_map : HexMap,color):
    cnt=0
    for (key,value) in list(hex_map.map.items()) :
        if color == value[1] :
            if len(Pieces_Available_Positions[value[0][:-1]](hex_map ,key[0],key[1])) >0 :
                cnt +=1

    return cnt


def isQueenSurrounded (color ,hex_map):
    for (key,value) in hex_map.map.items()  :
        if  value[0]=="Queen" and color == value[1] :
            if len(hex_map.get_neighbors(key[0],key[1])) == 6 :
                return True
            else :
                return False



def CalculateBoardValue (hex_map: HexMap , ActivePlayer ):
    whiteQueen=0
    blackQueen=0
    blackWon = isQueenSurrounded("B",hex_map)
    whiteWon = isQueenSurrounded("W",hex_map)
    if blackWon == True and whiteWon == True :
        if ActivePlayer == "W" :
            return (INTMIN)
        else:
            return  (INTMAX)
    elif blackWon == True :
        return INTMIN
    elif whiteWon == True :
        return INTMAX



    for (key ,value) in hex_map.map.items() :
        if value[0] == "Queen"  and value[1]=="W" :
            whiteQueen=(key,value)
        elif value[0] == "Queen"  and value[1]=="B" :
            blackQueen=(key,value)
    BlackHexesAround_WQ = []
    if (whiteQueen!=0):
        NonEmptyNeighbours_WQ = hex_map.get_neighbors(whiteQueen[0][0],whiteQueen[0][1])
        for Neighbour in NonEmptyNeighbours_WQ:
            if hex_map.get_piece(Neighbour[0], Neighbour[1])[1] == "B":
                BlackHexesAround_WQ.append(Neighbour)

    whiteHexesAround_BQ = []
    if (blackQueen!=0):
        NonEmptyNeighbours_BQ = hex_map.get_neighbors(blackQueen[0][0], blackQueen[0][1])
        for Neighbour in NonEmptyNeighbours_BQ:
            if hex_map.get_piece(Neighbour[0], Neighbour[1])[1] == "W":
                whiteHexesAround_BQ.append(Neighbour)

    numberOfWhiteFreePieces= FreePieces(hex_map,"W")
    numberOfBlackFreePieces= FreePieces(hex_map,"B")

    return 20*(len(whiteHexesAround_BQ) - len(BlackHexesAround_WQ))+ 1*(hex_map.White_turn_count -hex_map.Black_turn_count)+ 5*(numberOfWhiteFreePieces - numberOfBlackFreePieces) ;


def GameOver(hex_map : HexMap):
    blackDead = isQueenSurrounded("B", hex_map)
    whiteDead = isQueenSurrounded("W", hex_map)
    return blackDead or whiteDead

def calculateValue(hex_map:HexMap,player):
    vlaue = CalculateBoardValue(hex_map,player)
    if(player=="W"):
        return vlaue
    else:
        return -vlaue

def minimax(hex_map:HexMap , depth , maximizingPlayer,player,hex_map_on_menu:HexMap):
    # if max depth was reached or game was over calculate the heuristics and return the value based on the player
    if GameOver(hex_map) or depth==0:
        return calculateValue(hex_map,player)
    else:
        moves = generateMoves(hex_map,player,hex_map_on_menu)
        if maximizingPlayer:
            bestValue = INTMIN
        else:
            bestValue = INTMAX
        for move in moves:
            if move[5] == "Beetle1" and move[6] == "W":
                print("ostor ya rb")
            applyMove(hex_map,hex_map_on_menu,move)
            value = minimax(hex_map,depth-1,not maximizingPlayer,player,hex_map_on_menu)
            if maximizingPlayer:
                bestValue = max(bestValue,value)
            else:
                bestValue = min(bestValue,value)
            if move[5] == "Beetle1" and move[6] == "W":
                print("ostor ya rb")
            undoMove(hex_map,hex_map_on_menu,move)
        return bestValue


def minimax_alpha_beta(hex_map: HexMap, depth, maximizingPlayer, player, alpha, beta,hex_map_on_menu:HexMap):
    # Base case: if max depth is reached or game is over, calculate the heuristic value for the player
    if GameOver(hex_map) or depth == 0:
        return calculateValue(hex_map, player)

    moves = generateMoves(hex_map, player,hex_map_on_menu)

    if maximizingPlayer:
        bestValue = alpha  # Start with alpha for maximizing player
    else:
        bestValue = beta  # Start with beta for minimizing player

    for move in moves:
        applyMove(hex_map, move)  # Apply the move
        value = minimax_alpha_beta(hex_map, depth - 1, not maximizingPlayer, player, alpha, beta,hex_map_on_menu)  # Recursive call
        undoMove(hex_map, move)  # Undo the move

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



def generateMoves (hex_map:HexMap , Player  ,hex_map_on_menu:HexMap):
    Result =[]
    for (key,value) in list( hex_map.map.items() ) :
        if Player == value[1] :
            print(value[0][:-1])
            for Pos in Pieces_Available_Positions[value[0][:-1]](hex_map ,key[0],key[1]) :
                Result.append( ("move",key[0],key[1],Pos[0],Pos[1] ,value[0] ,value[1] ,value[2]) )
    for (key,value) in hex_map_on_menu.map.items() :
        if Player == value[1] :
            for Pos in  AvailablePositions(hex_map,Player,value[0]):
                Result.append(("add",key[0],key[1],Pos[0],Pos[1] ,value[0] ,value[1] ,value[2]))

    # Result contains tuples of ("move" or "add",Current q , Current r , next q , next r , name, color )
    return  Result


def applyMove (hex_map:HexMap ,hex_map_on_menu:HexMap, move):
    if move[5] == "Beetle1" and move[6] == "W":
        print("ostor ya rb")
    if(move[0]=="move"):
        if move[5][:-1]=="Beetle" :
            hex_map.move_beetle(move[1],move[2],move[3],move[4])
        else:
            hex_map.move_piece(move[1],move[2],move[3],move[4])

    elif(move[0]=="add"):
        hex_map.add_piece(move[3],move[4],move[5],move[6],move[7])
        hex_map_on_menu.remove_piece(move[1],move[2])

def undoMove (hex_map:HexMap ,hex_map_on_menu:HexMap, move):
    if move[5] == "Beetle1" and move[6] == "W":
        print("ostor ya rb")
    # hex_map.move_piece(move[2], move[3], move[0], move[1])

    if(move[0]=="move"):
        if move[5][:-1] == "Beetle":
            hex_map.move_beetle(move[3], move[4], move[1], move[2])
        else:
            hex_map.move_piece(move[3],move[4],move[1],move[2])
    elif(move[0]=="add"):
        #  remove_piece(self, q, r):
        hex_map.remove_piece(move[3],move[4])
        hex_map_on_menu.add_piece(move[1],move[2],move[5],move[6],move[7])


def nextMove(hex_map,hex_map_on_menu:HexMap, depth, player):
    moves = generateMoves(hex_map, player,hex_map_on_menu)
    bestValue = INTMIN
    bestMove = []
    for move in moves:
        if move[5] == "Beetle1" and move[6]=="W":
            print("ostor ya rb")
        applyMove(hex_map, hex_map_on_menu,move)
        value = minimax(hex_map, depth - 1, False, player,hex_map_on_menu)
        if(value > bestValue or value == bestValue and random.choice([True,False])):
            bestValue = value
            bestMove = move
        if move[5] == "Beetle1" and move[6]=="W":
            print("ostor ya rb")
        undoMove(hex_map, hex_map_on_menu,move)

    return bestMove
