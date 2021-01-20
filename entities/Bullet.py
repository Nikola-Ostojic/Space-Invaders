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
    def __init__(self, offset_x, offset_y, parent = None):
        QGraphicsPixmapItem.__init__(self,parent)
        self.setPixmap(QPixmap('assets/laser.png'))
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.active = False
        self.frames = 0

    def game_update(self, keys_pressed, player):
        if not self.active:
            if Qt.Key_Space in keys_pressed:
                self.active = True
                self.setPos(player.x()+self.offset_x,player.y()+self.offset_y)
                self.frames = BULLET_FRAMES
                self.sound = QtMultimedia.QSound('assets/sounds/shoot.wav')
                self.sound.play()
        else:
            self.setPos(self.x(),self.y()-BULLET_SPEED)
            self.frames -= 1
            if self.frames <= 0:
                self.active = False
                self.setPos(WINDOW_WIDTH, WINDOW_HEIGTH)