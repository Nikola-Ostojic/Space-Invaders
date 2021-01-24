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

# Board settings
BOARD_WIDTH = 800
BOARD_HEIGHT = 600
IMAGE_WIDTH = 50
IMAGE_HEIGHT = 50

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
            try:
                # movement logic
                if self.goLeft:
                    for enemy in self.enemies:
                        enemyPos = enemy.pos()
                        enemyX = enemyPos.x()
                        enemyY = enemyPos.y()
                        if enemyX > 50:
                            self.goLeft = True
                            self.goRight = False
                            self.calc_done.emit(enemy, enemyX - 10, enemyY)
                        else:
                            for enemy in self.enemies:
                                enemyPos = enemy.pos()
                                enemyX = enemyPos.x()
                                enemyY = enemyPos.y()
                                self.calc_done.emit(enemy, enemyX, enemyY + 15)
                            self.goLeft = False
                            self.goRight = True
                            break
                    sleep(0.25)

                elif self.goRight:
                    for enemy in reversed(self.enemies):
                        enemyPos = enemy.pos()
                        enemyX = enemyPos.x()
                        enemyY = enemyPos.y()

                        if enemyX < 800:
                            self.goRight = True
                            self.goLeft = False
                            self.calc_done.emit(enemy, enemyX + 10, enemyY)
                        else:
                            for enemy in self.enemies:
                                enemyPos = enemy.pos()
                                enemyX = enemyPos.x()
                                enemyY = enemyPos.y()
                                self.calc_done.emit(enemy, enemyX, enemyY + 15)
                            self.goRight = False
                            self.goLeft = True
                            break
                    sleep(0.25)

            except Exception as e:
                print('Exception in MoveEnemy_Thread: ', str(e))