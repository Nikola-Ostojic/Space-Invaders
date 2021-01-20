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

        # Test 1 enemy
        # PROVERI ZASTO NE RADI ENEMY
        #self.enemy = Enemy()
        #self.enemy.setPos(400, 525)

        for b in self.bullets:
            b.setPos(WINDOW_WIDTH,WINDOW_HEIGHT)
            self.addItem(b)
        self.addItem(self.player)

        self.view = QGraphicsView(self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.show()
        self.view.setFixedSize(WINDOW_WIDTH,WINDOW_HEIGHT)
        self.setSceneRect(0,0,WINDOW_WIDTH,WINDOW_HEIGHT)

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
        
        

/*from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from entities.Player import Player
from entities.Enemy import Enemy
from PyQt5.QtGui import QPixmap

from PyQt5 import QtGui

WINDOW_WIDTH = 1280
WINDOW_HEIGTH = 720

class Window(QWidget):
    
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)     

        self.setWindowTitle('Space Invaders')
        self.window_width = WINDOW_WIDTH
        self.window_heigth = WINDOW_HEIGTH       
        self.setGeometry(100, 100, self.window_width, self.window_heigth)

        self.set_background()

        lbl1 = Player(self)
        lbl1.move(520, 600)
        lbl1.setFocus()

        labele = []
        labele.append(Enemy(self))
        labele[0].move(100, 100)

        for i in range(1, 33):
            labele.append(Enemy(self))
            if i % 11 == 0:
                labele[i].move(labele[0].x(), labele[i].y() + 100)
            labele[i].move(labele[i - 1].x() + 100, labele[i - 1].y())

        

    def set_background(self):
        background = QImage('assets/background.png')
        background = background.scaled(WINDOW_WIDTH, WINDOW_HEIGTH)
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(pallete)*/


