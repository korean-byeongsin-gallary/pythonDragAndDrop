import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QMimeData

import dragAndDrop
import Function
import qdarkstyle

form_class = uic.loadUiType("mainUI.ui")[0] # UI file

class mainWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.blocks = []
        self.indentPos = []
        '''
        self.addBlock(0, 'sasdf', (300, 0))
        self.addBlock(0, 'sssss', (300, 100))
        self.addBlock(1, 'ddd', (300, 200))
        self.addBlock(2, 'ddd', (300, 300))
        self.addBlock(3, 'ddd', (300, 400))
        '''
        Function.printMom(self.centralwidget,self)
        Function.forMom(self.centralWidget(),self)
        self.initWidget()

    def isIndent(self, block):
        if str(type(block)) in ["<class 'dragAndDrop.indentBlock'>", "<class 'Function.forBlk'>"]: return True
        return False

    def addBlock(self, blkCode, name, pos):
        if blkCode == 0:
            block = dragAndDrop.block(name,self.centralwidget,len(self.blocks))
        elif blkCode == 1:
            block = dragAndDrop.indentBlock(name, self.centralwidget, len(self.blocks))
        elif blkCode == 2:
            block = Function.printBlk(self.centralwidget, len(self.blocks))
        elif blkCode == 3:
            block = Function.forBlk(self.centralwidget, len(self.blocks))
        self.blocks.append(block)
        block.move(pos[0], pos[1])
        if self.isIndent(block):
            self.indentPos.append([block.code, [self.mapFromGlobal(self.pos()).x(), self.mapFromGlobal(self.pos()).y()], block.depth])
        return block

    def initWidget(self):
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QDragEnterEvent):
        e.accept()

    #indentBlock과 자식 block까지 depth 설정
    def setDepth(self, blockCode, depth):
        self.blocks[blockCode].depth = depth
        for i in range(len(self.indentPos)):
            if self.indentPos[i][0] == blockCode:
                self.indentPos[i][2] = self.blocks[blockCode].depth
        for block in self.blocks[blockCode].blockList:
            if self.isIndent(self.blocks[block]):
                self.setDepth(block, depth + 1)

    def setPos(self, blockCode, pos):
        for i in range(len(self.indentPos)):
            if self.indentPos[i][0] == blockCode:
                self.indentPos[i][1] = pos
        for i in range(len(self.blocks[blockCode].blockList)):
            if self.isIndent(self.blocks[self.blocks[blockCode].blockList[i]]):
                self.setPos(self.blocks[blockCode].blockList[i], [pos[0] + 50, pos[1] + i * 50 + 50])

    def codeToPos(self, blockCode):
        for i in self.indentPos:
            if i[0] == blockCode:
                return i

    def superList(self, blockCode):
        par = self.blocks[blockCode]
        li = []
        while True:
            par = par.parent()
            #print(par.code)
            li.append(par.code)

            if self.codeToPos(par.code)[2] == 0: break
        #print(li)
        return li

    def ancestor(self, blockCode):
        #print(self.superList(blockCode))
        for i in self.superList(blockCode):
            if self.codeToPos(i)[2] == 0:
                return i
        return blockCode

    def maxDepthInIndent(self, blockCode):
        maxD = -1
        maxCode = self.ancestor(blockCode)
        print(self.ancestor(blockCode))
        print(self.blocks[self.ancestor(blockCode)].blockList)
        for i in self.blocks[self.ancestor(blockCode)].blockList:
            if not self.isIndent(self.blocks[i]):
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
        #BackGround 안에 drop했다면
        BGDrop = True
        #드롭 위치를 포함하는 모든 indentBlock의 list
        inPos = []
        #드롭 위치를 포함하는 indentBlock이 있는지
        isIn = False
        self.blocks[int(code)].move(position - QPoint(int(x), int(y)))
        for pos in self.indentPos:
            if pos[0] == int(code): continue


            if pos[1][0] <= e.pos().x() <= pos[1][0] + self.blocks[pos[0]].width() and pos[1][1] <= e.pos().y() <= pos[1][1] + self.blocks[pos[0]].height():
                inPos.append(pos)
                isIn = True
        if isIn:
            maxDepth = -1
            maxPos = inPos[0]
            for pos in inPos:
                if pos[2] > maxDepth:
                    maxPos = pos
                    maxDepth = pos[2]

            if self.isIndent(self.blocks[int(code)].parent()):
                self.blocks[int(code)].parent().blockList.remove(int(code))
            self.blocks[maxPos[0]].insertBlock(self.blocks[int(code)], (e.pos().y() - maxPos[1][1]) // 50)
            self.blocks[int(code)].setParent(self.blocks[maxPos[0]])
            self.blocks[maxPos[0]].blockList.insert((e.pos().y() - maxPos[1][1]) // 50, int(code))
            if self.isIndent(self.blocks[int(code)]):
                self.setDepth(int(code), self.blocks[int(code)].parent().depth + 1)
                self.setPos(int(code), [self.codeToPos(self.blocks[int(code)].parent().code)[1][0] + 50, self.codeToPos(self.blocks[int(code)].parent().code)[1][1] + (e.pos().y() - maxPos[1][1]) // 50 * 50 + 50])

            else:
                self.blocks[maxPos[0]].setMinimumHeight(self.blocks[maxPos[0]].blockCount() * 50)
                self.blocks[maxPos[0]].setMaximumHeight(self.blocks[maxPos[0]].blockCount() * 50)
            #print(self.superList(int(code)))

            for supPos in self.superList(int(code)):
                #print(supPos)
                tempH = self.blocks[supPos].height()
                tempW = self.blocks[supPos].width()
                if self.isIndent(self.blocks[int(code)]):
                    self.blocks[supPos].setMinimumHeight(tempH + self.blocks[int(code)].blockCount() * 50 + 50)
                    self.blocks[supPos].setMaximumHeight(tempH + self.blocks[int(code)].blockCount() * 50 + 50)
                else:
                    self.blocks[supPos].setMinimumHeight(tempH + 50)
                    self.blocks[supPos].setMaximumHeight(tempH + 50)
                #print(maxDepth)
                #print(self.codeToPos(supPos))
                #print(250 + (maxDepth - self.codeToPos(int(code))[2]) * 50 + 50)
                if supPos == self.maxDepthInIndent(int(code)):
                    self.blocks[supPos].setMinimumWidth(250 + (maxDepth - self.codeToPos(supPos)[2]) * 50 + 50)
                    self.blocks[supPos].setMaximumWidth(250 + (maxDepth - self.codeToPos(supPos)[2]) * 50 + 50)

            BGDrop = False

        if BGDrop:
            if self.isIndent(self.blocks[int(code)].parent()):
                self.blocks[int(code)].parent().blockList.remove(int(code))
                if self.isIndent(self.blocks[int(code)]):
                    self.setDepth(int(code), 0)
                self.blocks[int(code)].parent().setMinimumHeight(self.blocks[int(code)].parent().blockCount() * 50 + 50)
                self.blocks[int(code)].parent().setMaximumHeight(self.blocks[int(code)].parent().blockCount() * 50 + 50)
            self.blocks[int(code)].setParent(self.centralwidget)
            if self.isIndent(self.blocks[int(code)]):
                for i in range(len(self.indentPos)):
                    self.setDepth(int(code), 0)
                    self.setPos(int(code), [self.blocks[int(code)].geometry().x(), self.blocks[int(code)].geometry().y()])

        self.blocks[int(code)].setVisible(True)

        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    myWindow = mainWindow() 
    myWindow.show()
    app.exec_()