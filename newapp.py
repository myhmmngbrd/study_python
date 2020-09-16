from PyQt5 import QtGui, QtCore, QtWidgets
import os
import time
import pyautogui as ps
from imagesearch import *

class GrabWindow(QtWidgets.QDialog):
    #attrs
    mousePressed = False
    grabMode = None
    
    def __init__(self):
        super().__init__()
        self.init()

    #init
    def init(self):
        #attrs
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #init
        self.setGeometry(self.screen().availableGeometry())

        #grab border
        self.initWidgets()
        self.initStyle()
        self.initEventTrigger()

    def initWidgets(self):
        #grab border
        self.borderLeft = QtWidgets.QWidget(self)
        self.borderRight = QtWidgets.QWidget(self)
        self.borderTop = QtWidgets.QWidget(self)
        self.borderBottom = QtWidgets.QWidget(self)
        self.vertexLT = QtWidgets.QWidget(self)
        self.vertexRT = QtWidgets.QWidget(self)
        self.vertexRB = QtWidgets.QWidget(self)
        self.vertexLB = QtWidgets.QWidget(self)

        #grab status
        self.status = QtWidgets.QWidget(self)
        stautslayout = QtWidgets.QHBoxLayout(self.status)
        
        #status - location
        self.labelX1 = QtWidgets.QLabel('x1: ')
        self.labelY1 = QtWidgets.QLabel('y1: ')
        self.labelX2 = QtWidgets.QLabel('x2: ')
        self.labelY2 = QtWidgets.QLabel('y2: ')
        self.inputX1 = QtWidgets.QLineEdit()
        self.inputY1 = QtWidgets.QLineEdit()
        self.inputX2 = QtWidgets.QLineEdit()
        self.inputY2 = QtWidgets.QLineEdit()

        stautslayout.addWidget(self.labelX1)
        stautslayout.addWidget(self.inputX1)
        stautslayout.addWidget(self.labelY1)
        stautslayout.addWidget(self.inputY1)
        stautslayout.addWidget(self.labelX2)
        stautslayout.addWidget(self.inputX2)
        stautslayout.addWidget(self.labelY2)
        stautslayout.addWidget(self.inputY2)

    def initStyle(self):
        #left border
        self.borderLeft.setStyleSheet('border-right:2px solid green')
        self.borderLeft.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        #right border
        self.borderRight.setStyleSheet('border-left:2px solid green')
        self.borderRight.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        #top border
        self.borderTop.setStyleSheet('border-bottom:2px solid green')
        self.borderTop.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        #bottom border
        self.borderBottom.setStyleSheet('border-top:2px solid green')
        self.borderBottom.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        #left top vertex
        self.vertexLT.setStyleSheet(
            'border-right: 2px solid green;'
            'border-bottom: 2px solid green'
        )
        self.vertexLT.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        #right top vertex
        self.vertexRT.setStyleSheet(
            'border-left: 2px solid green;'
            'border-bottom: 2px solid green'
        )
        self.vertexRT.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        #left bottom vertex
        self.vertexRB.setStyleSheet(
            'border-left: 2px solid green;'
            'border-top: 2px solid green'
        )
        self.vertexRB.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        #right bottom vertex
        self.vertexLB.setStyleSheet(
            'border-right: 2px solid green;'
            'border-top: 2px solid green'
        )
        self.vertexLB.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))

    def initEventTrigger(self):
        self.borderLeft.mousePressEvent = lambda event: self.mousePressEvent(event, 'l')
        self.borderRight.mousePressEvent = lambda event: self.mousePressEvent(event, 'r')
        self.borderTop.mousePressEvent = lambda event: self.mousePressEvent(event, 't')
        self.borderBottom.mousePressEvent = lambda event: self.mousePressEvent(event, 'b')
        self.vertexLT.mousePressEvent = lambda event: self.mousePressEvent(event, 'lt')
        self.vertexRT.mousePressEvent = lambda event: self.mousePressEvent(event, 'rt')
        self.vertexRB.mousePressEvent = lambda event: self.mousePressEvent(event, 'rb')
        self.vertexLB.mousePressEvent = lambda event: self.mousePressEvent(event, 'lb')

    #event trigger
    def mousePressEvent(self, event, mode = None):
        self.mousePressed = True
        self.grabMode = mode
        self.x1 = event.x()
        self.y1 = event.y()
    def mouseReleaseEvent(self, event):
        self.mousePressed = False
    def mouseMoveEvent(self, event):
        if self.mousePressed:
            self.x2 = event.x()
            self.y2 = event.y()
            self.grab()
    def paintEvent(self, event):
        self.paint()

    #event handler

    def paint(self):
        #transparent background
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.2)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))   
        painter.drawRect(self.rect())

        #grab border

    def grab(self):
        ## self.x2 범위 제한 필요
        if not self.grabMode:
            x = min(self.x1, self.x2)
            y = min(self.y1, self.y2)
            w = abs(self.x1 - self.x2)
            h = abs(self.y1 - self.y2)
        else:
            hor = self.borderTop.geometry()
            ver = self.borderLeft.geometry()
            if self.grabMode == 'l':
                if self.x2 > hor.right():
                    x = hor.right() + 1
                    w = 0
                else:
                    x = self.x2
                    w = hor.right() - self.x2 + 1
                y = ver.top()
                h = ver.height()
            elif self.grabMode == 'r':
                x = hor.left()
                if self.x2 < hor.left():
                    w = 0
                else:
                    w = self.x2 - hor.left()
                y = ver.top()
                h = ver.height()
            elif self.grabMode == 't':
                x = hor.left()
                w = hor.width()
                if self.y2 > ver.bottom():
                    y = ver.bottom() + 1
                    h = 0
                else:
                    y = self.y2
                    h = ver.bottom() - self.y2 + 1
            elif self.grabMode == 'b':
                x = hor.left()
                w = hor.width()
                y = ver.top()
                if self.y2 < ver.top():
                    h = 0
                else:
                    h = self.y2 - ver.top()
            elif self.grabMode == 'lt':
                if self.x2 > hor.right():
                    x = hor.right() + 1
                    w = 0
                else:
                    x = self.x2
                    w = hor.right() - self.x2 + 1
                if self.y2 > ver.bottom():
                    y = ver.bottom() + 1
                    h = 0
                else:
                    y = self.y2
                    h = ver.bottom() - self.y2 + 1
            elif self.grabMode == 'rt':
                x = hor.left()
                if self.x2 < hor.left():
                    w = 0
                else:
                    w = self.x2 - hor.left()
                if self.y2 > ver.bottom():
                    y = ver.bottom() + 1
                    h = 0
                else:
                    y = self.y2
                    h = ver.bottom() - self.y2 + 1
            elif self.grabMode == 'rb':
                x = hor.left()
                if self.x2 < hor.left():
                    w = 0
                else:
                    w = self.x2 - hor.left()
                y = ver.top()
                if self.y2 < ver.top():
                    h = 0
                else:
                    h = self.y2 - ver.top()
            elif self.grabMode == 'lb':
                if self.x2 > hor.right():
                    x = hor.right() + 1
                    w = 0
                else:
                    x = self.x2
                    w = hor.right() - self.x2 + 1
                y = ver.top()
                if self.y2 < ver.top():
                    h = 0
                else:
                    h = self.y2 - ver.top()


        #grab border
        self.borderLeft.setGeometry(x - 10, y, 10, h)
        self.borderRight.setGeometry(x + w, y, 10, h)
        self.borderTop.setGeometry(x, y - 10, w, 10)
        self.borderBottom.setGeometry(x, y + h, w, 10)

        self.vertexLT.setGeometry(x - 10, y - 10, 10, 10)
        self.vertexRT.setGeometry(x + w, y - 10, 10, 10)
        self.vertexRB.setGeometry(x + w, y + h, 10, 10)
        self.vertexLB.setGeometry(x - 10, y + h, 10, 10)


        #set mask
        self.region = QtGui.QRegion(self.screen().availableGeometry())
        self.region -= QtGui.QRegion(x, y, w, h)
        self.setMask(self.region)

        #꼭지점 영역설정하고, 그리고, 마우스 커서 변경해주고, 드래그로 확대하는 기능 만들기


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = GrabWindow()
    myapp.show()

    sys.exit(app.exec_())
