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
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QObject
from time import sleep

BULLET_SPEED = 10  # pix/frame
WINDOW_WIDTH = 900
WINDOW_HEIGTH = 600

class PlayerShoot(QObject):
    calc_done = pyqtSignal(QGraphicsPixmapItem, int, int)
    collision_detected = pyqtSignal(QGraphicsPixmapItem, QGraphicsPixmapItem)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.laserLabels = []
        self.enemyLabels = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_laser(self, laserLabel: QGraphicsPixmapItem):
        self.laserLabels.append(laserLabel)

    def remove_laser(self, laserLabel: QGraphicsPixmapItem):
        if laserLabel in self.laserLabels:
            self.laserLabels.remove(laserLabel)

    def add_enemy(self, enemyLabel: QGraphicsPixmapItem):
        self.enemyLabels.append(enemyLabel)

    def remove_enemy(self, enemyLabel: QGraphicsPixmapItem):
        if enemyLabel in self.enemyLabels:
            self.enemyLabels.remove(enemyLabel)

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    def __work__(self):
        print('Pokrecem tred pucanja')
        while self.threadWorking:
            #print('Lasers: ', len(self.laserLabels))
            #print('Enemies: ', len(self.enemyLabels))
            #print("Ulazim u proveru kolizije")
            try:
                collided = False

                # Collision with enemy
                for enemy in self.enemyLabels:
                    if collided:
                        break
                    enemyGeo = enemy.pos()
                    enemyXStart = enemyGeo.x()
                    enemyXEnd = enemyGeo.x() + 50
                    enemyYStart = enemyGeo.y()
                    enemyYEnd = enemyGeo.y() + 50

                    enemyXArray = range(int(enemyXStart), int(enemyXEnd))
                    enemyYArray = range(int(enemyYStart), int(enemyYEnd))

                    # check for collision with laser
                    for laser in self.laserLabels:
                        laserGeo = laser.pos()
                        laserXStart = laserGeo.x()
                        laserXEnd = laserGeo.x() + 30
                        laserYStart = laserGeo.y()
                        laserYEnd = laserGeo.y() + 50

                        laserXArray = range(int(laserXStart), int(laserXEnd))
                        laserYArray = range(int(laserYStart), int(laserYEnd))

                        # drugi nacin detekcije kolizije
                        for enemyY in enemyYArray:
                            if collided:
                                break

                            if enemyY in laserYArray:
                                for enemyX in enemyXArray:
                                    if enemyX in laserXArray:
                                        self.remove_enemy(enemy)
                                        self.remove_laser(laser)
                                        self.collision_detected.emit(enemy, laser)
                                        collided = True
                                        break               

                # MOVE LABELS UP
                for label in self.laserLabels:
                    laserGeo = label.pos()
                    laserX = laserGeo.x()
                    laserY = laserGeo.y() - BULLET_SPEED
                    self.calc_done.emit(label, laserX, laserY)

                sleep(0.05)
            except Exception as e:
                print('Exception in Bullet_Thread: ', str(e))