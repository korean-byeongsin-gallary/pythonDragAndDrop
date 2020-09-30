import sys
import copy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtCore import QMimeData

class block(QWidget):
    def __init__(self, title, _parent):
        QWidget.__init__(self, parent= _parent,flags=Qt.Widget)
        self.offset = 0
        self.layout = QHBoxLayout()
        self.activate = True
        self.title = QLabel(title)
        self.text = QLineEdit()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
        
        #배경색 설정
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)
    
    def mouseMoveEvent(self, e: QMouseEvent):
        if self.activate:
            mime_data = QMimeData()
            mime_data.setData("application/hotspot", b"%d %d" % (e.x(), e.y()))

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
    def __init__(self,contain,_parent):
        QWidget.__init__(self, flags=Qt.Widget)
        contain.parent = self
        contain.activate = False
        self.contain = contain

        #배경색 설정
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)
    
    def mouseMoveEvent(self, e: QMouseEvent):
        newCopy = copy.deepcopy(self.contain)
        newCopy.activate = True
        newCopy.parent = self.parent
        newCopy.mouseMoveEvent(e)