pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']

def piece_str_to_int(piece:str):
    return pieces.index(piece.lower())+1

def piece_int_to_str(piece:int):
    return pieces[piece-1]

def knight_jumps_clockwise(num_of_eight:int):
    if num_of_eight == 0:
        return [2, 1]
    elif num_of_eight == 1:
        return [1, 2]
    elif num_of_eight == 2:
        return [-1, 2]
    elif num_of_eight == 3:
        return [-2, 1]
    elif num_of_eight == 4:
        return [-2, -1]
    elif num_of_eight == 5:
        return [-1, -2]
    elif num_of_eight == 6:
        return [1, -2]
    elif num_of_eight == 7:
        return [2, -1]

def get_piece_by_char(piece:str):
    if piece == "P":
        return "pawn"
    elif piece == "N":
        return "knight"
    elif piece == "B":
        return "bishop"
    elif piece == "R":
        return "rook"
    elif piece == "Q":
        return "queen"
    elif piece == "K":
        return "king"

def char_to_int(char):
    if char == "a":
        return 0
    elif char == "b":
        return 1
    elif char == "c":
        return 2
    elif char == "d":
        return 3
    elif char == "e":
        return 4
    elif char == "f":
        return 5
    elif char == "g":
        return 6
    else:
        return 7

def int_to_char(num):
    return "" if num in [0, 7] else pieces[num-1][0].lower() if not num == 2 else "n"

def char_from_col(col):
    if col == 0:
        return "a"
    elif col == 1:
        return "b"
    elif col == 2:
        return "c"
    elif col == 3:
        return "d"
    elif col == 4:
        return "e"
    elif col == 5:
        return "f"
    elif col == 6:
        return "h"
    else:
        return "g"