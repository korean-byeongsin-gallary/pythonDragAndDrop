import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QMimeData

from enums import *
import dragAndDrop
import Function
import qdarkstyle

#form_class = uic.loadUiType("mainUI.ui")[0] # UI file

def loadStyle(path):
    with open(path,'r') as fh:
        return fh.read()

class mainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()
        uic.loadUi('mainUI.ui', self)
        self.forSpawn.setupUi(window= self.dropWindow, code= blockCode.FOR)
        self.classSpawn.setupUi(window= self.dropWindow, code= blockCode.CLASS)
        self.printSpawn.setupUi(window= self.dropWindow, code= blockCode.PRINT)
        self.whileSpawn.setupUi(window= self.dropWindow, code= blockCode.WHILE)
        self.ifSpawn.setupUi(window= self.dropWindow, code= blockCode.IF)
        self.operSpawn.setupUi(window= self.dropWindow, code= blockCode.OPER)
        self.defSpawn.setupUi(window=self.dropWindow, code=blockCode.DEF)
        self.returnSpawn.setupUi(window=self.dropWindow, code=blockCode.RETURN)

        self.finalCode = ""
        self.codeDialog = QDialog()
        self.actionTo_code.triggered.connect(self.dialog_open)
        self.actionsave.triggered.connect(self.codeSave)
        self.actionRUN.triggered.connect(self.runCode)
        self.actionDelete_all.triggered.connect(self.deleteAll)

        self.setFixedSize(1600, 960)

    def dialog_open(self):

        self.finalCode = self.dropWindow.finalCode()
        self.showTheThing = QLabel(self.finalCode, self.codeDialog)
        self.codeDialog.setWindowTitle('Result Code')
        self.codeDialog.setWindowModality(Qt.ApplicationModal)
        self.codeDialog.resize(480, 640)
        self.codeDialog.show()

    def codeSave(self):
        file = open("save.txt", 'w')
        self.finalCode = self.dropWindow.finalCode()
        file.write(self.finalCode)

    def runCode(self):
        self.finalCode = self.dropWindow.finalCode()
        exec(self.finalCode)

    def deleteAll(self):
        for i in self.dropWindow.blocks:
            i.setParent(None)
        self.dropWindow.blocks = []


