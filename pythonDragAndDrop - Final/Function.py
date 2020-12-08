import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt

from enums import *
from PyQt5.QtCore import QMimeData
from dragAndDrop import *

def loadStyle(path):
    with open(path,'r') as fh:
        return fh.read()

class printBlk(block):

    def __init__(self, parent, code):
        block.__init__(self, "print" ,parent, code)
        self.text = "print()"
        self.setStyleSheet(loadStyle("styles/print.qss"))
        self.textInput.textChanged[str].connect(self.setText)

    def setText(self, text):
        self.text = "print(" + text + ")"

class returnBlk(block):

    def __init__(self, parent, code):
        block.__init__(self, "return" ,parent, code)
        self.text = "return None"
        self.setStyleSheet(loadStyle("styles/return.qss"))
        self.textInput.textChanged[str].connect(self.setText)

    def setText(self, text):
        self.text = "return " + text

class operBlk(block):

    def __init__(self, _parent, code):
        block.__init__(self, "" ,_parent, code)
        self.var = ""
        self.op = " = "
        self.val = ""
        self.text = self.var + self.op + self.val
        self.textInput.setParent(None)
        self.title.setParent(None)
        self.oper = QComboBox()
        self.oper.addItem("=")
        self.oper.addItem("==")
        self.oper.addItem("<=")
        self.oper.addItem(">=")
        self.oper.addItem("!=")
        self.oper.addItem("+=")
        self.oper.addItem("-=")
        self.oper.addItem("*=")
        self.oper.addItem("/=")
        self.varName = QLineEdit()
        self.value = QLineEdit()
        self.layout.addWidget(self.varName)
        self.layout.addWidget(self.oper)
        self.layout.addWidget(self.value)
        self.setLayout(self.layout)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setStyleSheet(loadStyle("styles/oper.qss"))
        self.varName.textChanged[str].connect(self.setVar)
        self.value.textChanged[str].connect(self.setVal)
        self.oper.activated[str].connect(self.setOper)

    def setVar(self, text):
        self.var = text
        self.text = self.var + self.op + self.val

    def setVal(self, text):
        self.val = text + ":"
        self.text = self.var + self.op + self.val

    def setOper(self, text):
        self.oper = " " + text + " "
        self.text = self.var + self.op + self.val

class forBlk(indentBlock):

    def __init__(self, _parent, code):
        indentBlock.__init__(self, "for", _parent, code)
        self.layout.addWidget(QLabel("in"))
        self.textInput.setMaximumWidth(50)
        self.textInput.setMinimumWidth(50)
        self.laterText = QLineEdit()
        self.layout.addWidget(self.laterText)
        self.setStyleSheet(loadStyle("styles/loop.qss"))
        self.textInput.textChanged[str].connect(self.setVar)
        self.laterText.textChanged[str].connect(self.setRange)
        self.var = ""
        self.range = ""
        self.text = "for " + self.var + " in " + self.range

    def setVar(self, text):
        self.var = text
        self.text = "for " + self.var + " in " + self.range

    def setRange(self, text):
        self.range = text + ":"
        self.text = "for " + self.var + " in " + self.range


class classBlk(indentBlock):

    def __init__(self, _parent, code):
        indentBlock.__init__(self, "class", _parent, code)
        self.setStyleSheet(loadStyle("styles/class.qss"))
        self.textInput.textChanged[str].connect(self.setText)

        self.text = "class "

    def setText(self, text):
        self.text = "class " + text + "():"

class defBlk(indentBlock):

    def __init__(self, _parent, code):
        indentBlock.__init__(self, "def", _parent, code)
        self.setStyleSheet(loadStyle("styles/def.qss"))
        self.textInput.textChanged[str].connect(self.setText)

        self.text = "def "

    def setText(self, text):
        self.text = "def " + text + "():"
        return

class whileBlk(indentBlock):

    def __init__(self, _parent, code):
        indentBlock.__init__(self, "while", _parent, code)
        self.setStyleSheet(loadStyle("styles/loop.qss"))
        self.textInput.textChanged[str].connect(self.setText)

        self.text = "while :"

    def setText(self, text):
        self.text = "while " + text + ":"

class ifBlk(indentBlock):

    def __init__(self, _parent, code):
        indentBlock.__init__(self, "", _parent, code)
        self.stt = ":"
        self.op = "if "
        self.text = self.op + self.stt
        self.title.setParent(None)
        self.oper = QComboBox()
        self.oper.addItem("if")
        self.oper.addItem("elif")
        self.oper.addItem("else")
        self.layout.insertWidget(0, self.oper)
        self.setStyleSheet(loadStyle("styles/if.qss"))
        self.textInput.textChanged[str].connect(self.setText)
        self.oper.activated[str].connect(self.setOper)

    def setText(self, text):
        self.stt = text + ":"
        self.text = self.op + self.stt

    def setOper(self, text):
        self.op = text + " "
        self.text = self.op + self.stt



