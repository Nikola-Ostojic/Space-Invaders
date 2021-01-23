import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStackedWidget

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
        print('Pozvan konstruktor menu')
        self.menu()



    def menu(self):
        self.mainMenu.playSignal.connect(self.playGame)
        self.mainMenu.quitGameSignal.connect(self.quit)

        self.mainMenu.multiplaySignalSignal.connect(self.playMultiplayer)

        self.centralWidget.addWidget(self.mainMenu)
        self.centralWidget.setCurrentWidget(self.mainMenu)

        self.resize(580, 500)


    def playMultiplayer(self):
        self.game = Window(2)       


    def quit(self):
        sys.exit()

    def playGame(self):
        self.game = Window(1)




