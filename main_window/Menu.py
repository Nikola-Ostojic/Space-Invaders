from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
class Menu(QWidget):

    playSignal = pyqtSignal()
    quitGameSignal = pyqtSignal()

    def __init__(self):
        super(Menu, self).__init__()

        play_button = QPushButton("Single player", self)
        play_button.setFixedWidth(100)
        play_button.setFixedHeight(70)
        play_button.move(0,0)
        play_button.clicked.connect(self.play)



        quit_button = QPushButton("Quit", self)
        quit_button.setFixedWidth(100)
        quit_button.setFixedHeight(70)
        quit_button.move(102,0)
        quit_button.clicked.connect(self.quit)
        print('prikazujem klasu Menu')


        self.show()

    def play(self):
        self.playSignal.emit()

    def quit(self):
        self.quitGameSignal.emit()