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
from enemy_actions.EnemyMove import MoveEnemy, EnemyShoot
from player_actions.PlayerShoot import PlayerShoot
from PyQt5 import QtMultimedia

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
from key_notifier import KeyNotifier

from entities.Bullet import Bullet
from entities.BulletEnemy import BulletEnemy

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
        self.enemies = []
        self.enemies.append(Enemy())
        self.enemies[0].setPos(100, 50)

        for i in range(0, 33):
            self.enemies.append(Enemy())
            if i == 11:
                self.enemies[i].setPos(self.enemies[0].x(), self.enemies[0].y() + 60)
                continue
            if i == 22:
                 self.enemies[i].setPos(self.enemies[11].x(), self.enemies[11].y() + 60)
                 continue              
            self.enemies[i].setPos(self.enemies[i - 1].x() + 60, self.enemies[i - 1].y())     

        for i in range(0, 33):
            self.addItem(self.enemies[i])
            
        # Pomeranje neprijatelja
        self.moveEnemy = MoveEnemy()
        self.moveEnemy.calc_done.connect(self.move_enemy)
        self.moveEnemy.start()

        # Pucanje igraca
        self.shootLaser = PlayerShoot()
        self.shootLaser.calc_done.connect(self.move_laser_up)
        self.shootLaser.collision_detected.connect(self.player_laser_enemy_collide)
        self.shootLaser.start()
        self.playerOneCanShoot = True
        self.playerTwoCanShoot = True

        # Pucanje protivnika
        self.enemyShoot = EnemyShoot()
        self.enemyShoot.can_shoot.connect(self.enemy_shoot_laser)
        self.enemyShoot.move_down.connect(self.move_enemy_laser)
        self.enemyShoot.collision_detected.connect(self.enemy_hit_player)
        self.enemyShoot.collision_detected.connect(self.enemy_laser_shield_collide)
        #self.enemyShoot.next_level.connect(self.next_level)
        self.enemyShoot.start()

        self.enemyShoot.add_player(self.player)

        for i in range(0, 33):
            self.moveEnemy.add_enemy(self.enemies[i])
            self.shootLaser.add_enemy(self.enemies[i])
            self.enemyShoot.add_enemy(self.enemies[i])

        #Dodavanje stitova
        self.shields = []
        self.shields.append(Shield())
        self.shields[0].setPos(50, 350)
        self.shields.append(Shield())
        self.shields[1].setPos(400, 350)
        self.shields.append(Shield())
        self.shields[2].setPos(700, 350)

        for i in range(0, 3):
            self.addItem(self.shields[i])
            self.enemyShoot.add_shield(self.shields[i])

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
            self.sound = QtMultimedia.QSound('assets/sounds/invaderkilled.wav')
            self.sound.play()
            enemyLabel.hide()
            laserLabel.hide()
            self.remove_enemy_label(enemyLabel)
            self.moveEnemy.remove_enemy(enemyLabel)
            #self.enemyShoot.remove_enemy(enemyLabel)

        except Exception as e:
            print('Exception in Main_Thread/player_laser_enemy_collide method: ', str(e))

    def enemy_laser_shield_collide(self, shieldLabel: QGraphicsPixmapItem, laserLabel: QGraphicsPixmapItem):
        try:
            laserLabel.hide()
            for shield in self.shields:
                if shield == shieldLabel:
                    shield.makeDamage()
                    self.enemyShoot.remove_shield(shield)
                    print('Damage to shield')
        except Exception as e:
            print(str(e))


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

    def enemy_shoot_laser(self, startX, startY):
        enemyLaserLabel = BulletEnemy()
        enemyLaserLabel.setPos(startX, startY)
        self.addItem(enemyLaserLabel)

        # dodamo laser da moze da se krece ka dole
        self.enemyShoot.add_laser(enemyLaserLabel)

    def move_enemy_laser(self, enemyLaser: QGraphicsPixmapItem, newX, newY):
        if newY < WINDOW_HEIGHT - 50:
            enemyLaser.setPos(newX, newY)
        else:
            enemyLaser.hide()
            self.enemyShoot.remove_laser(enemyLaser)

    def enemy_hit_player(self, laserLabel: QGraphicsPixmapItem, playerLabel: QGraphicsPixmapItem):
        self.sound = QtMultimedia.QSound('assets/sounds/shipexplosion.wav')
        self.sound.play()
        laserLabel.hide()
        playerLabel.setPos(400, 525)
        '''
        if self. == 2:
            if self.player.playerLabel == playerLabel:
                self.player.lower_lives()
                self.update_lives_label(1)
            if self.playerTwo.playerLabel == playerLabel:
                self.playerTwo.lower_lives()
                self.update_lives_label(2)
        else:
        '''
        #self.player.lower_lives()
        #self.update_lives_label(1)


    def __update_position__(self, key):
        playerPos = self.player.pos()
        dx = 0

        if playerPos.x() + dx <= 0:
            if key == Qt.Key_D:
                dx += PLAYER_SPEED
        elif playerPos.x() + dx >= 845:
            if key == Qt.Key_A:
                dx -= PLAYER_SPEED
        else:
            if key == Qt.Key_D:
                dx += PLAYER_SPEED
            if key == Qt.Key_A:
                dx -= PLAYER_SPEED
        self.player.setPos(playerPos.x()+dx, playerPos.y())

        if key == Qt.Key_Space:
            if self.playerOneCanShoot:
                laserLabel = Bullet()
                self.player_shoot_laser(laserLabel, playerPos.x(), playerPos.y())
               
'''
        ## player 2 ##
        playerPos2 = self.player2.pos()
        dx2 = 0

        if playerPos2.x() + dx2 <= 0:
            if key == Qt.Key_Right:
                dx2 += PLAYER_SPEED
        elif playerPos2.x() + dx2 >= 845:
            if key == Qt.Key_Left:
                dx -= PLAYER_SPEED
        else:
            if key == Qt.Key_Right:
                dx2 += PLAYER_SPEED
            if key == Qt.Key_Left:
                dx2 -= PLAYER_SPEED
        self.player2.setPos(playerPos2.x()+dx, playerPos2.y())

        if key == Qt.Key_Enter:
            if self.playerTwoCanShoot:
                laserLabel = Bullet()
                self.player_shoot_laser(laserLabel, playerPos2.x(), playerPos2.y())
'''