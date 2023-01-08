from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel

from utils.small_functions import piece_str_to_int, knight_jumps_clockwise, get_piece_by_char, char_to_int
from utils.ChessPiece import ChessPiece
from utils.possible_moves import possible_moves_bishop, possible_moves_king, possible_moves_knight, possible_moves_pawn, possible_moves_queen, possible_moves_rook

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
    def __init__(self, FEN:str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"):
        super().__init__()
        self.layout = [[[0] for _ in range(8)] for _ in range(8)]

        # Set the window properties
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('Chess')

        # variable to determine whose players turn it is
        self.current_player_color = "white"
        self.possible_moves = []
        self.castling = "KQkq"
        self.current_piece = None
        self.full_moves = 0
        self.half_moves = 0

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

        self.load(FEN)

        # Show the window
        self.show()

    def load(self, FEN:str):
        row = 0
        col = 0
        FENfields = FEN.split(" ")
        for char in FENfields[0]:
            if char == "/":
                row += 1
                col = 0
            elif char.isdigit():
                col += int(char)
            else:
                self.set_piece(get_piece_by_char(char.upper()), row, col, "black" if char.islower() else "white")
                col += 1
        self.current_player_color = "black" if FENfields[1] == "b" else "white"
        self.castling = FENfields[2]
        if FENfields[3] != "-":
            for i in range(0, len(FENfields[3]), 2):
                self.layout[8-int(FENfields[3][i])][char_to_int(FENfields[3][i-1])] = [7]
        self.half_moves = int(FENfields[4])
        self.full_moves = int(FENfields[5])


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
    
    def highlight_possible_moves(self):
        print(self.layout)
        for i in self.possible_moves:
            if self.layout[i[0]][i[1]][0] != 0 and self.layout[i[0]][i[1]][0] != 7:
                self.grid[i[0]][i[1]].setStyleSheet('background-color: red')
            else:
                self.grid[i[0]][i[1]].setStyleSheet('background-color: lightgreen')
    
    def move(self, piece):# wenn zweimal nach vorne gegangen wird im layout bei der übersprungenen stelle 7 einfügen und nächsten move wieder rauslöschen für en passant
        convert = ""
        if piece.color == "black":
            self.full_moves += 1
        if piece.piece == "" or piece.piece is None and not (self.current_piece.piece == "pawn" and piece.loc[0] in [0, 7]):
            self.half_moves += 1
        else:
            self.half_moves = 0
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
                if self.layout[piece.loc[0]][piece.loc[1]][0] == 8:
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
        finished = self.is_checkmate()
        if finished[0]:
            print(finished[1])
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
