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
        self.inputEdit = QLineEdit()
        self.btn = QPushButton("aaaa")
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.inputEdit)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)        
        #배경색 설정
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)
        print(self.inputEdit.__dict__)

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

    def __getstate__(self):
        d = self.__dict__
        del(d['layout'],d['offset'])
        d['title'] = d['title'].text()
        d['inputEdit'] = d['inputEdit'].text()
        d['btn']= d['btn'].text()
        return d

    def __setstate__(self,d):
        self.title.setText(d['title'])
        self.code = d['code']
        self.inputEdit.setText(d['inputEdit'])
    
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
        mime_data = QMimeData()
        mime_data.setData("application/hotspot", b"%d %d %d" % (e.x(), e.y(), newBlock.code))
        drag = QDrag(newBlock)
        drag.parent = newBlock

        drag.setMimeData(mime_data)
        newBlock.setVisible(True)
        newBlock.setVisible(False)
        pixmap = QPixmap(newBlock.size())
        newBlock.render(pixmap)
        drag.setPixmap(pixmap)

        drag.setHotSpot(e.pos() - newBlock.rect().topLeft())
        drag.exec_(Qt.MoveAction)

class TrashCan(QWidget):
    def __init__(self, _parent,window):
        QWidget.__init__(self, parent= _parent,flags=Qt.Widget)
        self.window = window
        self.setAcceptDrops(True)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)
        self.resize(100,100)

    def dragEnterEvent(self, e: QDragEnterEvent):
        e.accept()

    def dropEvent(self, e: QDropEvent):
        offset = e.mimeData().data("application/hotspot")
        x, y, code = offset.data().decode('utf-8').split() 
        self.window.delBlock(int(code))
        return
        print("aaa")
        e.setDropAction(Qt.MoveAction)
        e.accept()