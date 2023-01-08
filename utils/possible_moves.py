import copy

from utils.small_functions import knight_jumps_clockwise, piece_int_to_str

def is_check(layout, piece, loc, grid):
    layout[piece.loc[0]][piece.loc[1]] = [0]
    layout[loc[0]][loc[1]] = [piece.piece, piece.color]

    row = 0
    col = 0
    
    for i in range(8):
        for j in range(8):
            if layout[i][j][0] == 6 and layout[i][j][1] == piece.color:
                row = i
                col = j
                break

    # Check if any enemy pieces can attack the king
    for i in range(8):
        for j in range(8):
            location = layout[i][j]
            if location[0] != 0 and location[0] != 7 and location[1] != piece.color:
                moves = _get_possible_moves(layout, grid[i][j], grid, False)
                if [row, col] in moves:
                    return True

    # If no enemy pieces can attack the king, return False
    return False


def _get_possible_moves(layout, piece, grid, is_check_check:bool=True):
    possible_moves = []
    if is_check_check:
        print(piece_int_to_str(piece.piece))
        print(layout)
    if piece.piece == 1:
        possible_moves = possible_moves_pawn(layout, piece.loc, piece.color)
    if piece.piece == 2:
        possible_moves = possible_moves_knight(layout, piece.loc, piece.color)
    if piece.piece == 3:
        possible_moves = possible_moves_bishop(layout, piece.loc, piece.color)
    if piece.piece == 4:
        possible_moves = possible_moves_rook(layout, piece.loc, piece.color)
    if piece.piece == 5:
        possible_moves = possible_moves_queen(layout, piece.loc, piece.color)
    if piece.piece == 6:
        possible_moves = possible_moves_king(layout, piece.loc, piece.color)
    if is_check_check:
        print(possible_moves)
        for i in copy.deepcopy(possible_moves):
            if is_check(layout, piece, i, grid):
                possible_moves.pop(possible_moves.index(i))
        print(possible_moves)
    return possible_moves


def possible_moves_pawn(layout, loc, color):
    possible_moves = []
    
    # Determine the direction that the pawn is moving based on its color
    if color == 'white':
        direction = -1
    else:
        direction = 1

    # Check the space directly in front of the pawn
    r = loc[0] + direction
    c = loc[1]
    if r >= 0 and r < 8 and c >= 0 and c < 8:
        # The space is within the boundaries of the board
        if layout[r][c][0] == 0:
            # The space is empty, so it is a possible move
            possible_moves.append([r, c])
    
    # Check if the pawn can move two spaces forward on its first move
    if (color == 'white' and loc[0] == 6) or (color == 'black' and loc[0] == 1):
        # The pawn is on its starting row, so it can move two spaces forward
        r = loc[0] + direction*2
        c = loc[1]
        if layout[r][c][0] == 0 and len(possible_moves) > 0:
            # The space is empty, so it is a possible move
            possible_moves.append([r, c])
    
    # Check if the pawn can capture an enemy piece on the diagonal
    for dc in [-1, 1]:
        r = loc[0] + direction
        c = loc[1] + dc
        if r >= 0 and r < 8 and c >= 0 and c < 8:
            # The space is within the boundaries of the board
            if layout[r][c][0] != 0:
                if layout[r][c][0] == 7:
                    # The piece is en passant, so it is a possible move
                    possible_moves.append([r, c])
                elif layout[r][c][1] != color:
                    # The piece is an enemy, so it is a possible move
                    possible_moves.append([r, c])
    
    return possible_moves

def possible_moves_knight(layout, loc, color):
    possible_moves = []
    
    # Check the eight spaces that a knight can jump to
    for i in range(8):
        jump = knight_jumps_clockwise(i)
        r = loc[0] + jump[0]
        c = loc[1] + jump[1]
        if r >= 0 and r < 8 and c >= 0 and c < 8:
            # The jump is within the board
            if layout[r][c][0] == 0 or layout[r][c][0] == 7:
                # The space is empty, so it is a possible move
                possible_moves.append([r, c])
            else:
                if layout[r][c][1] != color:
                    # The piece is an enemy, so it is a possible move
                    possible_moves.append([r, c])
    return possible_moves

