from PyQt5 import QtGui, QtCore, QtWidgets
import os
import time
import pyautogui as ps
from imagesearch import *

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #layout
        layout = QtWidgets.QVBoxLayout(self)

        #grabbutton
        grabbtn = QtWidgets.QPushButton('grab')
        grabbtn.clicked.connect(self.grab)
        layout.addWidget(grabbtn)


    def grab(self):
        print('function grab')

        self.hide()

        subapp = GrabArea()
        result = subapp.exec_()

        print('function grab2')

        self.show()

        print(result)
        

class GrabArea(QtWidgets.QDialog):
    onClick = False
    selected = False
    sX = 0
    sY = 0
    eX = 0
    eY = 0

    def __init__(self):
        super().__init__()

        #attrs
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #init
        screen = self.screen()
        print(screen.name())
        print(screen.size())
        print(screen.availableGeometry())
        self.setGeometry(screen.availableGeometry())

        #grabborder
        self.border = QtWidgets.QWidget(self)
        self.border.setStyleSheet("border: 2px solid green")
        self.border.resize(0,0)

        #graboption
        self.options = QtWidgets.QWidget(self)
        self.options.setStyleSheet('background: rgba(255,0,0,100)')
        self.options.resize(1000,1000)
        self.options.move(100,100)
        self.options.hide()

        optlayout = QtWidgets.QHBoxLayout()
        self.options.setLayout(optlayout)

        self.inputX1 = QtWidgets.QLineEdit()
        self.inputY1 = QtWidgets.QLineEdit()
        self.inputX2 = QtWidgets.QLineEdit()
        self.inputY2 = QtWidgets.QLineEdit()

        optlayout.addWidget(self.inputX1)
        optlayout.addWidget(self.inputY1)
        optlayout.addWidget(self.inputX2)
        optlayout.addWidget(self.inputY2)


    def mousePressEvent(self, event):
        print('mousePress')
        self.onClick = True
        self.sX = event.x()
        self.sY = event.y()
    
    def mouseReleaseEvent(self, event):
        print('mouseRealse')
        self.onClick = False
        if self.selected:
            self.options.show()

    def mouseMoveEvent(self, event):
        if self.onClick:
            print('mouseMove')
            self.eX = event.x()
            self.eY = event.y()
            self.grab()

    def paintEvent(self, event):
        print('paint')

        #transparent
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.2)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))   
        painter.drawRect(self.rect())

    def grab(self):
        print('grab')
        self.selected = True
        if (self.sX < self.eX):
            x = self.sX
            w = self.eX - self.sX
        else:
            x = self.eX
            w = self.sX - self.eX
        if (self.sY < self.eY):
            y = self.sY
            h = self.eY - self.sY
        else:
            y = self.eY
            h = self.sY - self.eY
        
        self.border.setGeometry(x-2,y-2,w+4,h+4)
        region = QtGui.QRegion(self.screen().availableGeometry())
        region -= QtGui.QRegion(x,y,w,h)
        self.setMask(region)



        



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())

