import sys
from PyQt5.QtCore import QThread
import multiprocessing as mp

import time
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import  QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from entities.Player import Player
from entities.Player2 import Player2
from entities.Enemy import Enemy
from entities.Shield import Shield
from PyQt5.QtGui import QPixmap
from enemy_actions.EnemyMove import MoveEnemy
from player_actions.PlayerShoot import PlayerShoot

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
from key_notifier import KeyNotifier

from entities.Bullet import Bullet

from PyQt5.QtCore import (
    Qt,
    QBasicTimer
)
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView
)

PLAYER_BULLET_X_OFFSETS = [23, 45]
PLAYER_BULLET_Y         = 15
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FRAME_TIME_MS = 16  # ms/frame
PLAYER_SPEED = 8

class Window(QGraphicsScene):
    
    def __init__(self, singlemulti, parent = None):
        QGraphicsScene.__init__(self, parent)

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.do_key_press)
        self.key_notifier.start()

        numberOfPlayer = singlemulti
        # ShootLaser thread
        self.shootLaser = PlayerShoot()
        self.shootLaser.calc_done.connect(self.move_laser_up)
        self.shootLaser.collision_detected.connect(self.player_laser_enemy_collide)
        self.shootLaser.start()
        self.playerOneCanShoot = True
        #self.playerTwoCanShoot = True

        # use a timer to get 60Hz refresh (hopefully)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        # Postavljanje pozadine
        self.set_background()

        #Postavljanje Glavnog igraca
        if (numberOfPlayer == 1):
            self.player = Player()
            self.player.setPos(400, 525)
            self.addItem(self.player)

        elif (numberOfPlayer == 2):
            self.player = Player()
            self.player.setPos(400, 525)
            self.addItem(self.player)

            self.player2 = Player2()
            self.player2.setPos(100, 525)
            self.addItem(self.player2)   

        # Postavljanje neprijatelja
        enemies = []
        enemies.append(Enemy())
        enemies[0].setPos(100, 50)

        for i in range(0, 33):
            enemies.append(Enemy())
            if i == 11:
                enemies[i].setPos(enemies[0].x(), enemies[0].y() + 60)
                continue
            if i == 22:
                 enemies[i].setPos(enemies[11].x(), enemies[11].y() + 60)
                 continue              
            enemies[i].setPos(enemies[i - 1].x() + 60, enemies[i - 1].y())     

        for i in range(0, 33):
            self.addItem(enemies[i])

        # add enemies for other stuff
       # for i in range(len(self.enemies)):
            #self.moveEnemy.add_enemy(self.enemyLabels[i])
            #self.enemyShoot.add_enemy(self.enemyLabels[i])
            #self.shootLaser.add_enemy(self.enemies[i])
            #self.enemyAttack.add_enemy(self.enemyLabels[i])

        # Pomeranje neprijatelja
        self.moveEnemy = MoveEnemy()
        for i in range(0, 33):
            self.moveEnemy.add_enemy(enemies[i])
        self.moveEnemy.calc_done.connect(self.move_enemy)
        self.moveEnemy.start()

        #Dodavanje stitova
        shields = []
        shields.append(Shield())
        shields[0].setPos(50, 350)
        shields.append(Shield())
        shields[1].setPos(400, 350)
        shields.append(Shield())
        shields[2].setPos(700, 350)

        for i in range(0, 3):
            self.addItem(shields[i])      

        self.view = QGraphicsView(self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.show()
        #self.view.setFixedSize(WINDOW_WIDTH,WINDOW_HEIGHT)
        self.setSceneRect(0,0,WINDOW_WIDTH,WINDOW_HEIGHT)  
            
    def move_enemy(self, enemyPixMap: QGraphicsPixmapItem, newX, newY):
        enemyPixMap.setPos(newX, newY)

    def remove_enemy_label(self, enemy: QGraphicsPixmapItem):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())

    def do_key_press(self, key):
        try:
            self.__update_position__(key)
        except Exception as e:
            print('Exception: {}'.format(str(e)))

    def set_background(self):
        loadedPicture = QImage('assets/background.png')
        brushBackground = QBrush(loadedPicture)
        self.setBackgroundBrush(brushBackground)

    def player_laser_enemy_collide(self, enemyLabel: QGraphicsPixmapItem, laserLabel: QGraphicsPixmapItem):
        try:
            enemyLabel.hide()
            laserLabel.hide()
            self.remove_enemy_label(enemyLabel)
            self.moveEnemy.remove_enemy(enemyLabel)
            #self.enemyShoot.remove_enemy(enemyLabel)

        except Exception as e:
            print('Exception in Main_Thread/player_laser_enemy_collide method: ', str(e))

    def player_shoot_laser(self, laserLabel: QGraphicsPixmapItem, startX, startY):
        laserLabel.setPos(startX + PLAYER_BULLET_X_OFFSETS[0], startY - PLAYER_BULLET_Y)
        self.addItem(laserLabel)
        self.shootLaser.add_laser(laserLabel)

    def move_laser_up(self, laserLabel: QGraphicsPixmapItem, newX, newY):
        if newY > 0:
            laserLabel.setPos(newX, newY)
        else:
            laserLabel.hide()
            self.shootLaser.remove_laser(laserLabel)

    def __update_position__(self, key):
        playerPos = self.player.pos()

        if key == Qt.Key_D:
                self.player.setPos(playerPos.x() + PLAYER_SPEED, playerPos.y())
        elif key == Qt.Key_A:
                self.player.setPos(playerPos.x() - PLAYER_SPEED, playerPos.y())
        elif key == Qt.Key_Space:
            if self.playerOneCanShoot:
                laserLabel = Bullet()
                self.player_shoot_laser(laserLabel, playerPos.x(), playerPos.y())
                '''
        # 2 players
        if self.startPlayers == 2:
            playerTwoPos = self.playerTwoLabel.geometry()

            # player two moving
            if key == Qt.Key_Right:
                if self.try_move_player(playerTwoPos.x() + self.playerTwoSpeed):
                    self.playerTwoLabel.setGeometry(playerTwoPos.x() + self.playerTwoSpeed, playerTwoPos.y(), playerTwoPos.width(), playerTwoPos.height())
            elif key == Qt.Key_Left:
                if self.try_move_player(playerTwoPos.x() - self.playerTwoSpeed):
                    self.playerTwoLabel.setGeometry(playerTwoPos.x() - self.playerTwoSpeed, playerTwoPos.y(), playerTwoPos.width(), playerTwoPos.height())
            elif key == Qt.Key_0:
                if self.playerTwo.get_lives() > 0 and self.playerTwoCanShoot:
                    self.player_shoot_laser(playerTwoPos.x() + config.IMAGE_WIDTH // 2, playerTwoPos.y() - config.IMAGE_HEIGHT)
            '''