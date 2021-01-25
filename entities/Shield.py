import sys
from PyQt5.QtCore import (
    Qt,
    QBasicTimer, pyqtSignal
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

class Shield(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap('assets/shields/full.png').scaled(150, 50))
        self.health = 100

    def makeDamage(self):
        self.health = self.health - 30

    def update_shield(self, shieldLabel: QGraphicsPixmapItem):
        if 75 >= self.health >= 50:
            self.setPixmap(QPixmap('assets/shields/1st_stage.png').scaled(150, 50))
        elif 50 >= self.health >= 25:
            self.setPixmap(QPixmap('assets/shields/2nd_stage.png').scaled(150, 50))
        elif 25 >= self.health >= 0:
            self.setPixmap(QPixmap('assets/shields/3rd_stage.png').scaled(150, 50))
        else:
            self.hide()