def possible_moves_bishop(layout, loc, color):
    # Initialize an empty list for the possible moves
    possible_moves = []
    
    # Get the current row and column of the bishop
    row, col = loc
    
    # Check the top-left diagonal
    i = row - 1
    j = col - 1
    while i >= 0 and j >= 0:
        if layout[i][j][0] == 0 or layout[i][j][0] == 7:
            # The space is empty, so it is a possible move
            possible_moves.append([i, j])
        else:
            if layout[i][j][1] != color:
                # The piece is an enemy, so it is a possible move
                possible_moves.append([i, j])
            # In any other case, we cannot move to this space
            break
        i -= 1
        j -= 1
    
    # Check the top-right diagonal
    i = row - 1
    j = col + 1
    while i >= 0 and j < 8:
        if layout[i][j][0] == 0 or layout[i][j][0] == 7:
            # The space is empty, so it is a possible move
            possible_moves.append([i, j])
        else:
            if layout[i][j][1] != color:
                # The piece is an enemy, so it is a possible move
                possible_moves.append([i, j])
            # In any other case, we cannot move to this space
            break
        i -= 1
        j += 1
    
    # Check the bottom-left diagonal
    i = row + 1
    j = col - 1
    while i < 8 and j >= 0:
        if layout[i][j][0] == 0 or layout[i][j][0] == 7:
            # The space is empty, so it is a possible move
            possible_moves.append([i, j])
        else:
            if layout[i][j][1] != color:
                # The piece is an enemy, so it is a possible move
                possible_moves.append([i, j])
            # In any other case, we cannot move to this space
            break
        i += 1
        j -= 1
    
    # Check the bottom-right diagonal
    i = row + 1
    j = col + 1
    while i < 8 and j < 8:
        if layout[i][j][0] == 0 or layout[i][j][0] == 7:
            # The space is empty, so it is a possible move
            possible_moves.append([i, j])
        else:
            if layout[i][j][1] != color:
                # The piece is an enemy, so it is a possible move
                possible_moves.append([i, j])
            # In any other case, we cannot move to this space
            break
        i += 1
        j += 1
    
    return possible_moves

def possible_moves_rook(layout, loc, color):
    possible_moves = []

    row, col = loc
    
    # Check the spaces in the same row to the right
    for c in range(col+1, 8):
        # Check if the space is within the boundaries of the board
        if c >= 0 and c < 8:
            if layout[row][c][0] != 0 and layout[row][c][0] != 7:
                if layout[row][c][1] != color:
                    # The piece is an enemy, so it is a possible move
                    possible_moves.append([row, c])
                # The piece is not an enemy, so we can't move any further in this direction
                break
            else:
                # The space is not occupied, so it is a possible move
                possible_moves.append([row, c])
    
    # Check the spaces in the same row to the left
    for c in range(col-1, -1, -1):
        # Check if the space is within the boundaries of the board
        if c >= 0 and c < 8:
            if layout[row][c][0] != 0 and layout[row][c][0] != 7:
                if layout[row][c][1] != color:
                    # The piece is an enemy, so it is a possible move
                    possible_moves.append([row, c])
                # The piece is not an enemy, so we can't move any further in this direction
                break
            else:
                # The space is not occupied, so it is a possible move
                possible_moves.append([row, c])
    
    # Check the spaces in the same column above
    for r in range(row-1, -1, -1):
        # Check if the space is within the boundaries of the board
        if r >= 0 and r < 8:
            if layout[r][col][0] != 0 and layout[r][col][0] != 7:
                if layout[r][col][1] != color:
                    # The piece is an enemy, so it is a possible move
                    possible_moves.append([r, col])
            # The piece is not an enemy, so we can't move any further in this direction
            break
        else:
            # The space is not occupied, so it is a possible move
            possible_moves.append([r, col])
    
    # Check the spaces in the same column below
    for r in range(row+1, 8):
        # Check if the space is within the boundaries of the board
        if r >= 0 and r < 8:
            if layout[r][col][0] != 0 and layout[r][col][0] != 7:
                if layout[r][col][1] != color:
                    # The piece is an enemy, so it is a possible move
                    possible_moves.append([r, col])
                # The piece is not an enemy, so we can't move any further in this direction
                break
            else:
                # The space is not occupied, so it is a possible move
                possible_moves.append([r, col])
    return possible_moves

def possible_moves_queen(layout, loc, color):
    # The queen's possible moves are the combination of the possible moves of the rook and bishop
    possible_moves = possible_moves_rook(layout, loc, color) + possible_moves_bishop(layout, loc, color)
    return possible_moves

def possible_moves_king(layout, loc, color):
    possible_moves = []

    row, col = loc

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= row + i < 8 and 0 <= col + j < 8:
                piece = layout[row + i][col + j]
                if piece[0] == 0 or piece[0] == 7:
                    possible_moves.append([row + i, col + j])
                elif piece[1] != color:
                    possible_moves.append([row + i, col + j])
    return possible_moves
