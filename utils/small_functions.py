pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']

def piece_str_to_int(piece:str):
    return pieces.index(piece.lower())+1

def piece_int_to_str(piece:int):
    return pieces[piece]

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
