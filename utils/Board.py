from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel

from utils.small_functions import piece_str_to_int, knight_jumps_clockwise
from utils.ChessPiece import ChessPiece

import threading, copy


class InputThread(threading.Thread):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def run(self):
        # Get user input
        user_input = input()

        # Emit the input as a signal
        self.signal.emit(user_input)



# Create a class for the main window of the GUI
class ChessGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = [[[0] for _ in range(8)] for _ in range(8)]

        # Set the window properties
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('Chess')

        # variable to determine whose players turn it is
        self.current_player_color = "white"
        self.possible_moves = []
        self.current_piece = None

        # Create a 8x8 grid of labels to hold the chess pieces
        self.grid = [[ChessPiece(self) for _ in range(8)] for _ in range(8)]
        self.overlay = [[QLabel(self) for _ in range(8)] for _ in range(8)]

        # Set the background color and size of the labels
        for row in self.grid:
            for label in row:
                label.setStyleSheet('background-color: white')
                label.setFixedSize(100, 100)

        # Set the positions of the labels in the grid
        for i in range(8):
            for j in range(8):
                self.grid[i][j].move(100 * j, 100 * i)
                self.grid[i][j].loc = [i, j]
                self.overlay[i][j].move(100 * j, 100 * i)
                if (i + j) % 2 == 0:
                    self.grid[i][j].setStyleSheet('background-color: white')
                else:
                    self.grid[i][j].setStyleSheet('background-color: darkgray')

        # Set the initial positions of the chess pieces on the board
        self.set_piece('rook', 0, 0, 'black')
        self.set_piece('knight', 0, 1, 'black')
        self.set_piece('bishop', 0, 2, 'black')
        self.set_piece('queen', 0, 3, 'black')
        self.set_piece('king', 0, 4, 'black')
        self.set_piece('bishop', 0, 5, 'black')
        self.set_piece('knight', 0, 6, 'black')
        self.set_piece('rook', 0, 7, 'black')
        for i in range(8):
            self.set_piece('pawn', 1, i, 'black')
        for i in range(8):
            self.set_piece('pawn', 6, i, 'white')
        self.set_piece('rook', 7, 0, 'white')
        self.set_piece('knight', 7, 1, 'white')
        self.set_piece('bishop', 7, 2, 'white')
        self.set_piece('queen', 7, 3, 'white')
        self.set_piece('king', 7, 4, 'white')
        self.set_piece('bishop', 7, 5, 'white')
        self.set_piece('knight', 7, 6, 'white')
        self.set_piece('rook', 7, 7, 'white')

        # Show the window
        self.show()

    # Set the piece at the given row and column on the board
    def set_piece(self, piece, row, col, color):
        
        # Set the pixmap and background color of the label
        self.grid[row][col].setPixmap(QPixmap(fr'c:/Users/felix/Programmieren/Python/Chess/config/chess_pieces/{color}_{piece}.png'))
        self.grid[row][col].piece = piece
        self.grid[row][col].color = color
        if (row + col) % 2 == 0:
            self.grid[row][col].setStyleSheet('background-color: white')
        else:
            self.grid[row][col].setStyleSheet('background-color: darkgray')
        self.layout[row][col] = [piece_str_to_int(piece), color]
    
    def reset(self):
        self.possible_moves = []
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.grid[i][j].setStyleSheet('background-color: white')
                else:
                    self.grid[i][j].setStyleSheet('background-color: darkgray')
    
    def get_possible_moves(self, piece):
        self.possible_moves = _get_possible_moves(self.layout, piece, self.grid)
        self.current_piece = piece
    
    def highlight_possible_moves(self, color):
        return
    
    def move(self, piece):# wenn zweimal nach vorne gegangen wird im layout bei der übersprungenen stelle 7 einfügen und nächsten move wieder rauslöschen für en passant
        convert = ""
        for i in range(8):
            for j in range(8):
                if self.layout[i][j][0] == 7:
                    self.layout[i][j][0] = 8
        self.layout[self.current_piece.loc[0]][self.current_piece.loc[1]] = [0]
        if self.current_piece.piece == "pawn":
            if self.current_piece.color == "white":
                if self.layout[piece.loc[0]][piece.loc[1]][0] == 8:
                    self.layout[piece.loc[0]+1][piece.loc[1]] = [0]
                    self.grid[piece.loc[0]+1][piece.loc[1]].piece = None
                    self.grid[piece.loc[0]+1][piece.loc[1]].color = None
                    self.grid[piece.loc[0]+1][piece.loc[1]].setPixmap(QPixmap())
                elif self.current_piece.loc[0] - piece.loc[0] > 1:
                    self.layout[self.current_piece.loc[0]-1][self.current_piece.loc[1]] = [7]
                elif piece.loc[0] == 0:
                    convert = QtWidgets.QInputDialog.getText(self, 'Input Dialog', "Please enter which piece you want to convert to ('knight', 'bishop', 'rook', 'queen'): ")[0]
            else:
                if self.layout[piece.loc[0]][piece.loc[1]][0] == 7:
                    self.layout[piece.loc[0]-1][piece.loc[1]] = [0]
                    self.grid[piece.loc[0]-1][piece.loc[1]].piece = None
                    self.grid[piece.loc[0]-1][piece.loc[1]].color = None
                    self.grid[piece.loc[0]-1][piece.loc[1]].setPixmap(QPixmap())
                elif piece.loc[0] - self.current_piece.loc[0] > 1:
                    self.layout[piece.loc[0] - 1][piece.loc[1]] = [7]
                elif piece.loc[0] == 7:
                    convert = input("Please enter which piece you want to convert to ('knight', 'bishop', 'rook', 'queen'): ")
        for i in range(8):
            for j in range(8):
                if self.layout[i][j][0] == 8:
                    self.layout[i][j][0] = 0
        self.current_piece.setPixmap(QPixmap())
        piece.piece = self.current_piece.piece if convert == "" else convert
        piece.color = self.current_piece.color
        piece.setPixmap(QPixmap(fr'c:/Users/felix/Programmieren/Python/Chess/config/chess_pieces/{piece.color}_{piece.piece}.png'))
        self.layout[piece.loc[0]][piece.loc[1]] = [piece_str_to_int(piece.piece), piece.color]
        self.current_piece.piece = None
        self.current_piece.color = None
        self.current_piece = None
        self.reset()
        if self.is_checkmate():
            print("Winner: " + self.current_player_color)
        self.current_player_color = "black" if self.current_player_color == "white" else "white"
    
    def is_checkmate(self):
        return False

