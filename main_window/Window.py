import sys
from PyQt5.QtCore import QThread
import multiprocessing

import time
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import  QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QHBoxLayout
from entities.Player import Player
from entities.Player2 import Player2
from entities.Enemy import Enemy
from entities.Shield import Shield
from PyQt5.QtGui import QPixmap, QFont
from enemy_actions.EnemyMove import MoveEnemy, EnemyShoot
from player_actions.PlayerShoot import PlayerShoot
from PyQt5 import QtMultimedia, QtCore

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

from PyQt5.QtCore import pyqtSignal

PLAYER_BULLET_X_OFFSETS = [23, 45]
PLAYER_BULLET_Y         = 15
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FRAME_TIME_MS = 16  # ms/frame
PLAYER_SPEED = 8

class Window(QGraphicsScene):

    next_level = pyqtSignal(int)

    next_level2 = pyqtSignal(int)

    def __init__(self, singlemulti, level_number, parent = None):
        QGraphicsScene.__init__(self, parent)

        


        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.do_key_press)
        self.key_notifier.start()

        self.numberOfPlayer = singlemulti
        self.level_numberrr = level_number

        # Postavljanje pozadine
        self.set_background()

        #Postavljanje Glavnog igraca
        if (self.numberOfPlayer == 1):
            self.player = Player()
            self.player.setPos(400, 525)
            self.addItem(self.player)
            self.flag_playerOneDead=False

        elif (self.numberOfPlayer == 2):
            self.player = Player()
            self.player.setPos(400, 525)
            self.addItem(self.player)
            self.flag_playerOneDead=False

            self.player2 = Player2()
            self.player2.setPos(100, 525)
            self.addItem(self.player2)   
            self.flag_playerTwoDead=False

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
        self.enemyShoot.collision_detected_with_shield.connect(self.enemy_laser_shield_collide)
        #self.enemyShoot.next_level.connect(self.next_level)
        if self.numberOfPlayer == 1:
            self.enemyShoot.add_player(self.player)
        else:
            self.enemyShoot.add_player(self.player)
            self.enemyShoot.add_player(self.player2)
        self.enemyShoot.start()

        for i in range(0, 33):
            self.moveEnemy.add_enemy(self.enemies[i])
            self.shootLaser.add_enemy(self.enemies[i])
            self.enemyShoot.add_enemy(self.enemies[i])

        #Dodavanje stitova
        self.shields = []
        self.shields.append(Shield())
        self.shields[0].setPos(50, 350)
        self.shields.append(Shield())
        self.shields[1].setPos(375, 350)
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

        self.initUI(self.numberOfPlayer, self.level_numberrr)
            
    def move_enemy(self, enemyPixMap: QGraphicsPixmapItem, newX, newY):
        enemyPixMap.setPos(newX, newY)

    def remove_enemy_label(self, enemy: QGraphicsPixmapItem):
        if enemy in self.enemies:
            self.enemies.remove(enemy)           
            

    def remove_laser(self, laserLabel: QGraphicsPixmapItem):
        if laser in self.enemies:
            self.enemies.remove(enemy)           
            self.enemyShoot.remove_enemy(enemy)   #Da ne pucaju kad su vec pogodjeni

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())

    # POKUSAJ PROCESA

    def do_key_press(self, key):
        try:
            # proc = multiprocessing.Process(target = self.__update_position__, args = [key])
            # proc.start()
            # proc.join()

            #(Process(target=__update_position__, args=[key])).start()

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
            self.shootLaser.remove_laser(laserLabel)
            self.shootLaser.remove_enemy(enemyLabel)
            self.remove_enemy_label(enemyLabel)        
            self.enemyShoot.remove_enemy(enemyLabel)
            self.moveEnemy.remove_enemy(enemyLabel)
            

            if len(self.enemies) == 1:                
                if (self.numberOfPlayer == 1):
                    
                    self.shootLaser.die()
                    self.moveEnemy.die()
                    self.enemyShoot.die()
                    self.key_notifier.die()
                    self.key_notifier.keys.clear()
                    self.view.hide()
                    self.next_level.emit(self.level_numberrr + 1)
                elif (self.numberOfPlayer == 2):
                    
                    self.shootLaser.die()
                    self.moveEnemy.die()
                    self.enemyShoot.die()
                    self.key_notifier.keys.clear()
                    self.key_notifier.die()
                    self.view.hide()
                    self.next_level2.emit(self.level_numberrr + 1)


        except Exception as e:
            print('Exception in Main_Thread/player_laser_enemy_collide method: ', str(e))

    def enemy_laser_shield_collide(self, laserLabel: QGraphicsPixmapItem, shieldLabel: QGraphicsPixmapItem):
        try:
            self.sound = QtMultimedia.QSound('assets/sounds/shipexplosion.wav')
            self.sound.play()
            self.enemyShoot.remove_laser(laserLabel)
            laserLabel.hide()
            
            for shield in self.shields:
                if shield == shieldLabel:
                    shield.makeDamage()
                    if shield.health <= 0:    
                        self.enemyShoot.remove_shield(shield)
                        self.shields.remove(shield)
                    shield.update_shield(shield)  
            
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

        if self.player == playerLabel:
            self.player.loseLevel()
            self.update_GUI_lives(1)
        if self.numberOfPlayer == 2:
            if self.player2 == playerLabel:
                self.player2.loseLevel()
                self.update_GUI_lives(2)

    def __update_position__(self, key):
        
        if self.player:
            playerPos = self.player.pos() 

            dx = 0         

            # Closing program    
            if key == Qt.Key_T:
                self.shootLaser.die()
                self.moveEnemy.die()
                self.enemyShoot.die()
                self.key_notifier.die()
                self.view.hide()

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

               
        ## player 2 ##
        if self.numberOfPlayer == 2 and self.player2:
            playerPos2 = self.player2.pos()
            dx2 = 0

            if playerPos2.x() + dx2 <= 0:
                if key == Qt.Key_Right:
                    dx2 += PLAYER_SPEED
            elif playerPos2.x() + dx2 >= 845:
                if key == Qt.Key_Left:
                    dx2 -= PLAYER_SPEED
            else:
                if key == Qt.Key_Right:
                    dx2 += PLAYER_SPEED
                if key == Qt.Key_Left:
                    dx2 -= PLAYER_SPEED
            self.player2.setPos(playerPos2.x()+dx2, playerPos2.y())

            if key == Qt.Key_L and self.player2:
                if self.playerTwoCanShoot:
                    laserLabel2 = Bullet()
                    self.player_shoot_laser(laserLabel2, playerPos2.x(), playerPos2.y())

    def initUI(self, numberOfPlayer, level_number):
        self.horizontalLayoutWidget = QWidget()
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(13, 10, 871, 10))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(150)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setAlignment(Qt.AlignLeft)

        #Zivoti prvog igraca
        self.lab_lives1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lab_lives1.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(QFont.Bold)
        self.lab_lives1.setFont(font)
        self.lab_lives1.setObjectName("lab_lives1")
        self.lab_lives1.setStyleSheet("color:yellow")
        self.horizontalLayout.addWidget(self.lab_lives1)

        self.lab_lives1.setText("Player1 Lives: 3")

        #Level
        self.lab_level = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lab_level.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lab_level.setFont(font)
        self.lab_level.setObjectName("lab_level")
        self.lab_level.setStyleSheet("color:yellow")
        self.horizontalLayout.addWidget(self.lab_level)

        self.lab_level.setText("Level: " + str(level_number))

        #Zivoti drugog igraca
        if self.numberOfPlayer==2:
            self.lab_lives2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
            self.lab_lives2.setEnabled(True)
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.lab_lives2.setFont(font)
            self.lab_lives2.setObjectName("lab_lives2")
            self.lab_lives2.setStyleSheet("color:yellow")
            self.horizontalLayout.addWidget(self.lab_lives2)

            self.lab_lives2.setText("Player2 Lives: 3")
        

        self.horizontalLayoutWidget.show()
        self.horizontalLayoutWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.Widget = self.addWidget(self.horizontalLayoutWidget)


    def update_GUI_lives(self,playerNo):
        if playerNo==1:
            lives=self.player.lives
           
            if lives==3:
                self.lab_lives1Text = "Player1 Lives: 3"
                self.lab_lives1.setText(self.lab_lives1Text)
            elif lives==2:
                self.lab_lives1Text = "Player1 Lives: 2"
                self.lab_lives1.setText(self.lab_lives1Text)
            elif lives==1:
                self.lab_lives1Text = "Player1 Lives: 1"
                self.lab_lives1.setText(self.lab_lives1Text)
            elif lives<=0:
                self.lab_lives1Text = "Player1 Lives: 0"
                self.lab_lives1.setText(self.lab_lives1Text)
                self.flag_playerOneDead=True
                self.player.hide()
                self.player = None

        if playerNo==2:
            lives=self.player2.lives

            if lives==3:
                self.lab_lives2Text = "Player2 Lives: 3"
                self.lab_lives2.setText(self.lab_lives2Text)
            elif lives==2:
                self.lab_lives2Text = "Player2 Lives: 2"
                self.lab_lives2.setText(self.lab_lives2Text)
            elif lives==1:
                self.lab_lives2Text = "Player2 Lives: 1"
                self.lab_lives2.setText(self.lab_lives2Text)
            elif lives<=0:
                self.lab_lives2Text = "Player2 Lives: 0"
                self.lab_lives2.setText(self.lab_lives2Text)
                self.flag_playerTwoDead=True
                self.player2.hide()
                self.player2 = None

        if self.numberOfPlayer==1:
            if self.flag_playerOneDead==True:
                self.gameOver()
        elif self.numberOfPlayer==2:
            if self.flag_playerOneDead==True and self.flag_playerTwoDead==True:
                self.gameOver()

    


    def gameOver(self):   

        self.tempWidget = QWidget()
        self.tempWidget.setGeometry(QtCore.QRect(0,0,900,600))
        self.tempWidget.setObjectName("tempWidget")

        self.horizontalLayout = QHBoxLayout(self.tempWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(230)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        #Labela game over
        self.lab_gameOver = QtWidgets.QLabel(self.tempWidget)
        self.lab_gameOver.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(60)
        font.setBold(True)
        font.setWeight(QFont.Bold)
        self.lab_gameOver.setFont(font)
        self.lab_gameOver.setObjectName("lab_gameOver")
        self.lab_gameOver.setStyleSheet("color: red; background-color: transparent;")
        self.horizontalLayout.addWidget(self.lab_gameOver)
        self.lab_gameOver.setText("GAME OVER")
        


        self.tempWidget.setStyleSheet("background-color: rgba(255,255,255,70);")

        self.Widget = self.addWidget(self.tempWidget)

        self.moveEnemy.die()
        self.shootLaser.die()
        self.enemyShoot.die()
        self.key_notifier.die()


        
        