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

class BulletEnemy(QGraphicsPixmapItem):
    def __init__(self, parent = None):
        QGraphicsPixmapItem.__init__(self,parent)
        self.setPixmap(QPixmap('assets/enemylaser.png'))
        self.sound = QtMultimedia.QSound('assets/sounds/shoot2.wav')
        self.sound.play()