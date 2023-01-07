from PyQt5.QtWidgets import QLabel

class ChessPiece(QLabel):
    def __init__(self, parent, piece:str=None, loc:list=None, color:str=None) -> None:
        super().__init__(parent=parent)
        self.window = parent
        self.piece = piece
        self.loc = loc
        self.color = color
    
    def mousePressEvent(self, event):
        # Do something when the label is clicked
        if not self.loc in self.window.possible_moves:
            self.window.reset()
            if self.piece is not None and self.color == self.window.current_player_color:
                self.window.get_possible_moves(self)
                self.setStyleSheet('background-color: darkgreen')
                self.window.highlight_possible_moves(self.window.current_piece.color)
        else:
            self.window.move(self)
            

