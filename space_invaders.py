import sys

from PyQt5.QtWidgets import QApplication

from game import Game

class space_invaders():
    def __init__(self):
        self.game = Game()
        self.game.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    newGame = space_invaders()

    sys.exit(app.exec_())
    