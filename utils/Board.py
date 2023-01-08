import threading

from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from utils.small_functions import piece_str_to_int, get_piece_by_char, char_to_int, piece_int_to_str, int_to_char, char_from_col
from utils.ChessPiece import ChessPiece
from utils.possible_moves import _get_possible_moves


class InputThread(threading.Thread):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def run(self):
        # Get user input
        user_input = input()

        # Emit the input as a signal
        self.signal.emit(user_input)

class ChessGUI(QMainWindow):
    def __init__(self, FEN:str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 00 00"):
        super().__init__()

        # setting up window
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('Chess')

        # playing  variable
        self.current_player_color = "white"
        self.possible_moves = []
        self.castling = "KQkq"
        self.current_piece = None
        self.full_moves = 0
        self.half_moves = 0

        self.board = [[ChessPiece(self, loc=[i, j]) for j in range(8)] for i in range(8)]
        # position fields and make background color
        for i, row in enumerate(self.board):
            for j, pos in enumerate(row):
                pos.setFixedSize(100, 100)
                pos.move(100 * j, 100 * i)
                if (i + j) % 2 == 0:
                    pos.setStyleSheet('background-color: white')
                else:
                    pos.setStyleSheet('background-color: darkgray')        
        # set pieces from FEN string
        self.load(FEN)

        # show GUI
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
                for i in range(0, int(char)):
                    self.board[row][col + i].piece = 0
                col += int(char)
            else:
                self.set_piece(get_piece_by_char(char.upper()), row, col, "black" if char.islower() else "white")
                col += 1
        self.current_player_color = "black" if FENfields[1] == "b" else "white"
        self.castling = FENfields[2]
        if FENfields[3] != "-":
            for i in range(0, len(FENfields[3]), 2):
                self.board[8-int(FENfields[3][i])][char_to_int(FENfields[3][i-1])].piece = 7
        self.half_moves = int(FENfields[4])
        self.full_moves = int(FENfields[5])

        # add moved attribute to rooks if neccesary
        for ch in self.castling:
            if ch == "K":
                self.board[7][7].moved = False
                self.board[7][7].rook_pos = "K"
            if ch == "Q":
                self.board[7][0].moved = False
                self.board[7][0].rook_pos = "Q"
            if ch == "k":
                self.board[0][7].moved = False
                self.board[0][7].rook_pos = "k"
            if ch == "q":
                self.board[0][0].moved = False
                self.board[0][0].rook_pos = "q"

    # Set the piece at the given row and column on the board
    def set_piece(self, piece, row, col, color):
        # Set the pixmap, color and piece type of field
        self.board[row][col].setPixmap(QPixmap(fr'c:/Users/felix/Programmieren/Python/Chess/config/chess_pieces/{color}_{piece}.png'))
        self.board[row][col].piece = piece_str_to_int(piece)
        self.board[row][col].color = color

    # reset all backgrounds and possible_moves to null
    def reset(self):
        self.possible_moves = []
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.board[i][j].setStyleSheet('background-color: white')
                else:
                    self.board[i][j].setStyleSheet('background-color: darkgray')
    
    # highlight possible moves with light green, the ones which capture a piece red
    def highlight_possible_moves(self):
        for i in self.possible_moves:
            if self.board[i[0]][i[1]].piece != 0 and self.board[i[0]][i[1]].piece != 7:
                self.board[i[0]][i[1]].setStyleSheet('background-color: red')
            else:
                self.board[i[0]][i[1]].setStyleSheet('background-color: lightgreen')
    
    # create layout with only type and color for faster processing
    def create_layout(self):
        return [[[piece.piece, piece.color] if piece.color is not None else [piece.piece] for piece in row] for row in self.board]

    def create_FEN_string(self):
        FEN = ""

        # getting FEN position part
        position_list = []
        position_string = ""
        for i in range(8):
            position_list.append("/")
            for j in range(8):
                position_list.append(int_to_char(self.board[i][j].piece).lower() if self.board[i][j].color == "black" else int_to_char(self.board[i][j].piece).upper())
        position_list.pop(0)
        counter = 0
        for i in position_list:
            if i != "":
                position_string = position_string + str(counter) + i
            else:
                counter+=1
            if i == "/":
                counter = 0
        FEN = position_string.replace("0", "")

        # whose colors turn is it
        FEN = FEN + " b" if self.current_player_color == "black" else FEN + " w"

        # castling
        FEN = FEN + " " + self.castling if self.castling != "" else FEN + " -"

        # en passant
        row = -1
        col = -1
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece == 7:
                    row = i
                    col = j
        FEN = FEN + " -" if row == -1 else FEN + " " + str(char_from_col(col) + str(8-row))

        # current half moves
        FEN = FEN + " 0" + str(self.half_moves) if self.half_moves < 10 else FEN + " " + str(self.half_moves)

        # current full moves
        FEN = FEN + " 0" + str(self.full_moves) if self.full_moves < 10 else FEN + " " + str(self.full_moves)

        return FEN


    def get_possible_moves(self, piece:ChessPiece, setvalue:bool=True):
        possible_moves = _get_possible_moves(self.create_layout(), piece, self.board)
        
        # castling
        if piece.piece == 6:
            castling = [False, False]
            for ch in self.castling:
                possible = True
                if ch == "K" and piece.color == "white":
                    for i in range(5, 7):
                        if self.board[7][i].piece != 0:
                            possible = False
                    castling[0] = possible
                if ch == "Q" and piece.color == "white":
                    for i in range(1, 4):
                        if self.board[7][i].piece != 0:
                            possible = False
                    castling[1] = possible    
                if ch =="k" and piece.color == "black":
                    for i in range(5, 7):
                        if self.board[0][i].piece != 0:
                            possible = False
                    castling[0] = possible
                if ch == "q" and piece.color == "black":
                    for i in range(1, 4):
                        if self.board[0][i].piece != 0:
                            possible = False
                    castling[1] = possible
            if castling[0]:
                possible_moves.append([0 if self.current_piece.color == "black" else 7, 6])
            if castling[1]:
                possible_moves.append([0 if self.current_piece.color == "black" else 7, 2])

        if setvalue:
            self.current_piece = piece
            self.possible_moves = possible_moves
        
        return possible_moves
        

    def move(self, piece):
        # preparing so not none
        convert = ""

        # full move +1
        if piece.color == "black":
            self.full_moves += 1
        # half mooves plus one (if reached 50 = draw)
        if piece.piece == "" or piece.piece is None and not (self.current_piece.piece == "pawn" and piece.loc[0] in [0, 7]):
            self.half_moves += 1
        else:
            self.half_moves = 0
        
        # replacing en passant with 8 to differ from last and current move
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece == 7:
                    self.board[i][j].piece = 8

        # special moves for pawn
        if self.current_piece.piece == 1:
            if self.current_piece.color == "white":
                direction = 1
            else:
                direction = -1
            if self.board[piece.loc[0]][piece.loc[1]].piece == 8:
                self.board[piece.loc[0]+direction][piece.loc[1]].piece = 0
                self.board[piece.loc[0]+direction][piece.loc[1]].color = None
                self.board[piece.loc[0]+direction][piece.loc[1]].setPixmap(QPixmap())
            elif abs(self.current_piece.loc[0] - piece.loc[0]) > 1:
                self.board[self.current_piece.loc[0] - direction][self.current_piece.loc[1]].piece = 7
            elif piece.loc[0] in [0, 7]:
                convert = QtWidgets.QInputDialog.getText(self, 'Input Dialog', "Please enter which piece you want to convert to ('knight', 'bishop', 'rook', 'queen'): ")[0]

        # special moves for king
        if self.current_piece.piece == 6:
            if abs(self.current_piece.loc[1]-piece.loc[1]) > 1:
                if piece.loc[1] == 2:
                    self.board[self.current_piece.loc[0]][0].piece = 0
                    self.board[self.current_piece.loc[0]][0].color = None
                    self.board[self.current_piece.loc[0]][0].setPixmap(QPixmap())
                    self.board[self.current_piece.loc[0]][3].piece = 4
                    self.board[self.current_piece.loc[0]][3].color = self.current_piece.color
                    self.board[self.current_piece.loc[0]][3].setPixmap(QPixmap(fr'c:/Users/felix/Programmieren/Python/Chess/config/chess_pieces/{self.current_piece.color}_rook.png'))
                elif piece.loc[1] == 6:
                    self.board[self.current_piece.loc[0]][7].piece = 0
                    self.board[self.current_piece.loc[0]][7].color = None
                    self.board[self.current_piece.loc[0]][7].setPixmap(QPixmap())
                    self.board[self.current_piece.loc[0]][5].piece = 4
                    self.board[self.current_piece.loc[0]][5].color = self.current_piece.color
                    self.board[self.current_piece.loc[0]][5].setPixmap(QPixmap(fr'c:/Users/felix/Programmieren/Python/Chess/config/chess_pieces/{self.current_piece.color}_rook.png'))

        # replace all previous en passants with 0 again
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece == 8:
                    self.board[i][j].piece = 0

        # set image of current piece to null
        self.current_piece.setPixmap(QPixmap())
        # set piece type, color and image of new field
        piece.piece = self.current_piece.piece if convert == "" else piece_str_to_int(convert)
        piece.color = self.current_piece.color
        piece.setPixmap(QPixmap(fr'c:/Users/felix/Programmieren/Python/Chess/config/chess_pieces/{piece.color}_{piece_int_to_str(piece.piece)}.png'))
        self.current_piece.piece = 0
        self.current_piece.color = None
        self.current_piece = None
        self.reset()

        # remove castling rights
        if piece.piece == 6:
            self.castling = ''.join(ch for ch in self.castling if not (ch.isupper() if piece.color == "white" else ch.islower()))
        if piece.piece == 4:
            if not piece.moved:
                self.castling.replace(piece.rook_pos, "")
                piece.moved = True
        
        finished = self.is_finished()
        if finished[0]:
            print(finished[1])
            quit()
        self.current_player_color = "black" if self.current_player_color == "white" else "white"

    
    def is_finished(self):
        if self.half_moves > 49:
            return [True, "Draw, 50 half moves"]
        
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].color != self.current_player_color:
                    for move in self.get_possible_moves(self.board[i][j]):
                        possible_moves.append(move)

        if possible_moves == []:
            if not is_currently_checked(self, "black" if self.current_player_color == "white" else "white"):
                return [True, "Draw, no moves possible"]
            else:
                return [True, self.current_player_color + " WINS!"]

        return [False]

    
    def is_currently_checked(self, color):
        row = 0
        col = 0
        
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece == 6 and self.board[i][j].color == color:
                    row = i
                    col = j
                    break

        for i in range(8):
            for j in range(8):
                location = self.board[i][j]
                if location.piecce != 0 and location.piece != 7 and location.color != color:
                    moves = _get_possible_moves(self.create_layout(), self.board[i][j], self.board, False)
                    if [row, col] in moves:
                        return True
        
        return False