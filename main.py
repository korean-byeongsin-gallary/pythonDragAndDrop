import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QMimeData

import dragAndDrop

form_class = uic.loadUiType("mainUI.ui")[0] # UI file

def str_to_class(str):
    return eval(str)

class mainWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.blc = dragAndDrop.block('sasdf',self.centralwidget)
        self.blc2 = dragAndDrop.block('sssss',self.centralwidget)
        #self.blcs = dragAndDrop.blockSpawn(dragAndDrop.block('sssss',self.centralwidget),self.centralWidget)
        self.initWidget()
    
    def initWidget(self):
        self.setAcceptDrops(True)
        self.blc.move(20,20)

    def dragEnterEvent(self, e: QDragEnterEvent):
        e.accept()

    def dropEvent(self, e: QDropEvent):
        position = e.pos()
        print(e.parent)
        # 보내온 데이터를 받기
        # 그랩 당시의 마우스 위치값을 함께 계산하여 위젯 위치 보정
        offset = e.mimeData().data("application/hotspot")
        x, y = offset.data().decode('utf-8').split() 
        self.blc.move(position - QPoint(int(x), int(y)))

        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = mainWindow() 
    myWindow.show()
    app.exec_()