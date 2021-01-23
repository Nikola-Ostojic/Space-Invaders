import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

from main_window.Window import Window
from main_window.Menu import Menu

# Menu settings




class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = None
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainMenu = Menu()
        print('Pozvan konstruktor menu')
        self.menu()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setObjectName("Space Invaders")
        self.setFixedSize(336, 440)

        self.setWindowIcon(QtGui.QIcon('./assets/logo.png'))
        self.setWindowIconText("Space Invaders")


    def menu(self):
        self.mainMenu.playSignal.connect(self.playGame)
        self.mainMenu.quitGameSignal.connect(self.quit)
        self.centralWidget.addWidget(self.mainMenu)
        self.centralWidget.setCurrentWidget(self.mainMenu)





    def quit(self):
        sys.exit()

    def playGame(self):
        self.hide()
        print("Igra zapoceta, main menu hide-ovan")
        self.game = Window()
