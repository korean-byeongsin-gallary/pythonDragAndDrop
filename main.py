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
        #self.addBlock('asdf', (0, 0))
        '''
        self.addBlock(0, 'sasdf', (300, 0))
        self.addBlock(0, 'sssss', (300, 100))
        self.addBlock(1, 'ddd', (300, 200))
        self.addBlock(2, 'ddd', (300, 300))
        self.addBlock(3, 'ddd', (300, 400))
        '''
        #print(self.blocks)
        #dragAndDrop.blockSpawn('asdf',self.centralwidget,self)
        Function.printMom(self.centralwidget,self)
        Function.forMom(self.centralWidget(),self)
        #print(type(self.blocks[1]))
        self.initWidget()
        print(type(self.centralWidget()))


    #def indentPos(self):
     #   return self.indentPos()
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
            #print(self.indentPos)
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
            print(par.code)
            li.append(par.code)
            print(li)
            if self.codeToPos(par.code)[2] == 0: break
        return li



    def dropEvent(self, e: QDropEvent):
        position = e.pos()
        #print(e.pos().x(), e.pos().y())
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
        #print("*", e.pos().x(), e.pos().y())
        #print(self.indentPos)
        self.blocks[int(code)].move(position - QPoint(int(x), int(y)))
        #print(self.blocks[int(code)].geometry().x())

        #print(self.indentPos)
        for pos in self.indentPos:
            #print(pos)
            #print(-pos[1][0], -pos[1][0] + self.blocks[pos[0]].width(), -pos[1][1], -pos[1][1] + self.blocks[pos[0]].height())
            if pos[0] == int(code): continue


            if pos[1][0] <= e.pos().x() <= pos[1][0] + self.blocks[pos[0]].width() and pos[1][1] <= e.pos().y() <= pos[1][1] + self.blocks[pos[0]].height():
                print("***")
                inPos.append(pos)
                isIn = True
        #print(self.indentPos)
        if isIn:
            print("*", inPos)
            maxDepth = -1
            maxPos = inPos[0]
            for pos in inPos:
                if pos[2] > maxDepth:
                    maxPos = pos
                    maxDepth = pos[2]



            if self.isIndent(self.blocks[int(code)].parent()):
                self.blocks[int(code)].parent().blockList.remove(int(code))
                #print(self.blocks[maxPos[0]].blockList)
            self.blocks[maxPos[0]].insertBlock(self.blocks[int(code)], (e.pos().y() - maxPos[1][1]) // 50)
            self.blocks[int(code)].setParent(self.blocks[maxPos[0]])
            #print(self.blocks[int(code)].parent())
            print("**************")
            # print(e.pos().y(), pos[1][1], (e.pos().y() - pos[1][1]) // 50)
            self.blocks[maxPos[0]].blockList.insert((e.pos().y() - maxPos[1][1]) // 50, int(code))
            #print(self.blocks[maxPos[0]].blockList)
            # print("**************")
            if self.isIndent(self.blocks[int(code)]):
                self.setDepth(int(code), self.blocks[int(code)].parent().depth + 1)
                #print("***")
                print([self.codeToPos(self.blocks[int(code)].parent().code)[1][0] + 50, self.codeToPos(self.blocks[int(code)].parent().code)[1][1] + (e.pos().y() - maxPos[1][1]) // 50 * 50 + 50])
                self.setPos(int(code), [self.codeToPos(self.blocks[int(code)].parent().code)[1][0] + 50, self.codeToPos(self.blocks[int(code)].parent().code)[1][1] + (e.pos().y() - maxPos[1][1]) // 50 * 50 + 50])
                #print("***")

                #self.blocks[maxPos[0]].setMinimumHeight(self.blocks[maxPos[0]].blockCount() * 50 + self.blocks[int(code)].blockCount() * 50 + 50)
                #self.blocks[maxPos[0]].setMaximumHeight(self.blocks[maxPos[0]].blockCount() * 50 + self.blocks[int(code)].blockCount() * 50 + 50)
                print(self.blocks[int(code)].parent().depth)


            else:
                self.blocks[maxPos[0]].setMinimumHeight(self.blocks[maxPos[0]].blockCount() * 50 + 50)
                self.blocks[maxPos[0]].setMaximumHeight(self.blocks[maxPos[0]].blockCount() * 50 + 50)

            print(self.superList(int(code)))

            for supPos in self.superList(int(code)):
                temp = self.blocks[supPos].height()
                if self.isIndent(self.blocks[int(code)]):
                    self.blocks[supPos].setMinimumHeight(temp + self.blocks[int(code)].blockCount() * 50 + 50)
                    self.blocks[supPos].setMaximumHeight(temp + self.blocks[int(code)].blockCount() * 50 + 50)
                    self.blocks[supPos].setMinimumWidth(temp + self.blocks[int(code)].width())
                    self.blocks[supPos].setMaximumWidth(temp + self.blocks[int(code)].width())
                else:
                    self.blocks[supPos].setMinimumHeight(temp + 50)
                    self.blocks[supPos].setMaximumHeight(temp + 50)


            # print("**************")
            print(self.indentPos)

            BGDrop = False


        if BGDrop:
            #print("**********")
            if self.isIndent(self.blocks[int(code)].parent()):
                #print("***")
                self.blocks[int(code)].parent().blockList.remove(int(code))
                #print("***")
                print(self.blocks[int(code)].parent().blockList)
                #print("***")
                if self.isIndent(self.blocks[int(code)]):
                    self.setDepth(int(code), 0)
                self.blocks[int(code)].parent().setMinimumHeight(self.blocks[int(code)].parent().blockCount() * 50 + 50)
                self.blocks[int(code)].parent().setMaximumHeight(self.blocks[int(code)].parent().blockCount() * 50 + 50)
            self.blocks[int(code)].setParent(self.centralwidget)
            #print(self.indentPos)
            #self.blocks[int(code)].move(position - QPoint(int(x), int(y)))
            #
            #print(self.indentPos)
            if self.isIndent(self.blocks[int(code)]):
                #print("***", int(code))
                for i in range(len(self.indentPos)):
                    self.setDepth(int(code), 0)
                    self.setPos(int(code), [self.blocks[int(code)].geometry().x(), self.blocks[int(code)].geometry().y()])
            print(self.indentPos)
                #print(self.window.indentPos)


        self.blocks[int(code)].setVisible(True)
        #print(self.blocks[2].codeSpace.itemAt(0))


        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = mainWindow() 
    myWindow.show()
    app.exec_()