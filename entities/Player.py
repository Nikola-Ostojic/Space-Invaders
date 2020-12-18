from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget

WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720

class Player(QtWidgets.QLabel):
    def __init__(self, parent = QWidget):
        super().__init__(parent)
        self.setPixmap(QPixmap('assets/ship.png').scaled(50, 50))
       

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_A:
            if (self.x() > 1):
                self.move(self.x() - 10, self.y())
        elif event.key() == QtCore.Qt.Key_D:
            if (self.x() + 50 < WINDOW_WIDTH):
                self.move(self.x() + 10, self.y())
        elif event.key() == QtCore.Qt.Key_W:
            if (self.y() - 50 > 0):
                self.move(self.x(), self.y() - 10)
        elif event.key() == QtCore.Qt.Key_S:
            if (self.y() + 50  < WINDOW_HEIGTH):
                self.move(self.x(), self.y() + 10)
        else:
            QtWidgets.QLabel.keyPressEvent(self, event)