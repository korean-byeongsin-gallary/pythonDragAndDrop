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
    def __init__(self, _parent, window,code):
        blockSpawn.__init__(self, "print", _parent, window,code)
        '''self.setMaximumHeight(500)
        self.setMinimumHeight(500)
        self.setMaximumWidth(2000)
        self.setMinimumWidth(2000)
        self.move(QPoint(0,0))'''



class forBlk(indentBlock):

    def __init__(self, _parent, code):
        indentBlock.__init__(self, "for", _parent, code)
        self.layout.addWidget(QLabel("in"))
        self.laterText = QLineEdit()
        self.layout.addWidget(self.laterText)
        self.setStyleSheet(loadStyle("styles/while.qss"))

        self.text = ""

class forMom(blockSpawn):
    def __init__(self, _parent, window, code):
        blockSpawn.__init__(self, "print", _parent, window, code)
        '''self.setMaximumWidth(250)
        self.setMinimumWidth(250)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.move(QPoint(0, 100))'''




