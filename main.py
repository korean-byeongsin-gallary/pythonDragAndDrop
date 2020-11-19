import sys, sip
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from save import *

from PyQt5.QtCore import QMimeData

import blockDrag

form_class = uic.loadUiType("mainUI.ui")[0] # UI file

class mainWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.blocks = list()
        self.addBlock('sasdf',(50,500))
        self.addBlock('sssss',(30,30))
        self.delBlock(1)
        blockDrag.blockSpawn('asdf',self.centralwidget,self)
        tr = blockDrag.TrashCan(self.centralwidget,self)
        tr.move(300,300)
        self.initWidget()
        self.countBlock = 0
        self.btnSave.clicked.connect(self.sv)
        self.btnLoad.clicked.connect(self.ld)
    
    def addBlock(self,name,pos):
        block = blockDrag.block(name,self.centralwidget,len(self.blocks))
        self.blocks.append(block)
        block.move(pos[0],pos[1])
        return block
    
    def delBlock(self,code):
        self.blocks[code].delelted = True
        self.blocks[code].deleteLater()

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
    
    def sv(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', "","Python Drag and Drop Files(*.pydrag)")
        save(self.blocks,fname[0])
    
    def ld(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', "",
                                            "All Files(*);; Python Drag and Drop Files(*.pydrag)")
        loadBlocks = load(fname[0])
        print(loadBlocks)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = mainWindow() 
    myWindow.show()
    app.exec_()