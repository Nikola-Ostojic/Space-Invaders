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

PLAYER_SPEED = 3

class Player(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap('assets/ship.png').scaled(50, 50))
    
    def game_update(self, keys_pressed):
        dx = 0
        dy = 0
        if self.x()+dx <= 0:
            if Qt.Key_Right in keys_pressed:
                dx += PLAYER_SPEED
        elif self.x()+dx >= 850:
            if Qt.Key_Left in keys_pressed:
                dx -= PLAYER_SPEED
        else:
            if Qt.Key_Right in keys_pressed:
                dx += PLAYER_SPEED
            if Qt.Key_Left in keys_pressed:
                dx -= PLAYER_SPEED

        self.setPos(self.x()+dx, self.y()+dy)