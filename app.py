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
    changed = True
    x=0
    y=0
    w=0
    h=0
    X1 = 0
    Y1 = 0
    X2 = 0
    Y2 = 0

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
        self.border.setCursor(QtCore.Qt.SizeAllCursor)

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

        #position inputbox
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
        self.changed = True
        self.X1 = event.x()
        self.Y1 = event.y()
        if self.selected:
            self.options.hide()
    
    def mouseReleaseEvent(self, event):
        print('mouseRealse')
        self.onClick = False
        self.changed = True
        #if self.selected:

    def mouseMoveEvent(self, event):
        if self.onClick:
            self.X2 = event.x()
            self.Y2 = event.y()
            self.grab()

    def paintEvent(self, event):
        #if self.changed:
            self.repaint()
        
    def grab(self):
        self.selected = True
        self.x = min(self.X1, self.X2)
        self.w = abs(self.X2 - self.X1)
        self.y = min(self.Y1, self.Y2)
        self.h = abs(self.Y2 - self.Y1)
        self.border.setGeometry(self.x-2,self.y-2,self.w+4,self.h+4)
        self.region = QtGui.QRegion(self.screen().availableGeometry())
        self.region -= QtGui.QRegion(self.x,self.y,self.w,self.h)
        self.setOptions()
        self.setMask(self.region)

    def repaint(self):
        print('repaint')
        #transparent
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.2)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))   
        painter.drawRect(self.rect())
        self.changed = False
        
    def setOptions(self):
        x = min(self.X2 + 10, self.screen().size().width() - self.options.contentsRect().width() - 10)
        y = min(self.Y2, self.screen().size().height() - self.options.contentsRect().height() - 50)
        self.options.move(x, y)
        self.region += QtGui.QRegion(x, y, self.options.contentsRect().width(), self.options.contentsRect().height())
        self.inputX1.setText(str(self.x))
        self.inputY1.setText(str(self.y))
        self.inputX2.setText(str(self.x + self.w))
        self.inputY2.setText(str(self.y + self.h))
        print(self.options.isVisible())
        if not self.options.isVisible():
            self.options.show()



        



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())