class dropPlace(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.blocks = []
        self.indentPos = []
        #self.start = False
        self._indentBlocks =  [blockCode.INDENT, blockCode.FOR, blockCode.CLASS, blockCode.WHILE, blockCode.IF, blockCode.DEF]
        # self.trashCan = QWidget(self)
        # self.trashCan.setMaximumWidth(100)
        # self.trashCan.setMinimumWidth(100)
        # self.trashCan.setMaximumHeight(100)
        # self.trashCan.setMinimumHeight(100)
        # self.trashCan.setStyleSheet(loadStyle("styles/trashCan.qss"))
        # self.trashCan.move(QPoint(1000, 800))
        # self.trashCan.setVisible(True)

    def getCode(self, block):
        s = str(type(block))
        if s == "<class 'dragAndDrop.indentBlock'>": return blockCode.INDENT
        elif s == "<class 'Function.forBlk'>": return blockCode.FOR
        elif s == "<class 'dragAndDrop.block'>": return blockCode.BLOCK
        elif s == "<class 'Function.printBlk'>": return blockCode.PRINT
        elif s == "<class 'dragAndDrop.varGetter'>": return blockCode.VARGET
        elif s == "<class 'dragAndDrop.base'>": return blockCode.BASE
        elif s == "<class 'Function.classBlk'>": return blockCode.CLASS
        elif s == "<class 'Function.whileBlk'>": return blockCode.WHILE
        elif s == "<class 'Function.ifBlk'>": return blockCode.IF
        elif s == "<class 'Function.operBlk'>": return blockCode.OPER
        elif s == "<class 'Function.defBlk'>": return blockCode.DEF
        elif s == "<class 'Function.returnBlk'>": return blockCode.RETURN
        return False

    def addBlock(self, blkCode, pos):
        if blkCode == blockCode.BLOCK:
            block = dragAndDrop.block(name,self.centralt,len(self.blocks))
        elif blkCode == blockCode.INDENT:
            block = dragAndDrop.indentBlock(name, self, len(self.blocks))
        elif blkCode == blockCode.PRINT:
            block = Function.printBlk(self, len(self.blocks))
        elif blkCode == blockCode.FOR:
            block = Function.forBlk(self, len(self.blocks))
        elif blkCode == blockCode.CLASS:
            block = Function.classBlk(self, len(self.blocks))
        elif blkCode == blockCode.WHILE:
            block = Function.whileBlk(self, len(self.blocks))
        elif blkCode == blockCode.IF:
            block = Function.ifBlk(self, len(self.blocks))
        elif blkCode == blockCode.OPER:
            block = Function.operBlk(self, len(self.blocks))
        elif blkCode == blockCode.DEF:
            block = Function.defBlk(self, len(self.blocks))
        elif blkCode == blockCode.RETURN:
            block = Function.returnBlk(self, len(self.blocks))
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

    def BGBlocksSortByHeight(self):
        a = []
        for blk in self.blocks:
            if blk.parent() == self:
                if a == []:
                    a.append(blk.code)
                elif self.blocks[a[0]].y() > blk.y():
                    a.insert(0, blk.code)
                elif self.blocks[a[-1]].y() < blk.y():
                    a.insert(len(a), blk.code)
                else:
                    for i in range(len(a) - 1):
                        if self.blocks[a[i]].y() <= blk.y() <= self.blocks[a[i + 1]].y():
                            a.insert(i + 1, blk.code)
        return a

    def toCode(self, blockList, depth):
        codeText = ""
        for blkC in blockList:
            BGblk = self.blocks[blkC]
            if self.getCode(BGblk) in self._indentBlocks:
                codeText += "    " * depth + BGblk.text + '\n'
                codeText += self.toCode(BGblk.blockList, depth + 1)
            else:
                codeText += "    " * depth + BGblk.text + '\n'
        return codeText

    def finalCode(self):
        return self.toCode(self.BGBlocksSortByHeight(), 0)

    def dropEvent(self, e: QDropEvent):
        #self.start = True
        position = e.pos()
        # 보내온 데이터를 받기
        # 그랩 당시의 마우스 위치값을 함께 계산하여 위젯 위치 보정
        offset = e.mimeData().data("application/hotspot")
        x, y, code = offset.data().decode('utf-8').split()
        x, y, code = int(x), int(y), int(code)
        #print(x,y,code)
        #BackGround 안에 drop했다면
        dropT = dropType.BACKGROUND 
        #드롭 위치를 포함하는 모든 indentBlock의 list
        inPos = []
        self.blocks[code].move(position - QPoint(x, y))
        blkW = self.blocks[int(code)].width()
        blkH = self.blocks[int(code)].height()
        #print(e.pos().x(), e.pos().y())
        # if  1000 < e.pos().x() < 1100 and 800 < e.pos().y() < 900 :
        #     self.blocks[int(code)].setParent(None)
        #     self.blocks.remove(self.blocks[int(code)])
        #     print(self.BGBlocksSortByHeight())
        #
        #     return

        #print(self.blocks[code].x(), self.blocks[code].y())
        for pos in self.indentPos:
            if pos[0] == code: continue
            if pos[1][0] <= e.pos().x() <= pos[1][0] + self.blocks[pos[0]].width() and pos[1][1] <= e.pos().y() <= pos[1][1] + self.blocks[pos[0]].height():
                inPos.append(pos)
                dropT = dropType.INDENT
        if dropT == dropType.INDENT:
            maxDepth = -1
            maxPos = inPos[0]
            for pos in inPos:
                if pos[2] > maxDepth:
                    maxPos = pos
                    maxDepth = pos[2]
            hPtr = 50
            idx = 0
            ex = False
            lengthFromTop = e.pos().y() - maxPos[1][1]
            if 0 <= lengthFromTop <= 50:
                pass
            else:
                for i in range(len(self.blocks[maxPos[0]].blockList)):
                    if hPtr <= lengthFromTop <= hPtr + self.blocks[self.blocks[maxPos[0]].blockList[i]].height():
                        idx = i + 1
                        hPtr += self.blocks[self.blocks[maxPos[0]].blockList[i]].height()
                        ex = True
                        break
                    hPtr += self.blocks[self.blocks[maxPos[0]].blockList[i]].height()
            if not ex and hPtr <= lengthFromTop <= hPtr + 50:
                idx = len(self.blocks[maxPos[0]].blockList)
            prevPrt = -1
            if self.blocks[code].parent() != None and  self.blocks[code].parent() != self:
                prevPrt = self.blocks[code].parent().code
            self.blocks[maxPos[0]].insertBlock(self.blocks[code], idx)
            self.blocks[code].setParent(self.blocks[maxPos[0]])
            self.blocks[maxPos[0]].blockList.insert(idx, code)
            #print("*")
            # 드롭한 블록이 indentBlock이라면 Depth을 새 부모의 Depth + 1 로 설정, Pos도 그에 따라 설정
            print(self.blocks[maxPos[0]].blockList)
            for i in range(len(self.blocks[maxPos[0]].blockList)):
                if self.getCode(self.blocks[self.blocks[maxPos[0]].blockList[i]]) in self._indentBlocks:
                    self.setDepth(self.blocks[maxPos[0]].blockList[i], self.blocks[code].parent().depth + 1)
                    #print("*")
                    self.setPos(self.blocks[maxPos[0]].blockList[i],
                                [self.codeToPos(self.blocks[code].parent().code)[1][0] + 50,
                                 self.codeToPos(self.blocks[code].parent().code)[1][1] + hPtr])
            #print("*")
            GWidth = blkW + maxPos[2] * 50 + 50
            self.blocks[code].globalWidth = GWidth
            #print(self.superList(code))
            for supPos in self.superList(code):
                tempH = self.blocks[supPos].height()
                tempW = self.blocks[supPos].globalWidth
                #print("*",maxPos[0], prevPrt)
                if maxPos[0] != prevPrt:
                    self.blocks[supPos].setMinimumHeight(tempH + blkH)
                    self.blocks[supPos].setMaximumHeight(tempH + blkH)

                if tempW < GWidth:
                    self.blocks[supPos].globalWidth = GWidth
                    self.blocks[supPos].setMinimumWidth(GWidth - self.blocks[supPos].depth * 50)
                    self.blocks[supPos].setMaximumWidth(GWidth - self.blocks[supPos].depth * 50)

        elif dropT == dropType.BACKGROUND:
            if self.getCode(self.blocks[code].parent()) in self._indentBlocks:
                self.blocks[code].parent().blockList.remove(code)
                for supPos in self.superList(int(code)):
                    tempH = self.blocks[supPos].height()
                    self.blocks[supPos].setMinimumHeight(tempH - blkH)
                    self.blocks[supPos].setMaximumHeight(tempH - blkH)
                    if self.blocks[supPos].globalWidth == self.blocks[int(code)].globalWidth:
                        maxW = 0
                        for blk in self.blocks[supPos].blockList:
                            if self.blocks[blk].globalWidth > maxW:
                                maxW = self.blocks[blk].globalWidth
                        if maxW == 0:
                            maxW = self.blocks[supPos].depth * 50 + 250
                        self.blocks[supPos].globalWidth = maxW
                        self.blocks[supPos].setMinimumWidth(maxW - self.blocks[supPos].depth * 50)
                        self.blocks[supPos].setMaximumWidth(maxW - self.blocks[supPos].depth * 50)
                # 여기에 뺄 때 크기 줄어드는 코드 완성하기
            self.blocks[code].setParent(self)
            if self.getCode(self.blocks[code]) in self._indentBlocks:
                self.setDepth(code, 0)
                self.setPos(code, [self.blocks[code].geometry().x(), self.blocks[code].geometry().y()])
        elif dropT == dropType.VARGET:
            pass
        else:
            raise (Exception)
        #print(self.indentPos)


        self.blocks[code].setVisible(True)
        print(self.BGBlocksSortByHeight())

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    myWindow = mainWindow() 
    myWindow.show()
    app.exec_()