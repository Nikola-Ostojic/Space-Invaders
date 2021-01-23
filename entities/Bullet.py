import sys
from PyQt5.QtCore import (
    Qt,
    QBasicTimer
)
from PyQt5 import QtMultimedia

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

BULLET_SPEED = 10  # pix/frame
BULLET_FRAMES = 100
WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720

class Bullet(QGraphicsPixmapItem):
    def __init__(self, parent = None):
        QGraphicsPixmapItem.__init__(self,parent)
        self.setPixmap(QPixmap('assets/laser.png'))