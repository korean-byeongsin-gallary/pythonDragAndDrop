import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QMimeData

import dragAndDrop
import Function

form_class = uic.loadUiType("mainUI.ui")[0] # UI file

class mainWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.blocks = []
        self.indentPos = []
        self.maxWidthBlocks = []
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
        blkW = self.blocks[int(code)].width()
        blkH = self.blocks[int(code)].height()
        for pos in self.indentPos:
            if pos[0] == int(code): continue
            if pos[1][0] <= e.pos().x() <= pos[1][0] + self.blocks[pos[0]].width() and pos[1][1] <= e.pos().y() <= pos[1][1] + self.blocks[pos[0]].height():
                inPos.append(pos)
                isIn = True
        if isIn:
            maxDepth = -1 # 드롭 위치를 포함하는 indentBlock 중 가장 큰 Depth
            maxPos = inPos[0] # 드롭 위치를 포함하는 indentBlock 중 가장 큰 Depth를 가진 inDentBlock의 Pos
            #maxPos, MaxDepth 정하기
            for pos in inPos:
                if pos[2] > maxDepth:
                    maxPos = pos
                    maxDepth = pos[2]
            # 그 전 부모에게서 드롭한 블록을 제거, 그에 따른 크기 조정

            if self.isIndent(self.blocks[int(code)].parent()):
                self.blocks[int(code)].parent().blockList.remove(int(code))
                for supPos in self.superList(int(code)):
                    tempH = self.blocks[supPos].height()
                    self.blocks[supPos].setMinimumHeight(tempH - blkH)
                    self.blocks[supPos].setMaximumHeight(tempH - blkH)
            #가장 깊은 depth을 가진 indentBlock의 blockList에 insert, 그 후 새로운 부모로 설정
            self.blocks[maxPos[0]].insertBlock(self.blocks[int(code)], (e.pos().y() - maxPos[1][1]) // 50)
            self.blocks[int(code)].setParent(self.blocks[maxPos[0]])
            self.blocks[maxPos[0]].blockList.insert((e.pos().y() - maxPos[1][1]) // 50, int(code))
            #드롭한 블록이 indentBlock이라면 Depth을 새 부모의 Depth + 1 로 설정, Pos도 그에 따라 설정
            if self.isIndent(self.blocks[int(code)]):
                self.setDepth(int(code), self.blocks[int(code)].parent().depth + 1)
                self.setPos(int(code), [self.codeToPos(self.blocks[int(code)].parent().code)[1][0] + 50, self.codeToPos(self.blocks[int(code)].parent().code)[1][1] + (e.pos().y() - maxPos[1][1]) // 50 * 50 + 50])
            #부모의 조상까지 걸쳐 올라가면서 Width를 증가시킴
            for supPos in self.superList(int(code)):
                tempH = self.blocks[supPos].height()
                tempW = self.blocks[supPos].width()
                self.blocks[supPos].setMinimumHeight(tempH + blkH)
                self.blocks[supPos].setMaximumHeight(tempH + blkH)
                print(tempW, blkW + (maxPos[2] - self.codeToPos(supPos)[2]) * 50 + 50)
                self.blocks[supPos].setMinimumWidth(max(tempW, blkW + (maxPos[2] - self.codeToPos(supPos)[2]) * 50 + 50))
                self.blocks[supPos].setMaximumWidth(max(tempW, blkW + (maxPos[2] - self.codeToPos(supPos)[2]) * 50 + 50))
                #가장 큰 너비를 가지는 block
                #if self.codeToPos(supPos)[2] == 0 and tempW < blkW + (maxPos[2] - self.codeToPos(supPos)[2]) * 50 + 50:



            BGDrop = False

        if BGDrop:
            if self.isIndent(self.blocks[int(code)].parent()):
                self.blocks[int(code)].parent().blockList.remove(int(code))
                for supPos in self.superList(int(code)):
                    tempH = self.blocks[supPos].height()
                    self.blocks[supPos].setMinimumHeight(tempH - blkH)
                    self.blocks[supPos].setMaximumHeight(tempH - blkH)
                if self.isIndent(self.blocks[int(code)]):
                    self.setDepth(int(code), 0)
                #여기에 뺄 때 크기 줄어드는 코드 완성하기
            self.blocks[int(code)].setParent(self.centralwidget)
            if self.isIndent(self.blocks[int(code)]):
                self.setDepth(int(code), 0)
                self.setPos(int(code), [self.blocks[int(code)].geometry().x(), self.blocks[int(code)].geometry().y()])

        self.blocks[int(code)].setVisible(True)

        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = mainWindow() 
    myWindow.show()
    app.exec_()