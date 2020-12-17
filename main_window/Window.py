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

        # centralW = QtWidgets.QWidget()
        # self.setCentralWidget(centralW)       

        # self.player = Player()       
        
        # layout = QtWidgets.QVBoxLayout(centralW)
        # layout.addWidget(self.player)
        # self.player.setFocus()       

        # self.setLayout(layout)
        

        # self.addWidget(self.player)
        # self.player.setFocus()
        # self.player.move(300, 0)

        # for i in range(5):
        #     self.addWidget(Enemy())

        # self.set_layout(centralW)

        lbl1 = Player(self)
        # lbl1.setPixmap(QPixmap('assets/ship.png').scaled(50, 50))
        lbl1.move(220, 600)
        lbl1.setFocus()

        

   

    def set_background(self):
        background = QImage('assets/background.png')
        background = background.scaled(WINDOW_WIDTH, WINDOW_HEIGTH)
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(pallete)