def _get_possible_moves(layout, piece, grid, is_check_check:bool=True):
    possible_moves = []

    layout_copy = copy.deepcopy(layout)

    if piece.piece == "pawn":
        possible_moves = possible_moves_pawn(layout_copy, piece.loc, piece.color)
    if piece.piece == "knight":
        possible_moves = possible_moves_knight(layout_copy, piece.loc, piece.color)
    if piece.piece == "bishop":
        possible_moves = possible_moves_bishop(layout_copy, piece.loc, piece.color)
    if piece.piece == "rook":
        possible_moves = possible_moves_rook(layout_copy, piece.loc, piece.color)
    if piece.piece == "queen":
        possible_moves = possible_moves_queen(layout_copy, piece.loc, piece.color)
    if piece.piece == "king":
        possible_moves = possible_moves_king(layout_copy, piece.loc, piece.color)

    if is_check_check:
        for i in possible_moves:
            if is_check(layout_copy, piece, i, grid):
                print("check found: ")
                possible_moves.pop(possible_moves.index(i))
    
        print(str(possible_moves) + "\n\n\n")
    return possible_moves

def is_check(layout, piece, loc, grid):
    layout[piece.loc[0]][piece.loc[1]] = [0]
    layout[loc[0]][loc[1]] = [piece_str_to_int(piece.piece), piece.color]
    
    row = 0
    col = 0
    
    for i in range(8):
        for j in range(8):
            if layout[i][j][0] == 6 and layout[i][j][1] == piece.color:
                row = i
                col = 0
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
        else:
            if layout[r][c][1] != color:
                # The piece is an enemy, so it is a possible move
                possible_moves.append([r, c])
    
    # Check if the pawn can move two spaces forward on its first move
    if (color == 'white' and loc[0] == 6) or (color == 'black' and loc[0] == 1):
        # The pawn is on its starting row, so it can move two spaces forward
        r = loc[0] + direction*2
        c = loc[1]
        if layout[r][c][0] == 0:
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
    row = loc[0]
    col = loc[1]
    
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

    row = loc[0]
    col = loc[1]
    
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
            if layout[r][col][0] != 0 and layout[row][c][0] != 7:
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
            print(layout)
            if layout[r][col][0] != 0 and layout[row][c][0] != 7:
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
    moves = []

    row = loc[0]
    col = loc[1]

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= row + i < 8 and 0 <= col + j < 8:
                piece = layout[row + i][col + j]
                if piece[0] == 0 or piece[0] == 7:
                    moves.append([row + i, col + j])
                elif piece[1] != color:
                    moves.append([row + i, col + j])
    return moves

