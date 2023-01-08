import sys
from PyQt5.QtWidgets import QApplication

from utils import Board

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = Board()
    sys.exit(app.exec_())
    