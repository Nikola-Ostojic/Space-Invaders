import sys
from PyQt5 import QtWidgets
from main_window.Window import Window


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())