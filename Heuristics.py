from Hex_map import HexMap
from Available_positions import *
from Utilities import *
Pieces_Available_Positions={
    "Queen" : Available_Positions_Queen ,
    "Ant"   : AvailablePositions_SoldierAnt ,
    "GrassHopper" : AvailablePositions_GrassHopper ,
    "Beetle"      : AvailablePositions_Beetle ,
    "Spider"      : Available_Positions_Spider
}




def FreePieces (hex_map : HexMap,color):
    cnt=0
    for (key,value) in hex_map.map.items() :
        if color == value[1] :
            if len(Pieces_Available_Positions[value[0]](hex_map ,key[0],key[1])) >0 :
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

    NonEmptyNeighbours_WQ = hex_map.get_neighbors(whiteQueen[0][0],whiteQueen[0][1])
    BlackHexesAround_WQ =[]
    for Neighbour in NonEmptyNeighbours_WQ:
        if hex_map.get_piece(Neighbour[0],Neighbour[1])[1]=="B" :
            BlackHexesAround_WQ.append(Neighbour)

    NonEmptyNeighbours_BQ = hex_map.get_neighbors(blackQueen[0][0], blackQueen[0][1])
    whiteHexesAround_BQ = []
    for Neighbour in NonEmptyNeighbours_BQ:
        if hex_map.get_piece(Neighbour[0], Neighbour[1])[1] == "W":
            whiteHexesAround_BQ.append(Neighbour)

    numberOfWhiteFreePieces= FreePieces(hex_map,"W")
    numberOfBlackFreePieces= FreePieces(hex_map,"B")

    return 20*(len(whiteHexesAround_BQ) - len(BlackHexesAround_WQ))+ 1*(hex_map.White_turn_count -hex_map.Black_turn_count)+ 5*(numberOfWhiteFreePieces - numberOfBlackFreePieces) ;


