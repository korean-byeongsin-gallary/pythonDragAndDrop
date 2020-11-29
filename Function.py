import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QMimeData
from dragAndDrop import *

def loadStyle(path):
    with open(path,'r') as fh:
        return fh.read()

class printBlk(block):

    def __init__(self, _parent, code):
        block.__init__(self, "print" ,_parent, code)
        self.text = "print"
        self.setStyleSheet(loadStyle("styles/print.qss"))

    def getText(self):
        pass

class printMom(blockSpawn):
    def __init__(self, _parent, window):
        blockSpawn.__init__(self, "print", _parent, window)
        self.code = 2
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 10, 5, 5)
        self.title = QLabel("print")
        self.text = QLineEdit()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
        # 배경색 설정
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setMaximumWidth(200)
        self.setMinimumWidth(200)
        self.move(QPoint(0,0))



class forBlk(indentBlock):

    def __init__(self, _parent, code):
        indentBlock.__init__(self, "for", _parent, code)
        self.layout.addWidget(QLabel("in"))
        self.laterText = QLineEdit()
        self.layout.addWidget(self.laterText)
        self.setStyleSheet(loadStyle("styles/while.qss"))

        self.text = ""

class forMom(blockSpawn):
    def __init__(self, _parent, window):
        blockSpawn.__init__(self, "print", _parent, window)
        self.code = 3
        self.container = QVBoxLayout()
        self.indenting = QHBoxLayout()
        self.codeSpace = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.title = QLabel("for")
        self.text = QLineEdit()
        self.topSpace = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.bottomSpace = QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.indentSpace = QSpacerItem(30, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
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
        self.layout.addWidget(QLabel("in"))
        self.laterText = QLineEdit()
        self.layout.addWidget(self.laterText)
        self.setLayout(self.container)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)
        self.setMaximumWidth(250)
        self.setMinimumWidth(250)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.move(QPoint(0, 100))




