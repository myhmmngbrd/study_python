from PyQt5 import QtGui, QtCore, QtWidgets
import os
import time
import pyautogui as ps
from imagesearch import *

#paint 이벤트 부하 줄이기
#inputbox 대신 지금 지역정보가 기입된 라벨 삽입하기


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
    crash = False
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
        self.options.resize(200,30)
        self.options.hide()

        optlayout = QtWidgets.QHBoxLayout()
        self.options.setLayout(optlayout)
        self.options.setContentsMargins(0,0,0,0)
        optlayout.setContentsMargins(0,0,0,0)
        optlayout.setSpacing(2)


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
        if self.selected:
            self.options.hide()
    
    def mouseReleaseEvent(self, event):
        print('mouseRealse')
        self.onClick = False
        if self.selected:
            x = min(self.eX + 10, self.screen().size().width() - self.options.contentsRect().width() - 10)
            y = min(self.eY, self.screen().size().height() - self.options.contentsRect().height() - 50)
            self.options.move(x, y)
            self.region += QtGui.QRegion(x, y, self.options.contentsRect().width(), self.options.contentsRect().height())
            self.setMask(self.region)
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
        print(self.rect())

    def grab(self):
        print('grab')
        self.selected = True
        self.x = min(self.sX, self.eX)
        self.w = abs(self.eX - self.sX)
        self.y = min(self.sY, self.eY)
        self.h = abs(self.eY - self.sY)
        
        self.border.setGeometry(self.x-2,self.y-2,self.w+4,self.h+4)
        self.region = QtGui.QRegion(self.screen().availableGeometry())
        self.region -= QtGui.QRegion(self.x,self.y,self.w,self.h)
        self.setMask(self.region)



        



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())

