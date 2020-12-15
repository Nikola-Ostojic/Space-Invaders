import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5 import QtCore, QtWidgets
from Player import Player

WINDOW_WIDTH = 600
WINDOW_HEIGTH = 800


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Space Invaders')
        self.window_width = WINDOW_WIDTH
        self.window_heigth = WINDOW_HEIGTH
        self.setGeometry(100, 100, self.window_width, self.window_heigth)
        centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(centralwidget)
        layout = QtWidgets.QHBoxLayout(centralwidget)
        self.player = Player()

        layout.addWidget(self.player)
        self.player.setFocus()

        background = QImage('assets/background.png')
        background = background.scaled(WINDOW_WIDTH, WINDOW_HEIGTH)
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(pallete)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())