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

    def mouseMoveEvent(self, e: QMouseEvent):
        mime_data = QMimeData()
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
    def __init__(self, title, _parent,window):
        QWidget.__init__(self, parent= _parent,flags=Qt.Widget)
        self.title= title
        self.window = window


        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)
        self.resize(100,100)
        self.newBlock = None

    def mouseMoveEvent(self, e: QMouseEvent):
        mime_data = QMimeData()
        mime_data.setData("application/hotspot", b"%d %d %d" % (e.x(), e.y(), self.newBlock.code))
        drag = QDrag(self.newBlock)
        drag.parent = self.newBlock

        drag.setMimeData(mime_data)

        pixmap = QPixmap(self.newBlock.size())
        self.newBlock.render(pixmap)
        drag.setPixmap(pixmap)

        drag.setHotSpot(e.pos() - self.newBlock.rect().topLeft())
        drag.exec_(Qt.MoveAction)
    def mousePressEvent(self, e): # e ; QMouseEvent 
        print('BUTTON PRESS')
        self.newBlock = self.window.addBlock(self.title,(self.x(),self.y()))