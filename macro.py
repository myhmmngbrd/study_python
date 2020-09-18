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

        #board, tool
        board = self.board = QtWidgets.QScrollArea(self)
        board.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #board.setWidgetResizable(True)
        tools = self.tools = QtWidgets.QWidget(self)
        layout.addWidget(board)
        layout.addWidget(tools)

        board.setStyleSheet('background:#ddd')
        tools.setStyleSheet('background:#ddd')

        print(board.geometry())

        #board contents
        bc = self.boardcontents = QtWidgets.QWidget()
        bc.resize(board.geometry().width(), 0)
        bc.offset = 0
        board.setWidget(bc)

        bl = self.boardlayout = QtWidgets.QVBoxLayout()
        #boardlayout.setAlignment(QtCore.Qt.AlignTop)
        bc.setLayout(bl)
       
        bc.setContentsMargins(0,0,0,0)
        bl.setContentsMargins(0,0,0,0)
        bl.setSpacing(0)

        self.orders = []
        #tools contents
        tl = self.toolslayout = QtWidgets.QVBoxLayout(tools)
        tl.setAlignment(QtCore.Qt.AlignTop)

        addbtn = self.addbtn = QtWidgets.QPushButton('add')
        addbtn.clicked.connect(self.addWidget)
        tl.addWidget(addbtn)

    def resizeEvent(self, event):
        self.boardcontents.setFixedWidth(self.board.geometry().width())


    def addWidget(self):
        offset = self.boardcontents.offset
        self.boardcontents.offset += 1
        
        order = Order()#QtWidgets.QWidget()
        #order.mousePressEvent = lambda event: self.test(event, order)
        self.orders.append(order)

        self.boardlayout.addWidget(order)
        self.boardcontents.setFixedHeight((offset + 1) * 30)

        print(self.boardcontents.children()[offset + 1].childrenRect())

class Order(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        bg = self.background = QtWidgets.QWidget(self)
        bg.resize(self.rect().width(), self.rect().height())

#        QtWidgets.QLabel('test',bg)

        bl = self.backgroundlayout = QtWidgets.QVBoxLayout()
        bg.setLayout(bl)

        test = QtWidgets.QLabel('test')
        bl.addWidget(test)

        print(test.geometry())

        
    def mousePressEvent(self, event):
        self.parent().setStyleSheet('background:red')
        self.setFocus()

    def focusInEvent(self, event):
        print('focusin')
        self.setStyleSheet('''
            background:blue;
            color:white;
        ''')

    def focusOutEvent(self, event):
        print('focusout')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())
