import sys
from PyQt5.QtCore import (
    Qt,
    QBasicTimer
)
from PyQt5.QtGui import (
    QBrush,
    QPixmap
)
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView
)
class Enemy(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap('assets/enemy1.png').scaled(50, 50))

    # def keyPressEvent(self, event):

    #     if event.key() == QtCore.Qt.Key_A:
    #         if (self.x() > 1):
    #             self.move(self.x() - 10, self.y())
    #     elif event.key() == QtCore.Qt.Key_D:
    #         if (self.x() + 50 < WINDOW_WIDTH):
    #             self.move(self.x() + 10, self.y())
    #     else:
    #         QtWidgets.QLabel.keyPressEvent(self, event)