import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QMimeData

from enums import *
import dragAndDrop
import function
import qdarkstyle

#form_class = uic.loadUiType("mainUI.ui")[0] # UI file

class mainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()
        uic.loadUi('mainUI.ui', self)
        self.forSpawn.setupUi(window= self.dropWindow, code= blockCode.FOR)
        self.classSpawn.setupUi(window= self.dropWindow, code= blockCode.CLASS)
        self.printSpawn.setupUi(window= self.dropWindow, code= blockCode.PRINT)
        self.whileSpawn.setupUi(window= self.dropWindow, code= blockCode.WHILE)
        #uic.setupUi(self)
        '''
        self.addBlock(0, 'sasdf', (300, 0))
        self.addBlock(0, 'sssss', (300, 100))
        self.addBlock(1, 'ddd', (300, 200))
        self.addBlock(2, 'ddd', (300, 300))
        self.addBlock(3, 'ddd', (300, 400))
        Function.printMom(self.centralwidget,self,blockCode.PRINT)
        a = Function.forMom(self.centralWidget(),self,blockCode.FOR)
        a. move(0,200)
        self.initWidget()
        self.forSpawn.title = "for"
        self.forSpawn.window = self
        self.forSpawn.code = blockCode.FOR'''

   


    

class dropPlace(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.blocks = []
        self.indentPos = []
        self._indentBlocks =  [blockCode.INDENT,blockCode.FOR,blockCode.CLASS]

    def getCode(self, block):
        s = str(type(block))
        if s == "<class 'dragAndDrop.indentBlock'>": return blockCode.INDENT
        elif s == "<class 'function.forBlk'>": return blockCode.FOR
        elif s == "<class 'dragAndDrop.block'>": return blockCode.BLOCK
        elif s == "<class 'function.printBlk'>": return blockCode.PRINT
        elif s == "<class 'dragAndDrop.varGetter'>": return blockCode.VARGET
        elif s == "<class 'dragAndDrop.base'>": return blockCode.BASE
        elif s == "<class 'function.classBlk'>": return blockCode.CLASS
        elif s == "<class 'function.whileBlk'>": return blockCode.WHILE
        return False

    def addBlock(self, blkCode, pos):
        if blkCode == blockCode.BLOCK:
            block = dragAndDrop.block(name,self.centralt,len(self.blocks))
        elif blkCode == blockCode.INDENT:
            block = dragAndDrop.indentBlock(name, self, len(self.blocks))
        elif blkCode == blockCode.PRINT:
            block = function.printBlk(self, len(self.blocks))
        elif blkCode == blockCode.FOR:
            block = function.forBlk(self, len(self.blocks))
        elif blkCode == blockCode.CLASS:
            block = function.classBlk(self, len(self.blocks))
        elif blkCode == blockCode.WHILE:
            block = function.whileBlk(self, len(self.blocks))
        else:
            raise(Exception)
        self.blocks.append(block)
        block.move(pos[0], pos[1])
        print(self.getCode(block))
        if self.getCode(block) in self._indentBlocks:
            self.indentPos.append([block.code, [self.mapFromGlobal(self.pos()).x(), self.mapFromGlobal(self.pos()).y()], block.depth])
        return block

    def initWidget(self):
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QDragEnterEvent):
        e.accept()

    #indentBlock과 자식 block까지 depth 설정
    def setDepth(self, blkCode, depth):
        self.blocks[blkCode].depth = depth
        for i in range(len(self.indentPos)):
            if self.indentPos[i][0] == blkCode:
                self.indentPos[i][2] = self.blocks[blkCode].depth
        for block in self.blocks[blkCode].blockList:
            if self.getCode(self.blocks[block]) in self._indentBlocks:
                self.setDepth(block, depth + 1)

    def setPos(self, blkCode, pos):
        for i in range(len(self.indentPos)):
            if self.indentPos[i][0] == blkCode:
                self.indentPos[i][1] = pos
        for i in range(len(self.blocks[blkCode].blockList)):
            if self.getCode(self.blocks[self.blocks[blkCode].blockList[i]]) in self._indentBlocks:
                self.setPos(self.blocks[blkCode].blockList[i], [pos[0] + 50, pos[1] + i * 50 + 50])

    def codeToPos(self, blkCode):
        for i in self.indentPos:
            if i[0] == blkCode:
                return i

    def superList(self, blkCode):
        par = self.blocks[blkCode]
        li = []
        while True:
            par = par.parent()
            #print(par.code)
            li.append(par.code)

            if self.codeToPos(par.code)[2] == 0: break
        #print(li)
        return li

    def ancestor(self, blkCode):
        #print(self.superList(blockCode))
        for i in self.superList(blkCode):
            if self.codeToPos(i)[2] == 0:
                return i
        return blkCode

    def maxDepthInIndent(self, blkCode):
        maxD = -1
        maxCode = self.ancestor(blkCode)
        print(self.ancestor(blkCode))
        print(self.blocks[self.ancestor(blkCode)].blockList)
        for i in self.blocks[self.ancestor(blkCode)].blockList:
            if not (self.getCode(self.blocks[i]) in self._indentBlocks):
                continue
            if self.codeToPos(i)[2] > maxD:
                maxD = self.codeToPos(i)[2]
                maxCode = self.codeToPos(i)[0]
        print(maxCode)
        return maxCode

    def dropEvent(self, e: QDropEvent):
        position = e.pos()
        # 보내온 데이터를 받기
        # 그랩 당시의 마우스 위치값을 함께 계산하여 위젯 위치 보정
        offset = e.mimeData().data("application/hotspot")
        x, y, code = offset.data().decode('utf-8').split()
        x, y, code = int(x), int(y), int(code)
        print(x,y,code)
        #BackGround 안에 drop했다면
        dropT = dropType.BACKGROUND 
        #드롭 위치를 포함하는 모든 indentBlock의 list
        inPos = []
        self.blocks[code].move(position - QPoint(x, y))
        for pos in self.indentPos:
            if pos[0] == code: continue
            if pos[1][0] <= e.pos().x() <= pos[1][0] + self.blocks[pos[0]].width() and pos[1][1] <= e.pos().y() <= pos[1][1] + self.blocks[pos[0]].height():
                inPos.append(pos)
                dropT = dropType.INDENT
        print(dropT,e.pos().x(),e.pos().y(),self.indentPos)
        if dropT == dropType.INDENT:
            maxDepth = -1
            maxPos = inPos[0]
            for pos in inPos:
                if pos[2] > maxDepth:
                    maxPos = pos
                    maxDepth = pos[2]
            if self.getCode(self.blocks[code].parent()) in self._indentBlocks:
                self.blocks[code].parent().blockList.remove(code)
            self.blocks[maxPos[0]].insertBlock(self.blocks[code], (e.pos().y() - maxPos[1][1]) // 50)
            self.blocks[code].setParent(self.blocks[maxPos[0]])
            self.blocks[maxPos[0]].blockList.insert((e.pos().y() - maxPos[1][1]) // 50, code)
            if self.getCode(self.blocks[code]) in self._indentBlocks:
                self.setDepth(code, self.blocks[code].parent().depth + 1)
                self.setPos(code, [self.codeToPos(self.blocks[code].parent().code)[1][0] + 50, self.codeToPos(self.blocks[code].parent().code)[1][1] + (e.pos().y() - maxPos[1][1]) // 50 * 50 + 50])

            else:
                self.blocks[maxPos[0]].setMinimumHeight(self.blocks[maxPos[0]].blockCount() * 50)
                self.blocks[maxPos[0]].setMaximumHeight(self.blocks[maxPos[0]].blockCount() * 50)
            #print(self.superList(int(code)))

            for supPos in self.superList(code):
                #print(supPos)
                tempH = self.blocks[supPos].height()
                tempW = self.blocks[supPos].width()
                if self.getCode(self.blocks[code]) in self._indentBlocks:
                    self.blocks[supPos].setMinimumHeight(tempH + self.blocks[code].blockCount() * 50 + 50)
                    self.blocks[supPos].setMaximumHeight(tempH + self.blocks[code].blockCount() * 50 + 50)
                else:
                    self.blocks[supPos].setMinimumHeight(tempH + 50)
                    self.blocks[supPos].setMaximumHeight(tempH + 50)
                #print(maxDepth)
                #print(self.codeToPos(supPos))
                #print(250 + (maxDepth - self.codeToPos(int(code))[2]) * 50 + 50)
                if supPos == self.maxDepthInIndent(code):
                    self.blocks[supPos].setMinimumWidth(250 + (maxDepth - self.codeToPos(supPos)[2]) * 50 + 50)
                    self.blocks[supPos].setMaximumWidth(250 + (maxDepth - self.codeToPos(supPos)[2]) * 50 + 50)

        elif dropT == dropType.BACKGROUND:
            if self.getCode(self.blocks[code].parent()) in self._indentBlocks:
                self.blocks[code].parent().blockList.remove(code)
                if self.getCode(self.blocks[code]) in self._indentBlocks:
                    self.setDepth(code, 0)
                self.blocks[code].parent().setMinimumHeight(self.blocks[code].parent().blockCount() * 50 + 50)
                self.blocks[code].parent().setMaximumHeight(self.blocks[code].parent().blockCount() * 50 + 50)
            self.blocks[code].setParent(self)
            if self.getCode(self.blocks[code]) in self._indentBlocks:
                for i in range(len(self.indentPos)):
                    self.setDepth(code, 0)
                    self.setPos(code, [self.blocks[code].geometry().x(), self.blocks[code].geometry().y()])
        elif dropT == dropType.VARGET:
            pass
        else:
            raise (Exception)

        self.blocks[code].setVisible(True)

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    myWindow = mainWindow() 
    myWindow.show()
    app.exec_()