from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtWidgets

WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720

class Enemy(QtWidgets.QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setPixmap(QPixmap('assets/enemy.png').scaled(100, 100))

    # def keyPressEvent(self, event):

    #     if event.key() == QtCore.Qt.Key_A:
    #         if (self.x() > 1):
    #             self.move(self.x() - 10, self.y())
    #     elif event.key() == QtCore.Qt.Key_D:
    #         if (self.x() + 50 < WINDOW_WIDTH):
    #             self.move(self.x() + 10, self.y())
    #     else:
    #         QtWidgets.QLabel.keyPressEvent(self, event)