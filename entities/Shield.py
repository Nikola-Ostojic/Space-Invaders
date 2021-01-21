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

class Shield(QGraphicsPixmapItem):
    def __init__(self):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap('assets/shields/full.png').scaled(200, 200))