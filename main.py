import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QMimeData

import dragAndDrop

form_class = uic.loadUiType("mainUI.ui")[0] # UI file

class mainWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.blocks = list()
        self.addBlock('sasdf',(50,500))
        self.addBlock('sssss',(30,30))
        dragAndDrop.blockSpawn('asdf',self.centralwidget,self)
        self.initWidget()
    
    def addBlock(self,name,pos):
        block = dragAndDrop.block(name,self.centralwidget,len(self.blocks))
        self.blocks.append(block)
        block.move(pos[0],pos[1])
        return block
        

    def initWidget(self):
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QDragEnterEvent):
        e.accept()

    def dropEvent(self, e: QDropEvent):
        position = e.pos()
        # 보내온 데이터를 받기
        # 그랩 당시의 마우스 위치값을 함께 계산하여 위젯 위치 보정
        offset = e.mimeData().data("application/hotspot")
        x, y, code = offset.data().decode('utf-8').split() 
        self.blocks[int(code)].move(position - QPoint(int(x), int(y)))
        self.blocks[int(code)].setVisible(True)

        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = mainWindow() 
    myWindow.show()
    app.exec_()