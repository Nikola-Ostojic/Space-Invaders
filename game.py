import sys
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush
WINDOW_WIDTH = 600
WINDOW_HEIGTH = 800


class Player(QtWidgets.QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setPixmap(QPixmap('assets/ship.png').scaled(50, 50))
        
        

        
    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_A):
            self.move(self.x() - 30, self.y()())
        elif (event.key() == QtCore.Qt.Key_D):
            self.move(self.x() + 30, self.y())
        else:
            QtWidgets.QLabel.keyPressEvent(self, event)






class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Space Invaders')
        self.window_width = WINDOW_WIDTH
        self.window_heigth = WINDOW_HEIGTH
        self.setGeometry(100,100,self.window_width, self.window_heigth)
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.player = Player()
        layout.addWidget(self.player)

        
        
        background = QImage('assets/background.png')
        background = background.scaled(WINDOW_WIDTH, WINDOW_HEIGTH)
        pallete = QPalette()
        pallete.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(pallete)

        #self.player.setFocus()







if __name__ == '__main__':


    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()


    sys.exit(app.exec_())