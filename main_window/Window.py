import sys

from enemy_actions.EnemyMove import MoveEnemy

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

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter

from entities import Bullet
from entities import Bullet2

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

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FRAME_TIME_MS = 16  # ms/frame
PLAYER_BULLET_X_OFFSETS = [23, 45]
PLAYER_BULLET_Y         = 15

class Window(QGraphicsScene):
    
    def __init__(self, singlemulti, parent = None):
        QGraphicsScene.__init__(self, parent)


        # ShootLaser thread
        self.shootLaser = Bullet()
        self.shootLaser.calc_done.connect(self.move_laser_up)
        self.shootLaser.collision_detected.connect(self.player_laser_enemy_collide)
        self.shootLaser.moving_collision_detected.connect(self.player_laser_moving_enemy_collide)
        self.shootLaser.start()      
        

        # # hold the set of keys we're pressing
        # self.keys_pressed = set()

        # use a timer to get 60Hz refresh (hopefully)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        # Postavljanje pozadine
        self.set_background()

        #Postavljanje Glavnog igraca
        if (singlemulti == 1):
            self.player = Player()
            self.player.setPos(400, 525)

            # Pucanje
            self.bullets = [Bullet.Bullet(PLAYER_BULLET_X_OFFSETS[0],PLAYER_BULLET_Y)]


            for b in self.bullets:
                b.setPos(WINDOW_WIDTH,WINDOW_HEIGHT)
                self.addItem(b)

            self.addItem(self.player)

        elif (singlemulti == 2):
            self.player = Player()
            self.player.setPos(400, 525)

            # Pucanje
            self.bullets = [Bullet.Bullet(PLAYER_BULLET_X_OFFSETS[0],PLAYER_BULLET_Y)]


            for b in self.bullets:
                b.setPos(WINDOW_WIDTH,WINDOW_HEIGHT)
                self.addItem(b)

            self.addItem(self.player)

            self.player2 = Player2()
            self.player2.setPos(100, 525)

            # Pucanje
            self.bullets2 = [Bullet2.Bullet2(PLAYER_BULLET_X_OFFSETS[0],PLAYER_BULLET_Y)]


            for d in self.bullets2:
                d.setPos(WINDOW_WIDTH,WINDOW_HEIGHT)
                self.addItem(d)

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
        for i in range(len(self.enemyLabels)):
            #self.moveEnemy.add_enemy(self.enemyLabels[i])
            #self.enemyShoot.add_enemy(self.enemyLabels[i])
            self.shootLaser.add_enemy(self.enemyLabels[i])
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
        self.view.setFixedSize(WINDOW_WIDTH,WINDOW_HEIGHT)
        self.setSceneRect(0,0,WINDOW_WIDTH,WINDOW_HEIGHT)  
            
    def move_enemy(self, enemyPixMap: QGraphicsPixmapItem, newX, newY):
        enemyPixMap.setPos(newX, newY)

    def remove_enemy_label(self, enemy: QGraphicsPixmapItem):
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    # def keyPressEvent(self, event):
    #     self.keys_pressed.add(event.key())

    # def keyReleaseEvent(self, event):
    #     self.keys_pressed.remove(event.key())

    def timerEvent(self, event):
        self.game_update()
        self.update()

    # def game_update(self):
    #     self.player.game_update(self.keys_pressed)
    #     for b in self.bullets:
    #         b.game_update(self.keys_pressed, self.player)

    # def game_update2(self):
    #     self.player2.game_update2(self.keys_pressed)
    #     for d in self.bullets:
    #         d.game_update2(self.keys_pressed, self.player2)

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

    def player_laser_moving_enemy_collide(self, enemyLabel: QGraphicsPixmapItem, laserLabel: QGraphicsPixmapItem):
        try:
            enemyLabel.hide()
            laserLabel.hide()
            self.remove_enemy_label(enemyLabel)
            self.enemyAttack.remove_moving_enemy(enemyLabel)
        except Exception as e:
            print('Exception in Main_Thread/player_laser_enemy_collide method: ', str(e))

    def player_shoot_laser(self, startX, startY):
        laserPixmap = QPixmap('images/laser.png')
        laserLabel = QGraphicsPixmapItem(self)

        laserLabel.setPixmap(laserPixmap)
        laserLabel.setGeometry(startX, startY, config.IMAGE_WIDTH, config.IMAGE_HEIGHT)
        laserLabel.show()

        self.shootLaser.add_laser(laserLabel)

    def move_laser_up(self, laserLabel: QGraphicsPixmapItem, newX, newY):
        if newY > 0:
            laserLabel.move(newX, newY)
        else:
            laserLabel.hide()
            self.shootLaser.remove_laser(laserLabel)

    def __update_position__(self, key):
        playerPos = self.playerLabel.geometry()

        if key == Qt.Key_D:
            if self.try_move_player(playerPos.x() + self.playerOneSpeed):
                self.playerLabel.setGeometry(playerPos.x() + self.playerOneSpeed, playerPos.y(), playerPos.width(), playerPos.height())
        elif key == Qt.Key_A:
            if self.try_move_player(playerPos.x() - self.playerOneSpeed):
                self.playerLabel.setGeometry(playerPos.x() - self.playerOneSpeed, playerPos.y(), playerPos.width(), playerPos.height())
        elif key == Qt.Key_Space:
            if self.player.get_lives() > 0 and self.playerOneCanShoot:
                self.player_shoot_laser(playerPos.x() + config.IMAGE_WIDTH//2, playerPos.y() - config.IMAGE_HEIGHT)

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
