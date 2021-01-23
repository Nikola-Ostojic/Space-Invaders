from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView
)

from PyQt5.QtCore import pyqtSignal, QThread, QObject, QTimer

import time
from time import sleep

class MoveEnemy(QObject):
    calc_done = pyqtSignal(QGraphicsPixmapItem, int, int)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.enemies = []
        self.goLeft = True
        self.goRight = False
       
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def remove_enemy(self, enemyPixmap: QGraphicsPixmapItem):
        if enemyPixmap in self.enemies:
            self.enemies.remove(enemyPixmap)

    def add_enemy(self, enemyPixmap: QGraphicsPixmapItem):
        self.enemies.append(enemyPixmap)

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    #Kretanje neprijatelja
    def __work__(self):

        while self.threadWorking:

            if self.goRight:
                for i in range(0, 33):
                    #self.enemies[i].setPos(enemies[i - 1].x(), enemies[i - 1].y() + 50)
                    #self.calc_done.emit(self.enemies[i], self.enemies[i].x(), self.enemies[i].y() + 50)
                    self.calc_done.emit(self.enemies[i], self.enemies[i].x() + 10, self.enemies[i].y())
                    if self.enemies[32].x() > 891:
                        for i in range(0, 33):
                            self.calc_done.emit(self.enemies[i], self.enemies[i].x(), self.enemies[i].y() + 5)
                        time.sleep(0.1)
                        self.goRight = False
                        self.goLeft = True
                        break
                time.sleep(0.1)

            elif self.goLeft:
                for i in range(0, 33):
                    #self.enemies[i].setPos(enemies[i - 1].x(), enemies[i - 1].y() - 50)
                    self.calc_done.emit(self.enemies[i], self.enemies[i].x() - 10, self.enemies[i].y())                
                    if self.enemies[11].x() < 5:                    
                        for i in range(0, 33):
                            self.calc_done.emit(self.enemies[i], self.enemies[i].x(), self.enemies[i].y() + 5)
                        time.sleep(1.5)
                        self.goRight = True
                        self.goLeft = False
                        break
                time.sleep(0.1)



