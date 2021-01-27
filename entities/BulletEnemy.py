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
    sound_shoot2 = QtMultimedia.QSound('assets/sounds/shoot2.wav')

    def __init__(self, parent = None):
        QGraphicsPixmapItem.__init__(self,parent)
        self.setPixmap(QPixmap('assets/enemylaser.png'))
        self.sound_shoot2.play()