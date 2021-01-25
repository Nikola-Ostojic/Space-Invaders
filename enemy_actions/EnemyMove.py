from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView
)

from PyQt5.QtGui import (
    QBrush,
    QPixmap
)

from PyQt5.QtCore import pyqtSignal, QThread, QObject, QTimer

import time
from time import sleep
from random import randint

BULLET_SPEED = 10
COOLDOWN = 1000

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
                                self.calc_done.emit(enemy, enemyX, enemyY + 20)
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
                                self.calc_done.emit(enemy, enemyX, enemyY + 20)
                            self.goRight = False
                            self.goLeft = True
                            break
                    sleep(0.25)

            except Exception as e:
                print('Exception in MoveEnemy_Thread: ', str(e))

class EnemyShoot(QObject):
    can_shoot = pyqtSignal(int, int)
    collision_detected = pyqtSignal(QGraphicsPixmapItem, QGraphicsPixmapItem)
    collision_detected_with_shield = pyqtSignal(QGraphicsPixmapItem, QGraphicsPixmapItem)
    move_down = pyqtSignal(QGraphicsPixmapItem, int, int)
    next_level = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.current_level = 1

        self.threadWorking = True
        self.enemies = []
        self.lasers = []
        self.players = []
        self.shields = []

        self.enemyLaserSpeed = BULLET_SPEED
        self.shootingTimerInterval = COOLDOWN
        self.canShoot = False
        self.shootingTimer = QTimer()
        self.shootingTimer.setInterval(COOLDOWN)
        self.shootingTimer.timeout.connect(self.alert_shooting)
        self.shootingTimer.start()

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_enemy(self, enemyLabel: QGraphicsPixmapItem):
        self.enemies.append(enemyLabel)

    def remove_enemy(self, enemyLabel: QGraphicsPixmapItem):
        if enemyLabel in self.enemies:
            self.enemies.remove(enemyLabel)

    def add_laser(self, laserLabel: QGraphicsPixmapItem):
        self.lasers.append(laserLabel)

    def remove_laser(self, laserLabel: QGraphicsPixmapItem):
        if laserLabel in self.lasers:
            self.lasers.remove(laserLabel)

    def add_player(self, playerLabel: QGraphicsPixmapItem):
        self.players.append(playerLabel)

    def remove_player(self, playerLabel: QGraphicsPixmapItem):
        if playerLabel in self.players:
            self.players.remove(playerLabel)

    def add_shield(self, shieldLabel: QGraphicsPixmapItem):
        self.shields.append(shieldLabel)

    def remove_shield(self, shieldLabel: QGraphicsPixmapItem):
        if shieldLabel in self.shields:
            self.shields.remove(shieldLabel)

    def update_level(self, newInterval, newLaserSpeed):
        if (self.shootingTimerInterval - newInterval) >= 200:
            self.shootingTimerInterval -= newInterval
            self.shootingTimer.setInterval(self.shootingTimerInterval)
            #print('Changed shooting interval to: ', self.shootingTimerInterval)

        if (self.enemyLaserSpeed + newLaserSpeed) <= 18:
            self.enemyLaserSpeed += newLaserSpeed
            #print('Changed enemy laser speed to: ', self.enemyLaserSpeed)

    def die(self):
        self.threadWorking = False
        self.shootingTimer.stop()
        #print('Stopping shooting timer')
        self.thread.quit()

    def find_ymax(self):
        if len(self.enemies) > 0:
            enemy = self.enemies[0]
            enemyPos = enemy.pos()
            yMax = enemyPos.y()
            for i in range(1, len(self.enemies)):
                enemy = self.enemies[i]
                enemyPos = enemy.pos()
                y = enemyPos.y()
                if yMax < y:
                    yMax = y
            return yMax

    def get_enemies_from_y(self, yParam):
        result = []
        if len(self.enemies) > 0:
            for i in range(len(self.enemies)):
                enemy = self.enemies[i]
                enemyPos = enemy.pos()
                y = enemyPos.y()
                if y == yParam:
                    result.append(enemy)
        return result

    def alert_shooting(self):
        if not self.canShoot:
            self.canShoot = True

    def __work__(self):
        #print("Tred pucanja neprijatelja pokrenut")
        while self.threadWorking:
            try:
                if self.canShoot:
                    # CHOOSE A SHOOTER
                    #print('Biram neprijatelja')
                    yArray = []
                    #print(len(self.enemies))
                    for enemy in self.enemies:
                        enemyPos = enemy.pos()
                        enemyY = enemyPos.y()
                        if enemyY not in yArray:
                            yArray.append(enemyY)

                    sortedYs = yArray
                    #print(len(sortedYs))

                    if len(sortedYs) == 0:
                        #Dozvoli prvo da se svi laseri spuste
                        if len(self.lasers) == 0:
                            sleep(5)
                            self.current_level += 1
                            self.next_level.emit(self.current_level)

                    else:
                        yMax = sortedYs[-1]
                        lowestRowEnemies = self.get_enemies_from_y(yMax)

                        if len(lowestRowEnemies) == 11:
                            # Posto ih imamo 10, mozemo ih sve uzeti i jedan od njih ce da puca
                            randIndex = randint(0, 10)
                            enemy = lowestRowEnemies[randIndex]
                            enemyPos = enemy.pos()
                            laserX = enemyPos.x() + 50
                            laserY = enemyPos.y() + 50
                            self.can_shoot.emit(laserX, laserY)
                            self.canShoot = False

                        elif len(lowestRowEnemies) < 11:
                            # Imamo manje od 10, mozda neko iznad moze da puca
                            if len(sortedYs) > 1:
                                y = sortedYs[-2]
                            else:
                                #print("Ostao je samo jedan red")
                                y = sortedYs[-1]

                            upperEnemies = self.get_enemies_from_y(y)

                            for lowerEnemy in lowestRowEnemies:
                                lowerEnemyPos = lowerEnemy.pos()
                                lowerRowEnemyX = lowerEnemyPos.x()
                                for upperEnemy in upperEnemies:
                                    upperEnemyPos = upperEnemy.pos()
                                    upperEnemyX = upperEnemyPos.x()
                                    if lowerRowEnemyX == upperEnemyX:
                                        if upperEnemies in upperEnemies:
                                            upperEnemies.remove(upperEnemy)

                            lowestRowEnemies += upperEnemies

                            # probaj pucati
                            randIndex = randint(0, len(lowestRowEnemies)-1)
                            enemy = lowestRowEnemies[randIndex]
                            enemyPos = enemy.pos()
                            laserX = enemyPos.x() + 50
                            laserY = enemyPos.y() + 50
                            self.can_shoot.emit(laserX, laserY)
                            self.canShoot = False

                        # else:
                        #     print('Okej, nesto ovde ne radi ...')
            except Exception as e:
                print('Exception in EnemyShoot_Thread: ', str(e))

            try:
                # MOVE LASER DOWN
                if len(self.lasers) > 0:
                    for laser in self.lasers:
                        laserPos = laser.pos()
                        laserX = laserPos.x()
                        laserY = laserPos.y() + self.enemyLaserSpeed

                        # Check for collision with players
                        #print('Broj igraca: ', len(self.players))
                        if len(self.players) > 0:
                            for player in self.players:
                                playerPos = player.pos()
                                playerXStart = playerPos.x()
                                playerXEnd = playerPos.x() + 50
                                playerY = playerPos.y()

                                xIsEqual = False

                                if playerXStart <= laserX <= playerXEnd:
                                    xIsEqual = True

                                # nova provera za Y osu zbog brzih lasera
                                playerYRange = range(int(playerY), int(playerY + 50))
                                laserYRange = range(int(laserY), int(laserY + 50))
                                #print('Player Y Range: {} - {}'.format(playerYRange[1], playerYRange[-1]))
                                #print('Laser Y Range: {} - {}'.format(laserYRange[1], laserYRange[-1]))

                                for y in laserYRange:
                                    if y in playerYRange and xIsEqual:
                                        #print('enemy hit player with laser')
                                        self.collision_detected.emit(laser, player)
                                        self.remove_laser(laser)
                                        break
                                    else:
                                        self.move_down.emit(laser, laserX, laserY)

                        else:
                            self.move_down.emit(laser, laserX, laserY)

                        #print(len(self.shields))
                        if (len(self.shields) > 0):
                            for laser in self.lasers:
                                laserPos = laser.pos()
                                laserX = laserPos.x()
                                laserY = laserPos.y() + self.enemyLaserSpeed
                                for shield in self.shields:
                                    shieldPos = shield.pos()
                                    #print(shieldPos)
                                    shieldXStart = shieldPos.x()
                                    shieldXEnd = shieldXStart + 200
                                    shieldY = shieldPos.y()

                                    shieldXEqual = False

                                    if shieldXStart <= laserX <= shieldXEnd:
                                        shieldXEqual = True
                                    shieldYRange = range(int(shieldY), int(shieldY + 50))
                                    laserYRange = range(int(laserY), int(laserY + 50))

                                    for y in laserYRange:
                                        if y in shieldYRange and shieldXEqual:
                                            #print('enemy hit shield with laser')
                                            self.collision_detected_with_shield.emit(laser, shield)
                                            self.remove_laser(laser)
                                            break
                                        else:
                                            self.move_down.emit(laser, laserX, laserY)
                        else:
                            self.move_down.emit(laser, laserX, laserY)

            except Exception as e:
                print('Exception in Moving_Laser: ', str(e))

            sleep(0.05)