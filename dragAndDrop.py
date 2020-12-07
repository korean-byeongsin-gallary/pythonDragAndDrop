import sys
import copy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtCore import QMimeData

class base(QWidget):
    def __init__(self, _parent,code):
        QWidget.__init__(self, parent= _parent,flags=Qt.Widget)
        self.offset = 0
        self.code = code
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,5,5)
        self.setLayout(self.layout)        
    
    def paintEvent(self,event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        s = self.style()
        s.drawPrimitive(QStyle.PE_Widget, opt, p, self) 
    
    def mouseMoveEvent(self, e: QMouseEvent):
        mime_data = QMimeData()
        self.setVisible(False)
        #self.setParent(None)
        mime_data.setData("application/hotspot", b"%d %d %d" % (e.x(), e.y(), self.code))

        drag = QDrag(self)
        drag.parent = self
        # MIME 타입데이터를 Drag에 설정
        drag.setMimeData(mime_data)
        # 드래그시 위젯의 모양 유지를 위해 QPixmap에 모양을 렌더링
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_(Qt.MoveAction)

class block(base):
    def __init__(self, title, _parent,code):
        base.__init__(self, _parent, code)
        self.globalWidth = 200
        self.title = QLabel(title)
        self.textInput = QLineEdit()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textInput)
        #self.setLayout(self.layout)        
        #배경색 설정
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setMaximumWidth(200)
        self.setMinimumWidth(200)

class indentBlock(QWidget):
    def __init__(self, title, _parent, code):
        QWidget.__init__(self, parent= _parent, flags=Qt.Widget)
        self.tag = 1
        self.offset = 0
        self.code = code
        self.depth = 0
        self.blockList = []
        self.globalWidth = 250
        self.maxWidthBlocks = []
        self.container = QVBoxLayout()
        self.container.setSpacing(0)
        self.container.setContentsMargins(0, 0, 0, 50)
        self.indenting = QHBoxLayout()
        self.codeSpace = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.title = QLabel(title)
        self.textInput = QLineEdit()
        self.indentSpace = QWidget()
        self.indentSpace.setMinimumWidth(50)
        self.indentSpace.setMaximumWidth(50)
        self.indentSpace.setMinimumHeight(0)
        self.indentSpace.setMaximumHeight(0)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.textInput)
        self.indenting.addWidget(self.indentSpace)
        self.indenting.addLayout(self.codeSpace)
        self.container.addLayout(self.layout)
        self.container.addLayout(self.indenting)
        self.setLayout(self.container)
        #배경색 설정
        self.setMaximumWidth(250)
        self.setMinimumWidth(250)
        self.setMinimumHeight(self.blockCount() * 50 + 100)
        self.setMaximumHeight(self.blockCount() * 50 + 100)
        self.codeSpace.setSpacing(0)

    def initWidget(self):
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QDragEnterEvent):
        print("BAaaa")
        e.accept()

    def dropEvent(self, e: QDropEvent):
        print("BAaaa")

    def insertBlock(self, block, pos):
        #self.codeSpace.addWidget(block)
        self.codeSpace.insertWidget(pos, block)

    def blockCount(self):
        return len(self.blockList)
        #return self.codeSpace.count()

    def paintEvent(self,event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        s = self.style()
        s.drawPrimitive(QStyle.PE_Widget, opt, p, self) 

    def deleteBlock(self,block):
        pass


    def mouseMoveEvent(self, e: QMouseEvent):
        mime_data = QMimeData()
        self.setVisible(False)
        mime_data.setData("application/hotspot", b"%d %d %d" % (e.x(), e.y(), self.code))
  

        drag = QDrag(self)
        drag.parent = self
        # MIME 타입데이터를 Drag에 설정
        drag.setMimeData(mime_data)
        # 드래그시 위젯의 모양 유지를 위해 QPixmap에 모양을 렌더링
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)

        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_(Qt.MoveAction)

class blockSpawn(QWidget):
    def __init__(self, parent):#,title, window, code):
        QWidget.__init__(self, parent= parent,flags=Qt.Widget)

    def setupUi(self, window, code):
        self.window = window
        self.code = code
        self.layout = QHBoxLayout()
        dummy =  self.window.addBlock(self.code, (self.x(),self.y()))
        self.window.indentPos = []
        self.window.blocks = []
        pixmap = QPixmap(dummy.size())
        dummy.render(pixmap)
        dummy.setVisible(False)
        self.img = QLabel("")
        self.img.resize(dummy.size())
        self.img.setPixmap(pixmap)
        self.layout.addWidget(self.img)
        self.setLayout(self.layout)
        self.setMaximumHeight(pixmap.height()+50)
        self.setMinimumHeight(pixmap.height()+50)
        self.setMaximumWidth(pixmap.width()+50)
        self.setMinimumWidth(pixmap.width()+50)

    def mouseMoveEvent(self, e: QMouseEvent):
        newBlock = self.window.addBlock(self.code, (self.x(),self.y()))
        newBlock.setParent(None)
        mime_data = QMimeData()
        mime_data.setData("application/hotspot", b"%d %d %d" % (e.x(), e.y(), newBlock.code))
        drag = QDrag(newBlock)
        drag.parent = newBlock

        drag.setMimeData(mime_data)
        #newBlock.setVisible(True)
        pixmap = QPixmap(newBlock.size())
        newBlock.render(pixmap)
        drag.setPixmap(pixmap)

        drag.setHotSpot(e.pos() - newBlock.rect().topLeft())
        drag.exec_(Qt.MoveAction)

class trashCan(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent= parent,flags=Qt.Widget)
    
    def dropEvent(self, e: QDropEvent):
        pass