from Utilities import get_neighbors
def FreedomToMove(hex_map,Empty_Neighbours, AvailablePOSs):
    s = set() 
    directions = [(+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1)]
    for AvailablePOS in AvailablePOSs :
        Empty_Neighbours_ForAvailablePOS =[]
        for  direction in directions:
            Empty_Neighbours_ForAvailablePOS.append((AvailablePOS[0]+direction[0] , AvailablePOS[1]+direction[1]) )
        for Empty_Neighbour_ForAvailablePOS in Empty_Neighbours_ForAvailablePOS :
            flag =0 
            for Empty_Neighbour in Empty_Neighbours :
                if Empty_Neighbour[0] == Empty_Neighbour_ForAvailablePOS[0] and  Empty_Neighbour[1] == Empty_Neighbour_ForAvailablePOS[1] :
                    s.add( AvailablePOS) 
                    flag=1 
                    break 

            if flag ==1 :
                break 


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
    #print(neighbors)
    if len(neighbors) < 2:
        # Hive cannot break if the piece has less than 2 neighbors
        return False
    # if removed_piece not in grid.keys():
    #     # The piece to be removed is not in the grid
    #     return False
    piece = grid[removed_piece]
    # Step 2: Temporarily remove the piece from the grid
    del grid[removed_piece]  #del the selected piece from the hex map

    # Step 3: Start DFS from one neighbor
    start = neighbors[0]
    visited = set()
    dfs(grid, start, visited)

    # Step 4: Check if all other neighbors are reachable
    for neighbor in neighbors[1:]:
        if neighbor not in visited:
            # Not all neighbors are connected; hive is broken
            grid[removed_piece] = piece  # Restore the piece hexmap.map[select]
            return True

    # Step 5: Restore the removed piece and return the result
    grid[removed_piece] = piece
    return False
