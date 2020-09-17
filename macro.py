from PyQt5 import QtGui, QtCore, QtWidgets
import os
import time
import pyautogui as ps
from imagesearch import *

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500,300)
        self.setStyleSheet('background:#fff')
        layout = QtWidgets.QHBoxLayout(self)
        self.setContentsMargins(10,10,10,10)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(10)

        board = self.board = QtWidgets.QScrollArea(self)
        #board.setWidgetResizable(True)
        tools = self.tools = QtWidgets.QWidget(self)
        layout.addWidget(board)
        layout.addWidget(tools)

        board.setStyleSheet('background:#ddd')
        tools.setStyleSheet('background:#ddd')

        boardcontents = self.boardcontents = QtWidgets.QWidget()
        boardcontents.setStyleSheet('background:red')
        boardcontents.resize(100,0)
        boardcontents.offset = 0
        board.setWidget(boardcontents)

        boardlayout = self.boardlayout = QtWidgets.QVBoxLayout()
        #boardlayout.setAlignment(QtCore.Qt.AlignTop)
        boardcontents.setLayout(boardlayout)
       
        boardcontents.setContentsMargins(10,0,0,0)
        boardlayout.setContentsMargins(0,0,0,0)
        boardlayout.setSpacing(0)

        toolslayout = self.toolslayout = QtWidgets.QVBoxLayout(tools)
        toolslayout.setAlignment(QtCore.Qt.AlignTop)

        addbtn = self.addbtn = QtWidgets.QPushButton('add')
        addbtn.clicked.connect(self.addWidget)
        toolslayout.addWidget(addbtn)



    def addWidget(self):
        self.boardcontents.offset += 1
        test = QtWidgets.QWidget('test')
        test.setFixedHeight(30)
        test.clicked = self.test
#        test.setStyleSheet('background:black')
        self.boardlayout.addWidget(test)
        self.boardcontents.setFixedHeight(self.boardcontents.offset * 30)

    def mousePressEvent(self, event):
        print(self)
    def test(self, event):
        print(self.button())            

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())
