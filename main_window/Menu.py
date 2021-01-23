from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import *

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
class Menu(QWidget):

    playSignal = pyqtSignal()
    quitGameSignal = pyqtSignal()
    multiplaySignalSignal = pyqtSignal()

    def __init__(self):
        super(Menu, self).__init__()
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        #kreiranje labele za pozadinu
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 341, 441))
        self.label.setObjectName("label")

        #postavljanje gifa na labelu
        self.animated_bg=QMovie('./assets/stars.gif')
        self.animated_bg.setSpeed(100)
        self.label.setMovie(self.animated_bg)
        self.animated_bg.start()

        #Postavljanje logoa na vrh
        Name = QtWidgets.QLabel(self.centralwidget)
        Name.setGeometry(QtCore.QRect(68, 48, 199, 51))
        font = QtGui.QFont()
        font.setFamily("Poplar Std")
        font.setPointSize(31)
        font.setBold(True)
        font.setWeight(75)
        Name.setFont(font)
        Name.setStyleSheet("color: rgb(244, 255, 41)")
        Name.setAlignment(QtCore.Qt.AlignCenter)
        Name.setObjectName("Name")
        Name.setText("Space Invaders")
        Name_2 = QtWidgets.QLabel(self.centralwidget)
        Name_2.setGeometry(QtCore.QRect(15, 67, 199, 51))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        Name_2.setFont(font)
        Name_2.setStyleSheet("color: rgb(244, 255, 41)")
        Name_2.setAlignment(QtCore.Qt.AlignCenter)
        Name_2.setObjectName("Name_2")
        Name_2.setText("by D10S")
        

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(83, 167, 171, 201))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(32)
        self.verticalLayout.setObjectName("verticalLayout")


        play_button = QPushButton("Singleplayer", self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(play_button.sizePolicy().hasHeightForWidth())
        play_button.setSizePolicy(sizePolicy)
        play_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        play_button.setStyleSheet("background-color: rgba(0,0,0,50); border-style: outset; border-radius: 5px; border-color: beige; border-width: 1px  rgba(255,255,255,10); font: bold 12px; min-width: 10em; padding: 6px; color: white;")
        self.verticalLayout.addWidget(play_button)
        play_button.clicked.connect(self.play)


        multiplayer_button = QPushButton("Multiplayer", self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(multiplayer_button.sizePolicy().hasHeightForWidth())
        multiplayer_button.setSizePolicy(sizePolicy)
        multiplayer_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        multiplayer_button.setStyleSheet("background-color: rgba(0,0,0,50); border-style: outset; border-radius: 5px; border-color: beige; border-width: 1px  rgba(255,255,255,10); font: bold 12px; min-width: 10em; padding: 6px; color: white;")
        self.verticalLayout.addWidget(multiplayer_button)
        multiplayer_button.clicked.connect(self.playMultiplayer)


        quit_button = QPushButton("Quit", self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(quit_button.sizePolicy().hasHeightForWidth())
        quit_button.setSizePolicy(sizePolicy)
        quit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        quit_button.setStyleSheet("background-color: rgba(0,0,0,50); border-style: outset; border-radius: 5px; border-color: beige; border-width: 1px  rgba(255,255,255,10); font: bold 12px; min-width: 10em; padding: 6px; color: white;")
        self.verticalLayout.addWidget(quit_button)
        quit_button.clicked.connect(self.quit)
        

        print('prikazujem klasu Menu')


        self.show()


    def play(self):
        self.playSignal.emit()

    def playMultiplayer(self):
        self.multiplaySignalSignal.emit()

    def quit(self):
        self.quitGameSignal.emit()