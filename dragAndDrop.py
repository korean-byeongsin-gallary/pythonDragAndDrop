import sys
import copy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtCore import QMimeData

class block(QWidget):
    def __init__(self, title, _parent,code):
        QWidget.__init__(self, parent= _parent,flags=Qt.Widget)
        self.offset = 0
        self.code = code
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,5,5)
        self.title = QLabel(title)
        self.text = QLineEdit()
        self.btn = QPushButton("aaaa")
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)        
        #배경색 설정
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)
        self.setMaximumHeight(40)
        self.setMinimumHeight(40)
        self.setMaximumWidth(210)
        self.setMinimumWidth(210)

    def mouseMoveEvent(self, e: QMouseEvent):
        mime_data = QMimeData()
        self.setVisible(False)
        self.setParent(None)
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

class indentBlock(QWidget):
    def __init__(self, title, _parent,code):
        QWidget.__init__(self, parent= _parent,flags=Qt.Widget)
        self.offset = 0
        self.code = code
        self.container = QVBoxLayout()
        self.indenting = QHBoxLayout()
        self.codeSpace = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.title = QLabel(title)
        self.text = QLineEdit()
        self.topSpace = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.bottomSpace = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.indentSpace = QSpacerItem(30, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.btn = QPushButton("aaaa")
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.text)
        #self.layout.addWidget(self.btn)
        self.indenting.addItem(self.indentSpace)
        #self.codeSpace.addWidget()
        self.indenting.addLayout(self.codeSpace)
        self.container.addLayout(self.layout)
        #self.container.addItem(self.topSpace)
        self.container.addLayout(self.indenting)
        self.container.addItem(self.bottomSpace)
        self.setLayout(self.container)
        #배경색 설정
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)
        self.setMaximumWidth(250)
        self.setMinimumWidth(250)
        self.codeSpace.setSpacing(0)
    def insertBlock(self, block, pos):
        #self.codeSpace.addWidget(block)
        self.codeSpace.insertWidget(pos, block)

    def blockCount(self):
        return self.codeSpace.count()

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

'''
    def dropEvent(self, e: QDropEvent):
        source = e.source()
        print(source)
        # 보내온 데이터를 받기
        # 그랩 당시의 마우스 위치값을 함께 계산하여 위젯 위치 보정
        offset = e.mimeData().data("application/hotspot")
        x, y, code = offset.data().decode('utf-8').split()
        #self.blocks[int(code)].setParent(self)
        self.blocks[int(code)].setVisible(True)

        e.setDropAction(Qt.MoveAction)
        e.accept()
'''


class blockSpawn(QWidget):
    def __init__(self, title, _parent,window):
        QWidget.__init__(self, parent= _parent,flags=Qt.Widget)
        self.title= title
        self.window = window


        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)
        self.resize(100,100)

    def mouseMoveEvent(self, e: QMouseEvent):
        newBlock = self.window.addBlock(self.title,(self.x(),self.y()))
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