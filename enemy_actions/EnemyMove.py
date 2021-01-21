class Move(QGraphicsPixmapItem):
    def __init__(self):
        self.threadWorking = True
        self.thread = QThread()
        self.thread.started.connect(self.__move__)

    def start(self):
        self.thread.start()

    def die(self):
        self.threadWorking = False
        self.thread.quit()

#Kretanje neprijatelja
    def __move__(self):

        self.goRight = True
        self.goLeft = False

        while self.threadWorking:

            if self.goRight:
                for i in range(0, 33):
                    self.enemies[i].setPos(enemies[i - 1].x(), enemies[i - 1].y() + 50)               
                    if i == 11 && enemies[i].y() > 849:
                        for i in range(0, 33):
                            self.enemies[i].x() + 50
                        self.goRight = False
                        self.goLeft = True

            elif self.goLeft:
                for i in range(0, 33):
                    self.enemies[i].setPos(enemies[i - 1].x(), enemies[i - 1].y() - 50)               
                    if i == 11 && enemies[i].y() < 49:
                        for i in range(0, 33):
                            self.enemies[i].x() + 50
                        self.goRight = True
                        self.goLeft = False
            time.sleep(0.7)



