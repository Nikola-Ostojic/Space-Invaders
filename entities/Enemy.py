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
        self.setPixmap(QPixmap('assets/enemy1.png').scaled(40, 40))