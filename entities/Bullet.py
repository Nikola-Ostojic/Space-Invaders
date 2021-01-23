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

BULLET_SPEED = 10  # pix/frame
BULLET_FRAMES = 100
WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720

class Bullet(QGraphicsPixmapItem):
    calc_done = pyqtSignal(QGraphicsPixmapItem, int, int)
    collision_detected = pyqtSignal(QGraphicsPixmapItem, QGraphicsPixmapItem)

    def __init__(self, offset_x, offset_y, parent = None):
        QGraphicsPixmapItem.__init__(self,parent)

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
        while self.threadWorking:

            try:
                collided = False

                # Collision with enemy
                for enemy in self.enemyLabels:

                    if collided:
                        break

                    enemyGeo = enemy.geometry()
                    enemyXStart = enemyGeo.x()
                    enemyXEnd = enemyGeo.x() + config.IMAGE_WIDTH
                    enemyYStart = enemyGeo.y()
                    enemyYEnd = enemyGeo.y() + config.IMAGE_HEIGHT

                    enemyXArray = range(enemyXStart, enemyXEnd)
                    enemyYArray = range(enemyYStart, enemyYEnd)

                    # check for collision with laser
                    for laser in self.laserLabels:
                        laserGeo = laser.geometry()
                        laserXStart = laserGeo.x()
                        laserXEnd = laserGeo.x() + config.IMAGE_WIDTH
                        laserYStart = laserGeo.y()
                        laserYEnd = laserGeo.y() + config.IMAGE_HEIGHT

                        laserXArray = range(laserXStart, laserXEnd)
                        laserYArray = range(laserYStart, laserYEnd)

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
                    laserGeo = label.geometry()
                    laserX = laserGeo.x()
                    laserY = laserGeo.y() - config.PLAYER_LASER_SPEED
                    self.calc_done.emit(label, laserX, laserY)

                sleep(0.05)
            except Exception as e:
                print('Exception in Bullet_Thread: ', str(e))




    #     self.setPixmap(QPixmap('assets/laser.png'))
    #     self.offset_x = offset_x
    #     self.offset_y = offset_y
    #     self.active = False
    #     self.frames = 0

    # def game_update(self, keys_pressed, player):
    #     if not self.active:
    #         if Qt.Key_Space in keys_pressed:
    #             self.active = True
    #             self.setPos(player.x()+self.offset_x,player.y()+self.offset_y)
    #             self.frames = BULLET_FRAMES
    #             self.sound = QtMultimedia.QSound('assets/sounds/shoot.wav')
    #             self.sound.play()
    #     else:
    #         self.setPos(self.x(),self.y()-BULLET_SPEED)
    #         self.frames -= 1
    #         if self.frames <= 0:
    #             self.active = False
    #             self.setPos(WINDOW_WIDTH, WINDOW_HEIGTH)