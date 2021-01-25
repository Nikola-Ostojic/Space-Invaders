import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt 

from main_window.Window import Window
from main_window.Menu import Menu

# Menu settings

class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = None
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainMenu = Menu()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(341)
        self.setFixedHeight(441)

        

        #print('Pozvan konstruktor menu')
        self.menu()



    def menu(self):   

        self.mainMenu.playSignal.connect(self.playGame)
        self.mainMenu.quitGameSignal.connect(self.quit)

        self.mainMenu.multiplaySignalSignal.connect(self.playMultiplayer)

        self.centralWidget.addWidget(self.mainMenu)
        self.centralWidget.setCurrentWidget(self.mainMenu)

        self.resize(580, 500)

        self.mainMenu.show()


    def playMultiplayer(self):
        self.game = Window(2)       


    def quit(self):
        sys.exit()

    def playGame(self):
        self.game = Window(1)
        self.game.close.connect(self.close)

    def close(self):
        self.game = []
        #self.game.close()

    # self.game.shootLaser.die()
    # self.game.moveEnemy.die()
    # self.game.enemyShoot.die()
    # self.key_notifier.die()