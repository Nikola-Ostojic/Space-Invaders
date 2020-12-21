from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from entities.Player import Player
from entities.Enemy import Enemy
from PyQt5.QtGui import QPixmap

from PyQt5 import QtGui

WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720

class Window(QWidget):
    
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)     

        self.setWindowTitle('Space Invaders')
        self.window_width = WINDOW_WIDTH
        self.window_heigth = WINDOW_HEIGTH       
        self.setGeometry(100, 100, self.window_width, self.window_heigth)

        self.set_background()

        lbl1 = Player(self)
        lbl1.move(520, 600)
        lbl1.setFocus()

        labele = []
        labele.append(Enemy(self))
        labele[0].move(100, 100)

        for i in range(1, 33):
            labele.append(Enemy(self))
            if i % 11 == 0:
                labele[i].move(labele[0].x(), labele[i].y() + 100)
            labele[i].move(labele[i - 1].x() + 100, labele[i - 1].y())

        

    def set_background(self):
        background = QImage('assets/background.png')
        background = background.scaled(WINDOW_WIDTH, WINDOW_HEIGTH)
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(pallete)

