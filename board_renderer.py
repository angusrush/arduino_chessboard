import chess
import chess.svg
import sys
import time

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

class BoardWindow(QMainWindow):
    def __init__(self, board):
        super(BoardWindow, self).__init__()

        self.setGeometry(50, 50, 550, 550)

        self.widgetSvg = QSvgWidget(parent = self)
        self.widgetSvg.setGeometry(5, 5, 540, 540)

        self.chessboard = board

        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def paintEvent(self, event):
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = chess.Board()
    w = BoardWindow(board)
    w.show()
    sys.exit(app.exec_())

