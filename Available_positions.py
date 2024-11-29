from rules import *
import copy

def AvailablePositions(hex_map, turn):
    result = []
    s = set()
    if turn == "W":
        if hex_map.Length == 0:
            return [(0,0,None)] #was return TRUE
        elif hex_map.Length ==1 :
            keys = list(hex_map.map.keys())
            return  hex_map.get_Empty_neighbors(keys[0][0],keys[0][1] )
        else:
            keys = list(hex_map.map.keys())
            List = []
            for key in keys:
                List += hex_map.get_Empty_neighbors(key[0], key[1])
                for element in List:
                    s.add((element[0], element[1],element[2]))

            for element in s:
                flag = 0
                for element2 in List:
                    if (element[0] == element2[0]) and (element[1] == element2[1]) and element2[2] == "B":
                        flag = 1
                if flag == 0:
                    result.append((element[0], element[1],element[2]))

    if turn == "B":
        if hex_map.Length == 0:
            return [(0,0,None)] #was return TRUE
        elif hex_map.Length == 1:
            keys = list(hex_map.map.keys())
            return hex_map.get_Empty_neighbors(keys[0][0], keys[0][1])
        else:
            keys = list(hex_map.map.keys())
            List = []
            for key in keys:
                List += hex_map.get_Empty_neighbors(key[0], key[1])
                for element in List:
                    s.add((element[0], element[1],element[2]))

            for element in s:
                flag = 0
                for element2 in List:
                    if (element[0] == element2[0]) and (element[1] == element2[1]) and (element2[2] == "W"):
                        flag = 1
                if flag == 0:
                    result.append((element[0], element[1],element[2]))

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

