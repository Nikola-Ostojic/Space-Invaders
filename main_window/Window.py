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
from entities.Enemy import Enemy
from entities.Shield import Shield
from PyQt5.QtGui import QPixmap

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter

from entities import Bullet

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
    
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)      
        

        # hold the set of keys we're pressing
        self.keys_pressed = set()

        # use a timer to get 60Hz refresh (hopefully)
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        # Postavljanje pozadine
        self.set_background()

        self.player = Player()
        self.player.setPos(400, 525)
        self.bullets = [Bullet.Bullet(PLAYER_BULLET_X_OFFSETS[0],PLAYER_BULLET_Y)]


        for b in self.bullets:
            b.setPos(WINDOW_WIDTH,WINDOW_HEIGHT)
            self.addItem(b)

        self.addItem(self.player)

        # Postavljanje neprijatelja
        enemies = []
        enemies.append(Enemy())
        enemies[0].setPos(100, 50)

        for i in range(0, 33):
            enemies.append(Enemy())
            if i == 11:
                enemies[i].setPos(enemies[0].x(), enemies[0].y() + 100)
                continue
            if i == 22:
                 enemies[i].setPos(enemies[11].x(), enemies[11].y() + 100)
                 continue              
            enemies[i].setPos(enemies[i - 1].x() + 100, enemies[i - 1].y())

        for i in range(0, 33):
            self.addItem(enemies[i])

        # Pomeranje neprijatelja
        self.moveEnemy = MoveEnemy()
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
        enemyLabel.setPos(newX, newY)

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())

    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

    def timerEvent(self, event):
        self.game_update()
        self.update()

    def game_update(self):
        self.player.game_update(self.keys_pressed)
        for b in self.bullets:
            b.game_update(self.keys_pressed, self.player)

    def set_background(self):
        loadedPicture = QImage('assets/background.png')
        brushBackground = QBrush(loadedPicture)
        self.setBackgroundBrush(brushBackground)

