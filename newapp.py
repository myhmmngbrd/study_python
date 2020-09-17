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

        self.borderLeft.resize(0,0)
        self.borderRight.resize(0,0)
        self.borderTop.resize(0,0)
        self.borderBottom.resize(0,0)
        self.vertexLT.resize(0,0)
        self.vertexRT.resize(0,0)
        self.vertexRB.resize(0,0)
        self.vertexLB.resize(0,0)
        

        #grab status
        self.status = QtWidgets.QWidget(self)
        statuslayout = QtWidgets.QHBoxLayout(self.status)

        self.status.setContentsMargins(0,0,0,0)
        statuslayout.setContentsMargins(0,0,0,0)
        statuslayout.setSpacing(0)

        self.status.setFixedWidth(230)
        
        #status - location
        self.labelX1 = QtWidgets.QLabel('x1: ')
        self.labelY1 = QtWidgets.QLabel('y1: ')
        self.labelX2 = QtWidgets.QLabel('x2: ')
        self.labelY2 = QtWidgets.QLabel('y2: ')
        self.inputX1 = QtWidgets.QLineEdit()
        self.inputY1 = QtWidgets.QLineEdit()
        self.inputX2 = QtWidgets.QLineEdit()
        self.inputY2 = QtWidgets.QLineEdit()

        statuslayout.addWidget(self.labelX1)
        statuslayout.addWidget(self.inputX1)
        statuslayout.addWidget(self.labelY1)
        statuslayout.addWidget(self.inputY1)
        statuslayout.addWidget(self.labelX2)
        statuslayout.addWidget(self.inputX2)
        statuslayout.addWidget(self.labelY2)
        statuslayout.addWidget(self.inputY2)

        self.okbtn = QtWidgets.QPushButton('ok')
        statuslayout.addWidget(self.okbtn)

    def initStyle(self):
        #left border
        self.borderLeft.setStyleSheet('border-right:2px solid red')
        self.borderLeft.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        #right border
        self.borderRight.setStyleSheet('border-left:2px solid green')
        self.borderRight.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        #top border
        self.borderTop.setStyleSheet('border-bottom:2px solid yellow')
        self.borderTop.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        #bottom border
        self.borderBottom.setStyleSheet('border-top:2px solid blue')
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

        #status
        #inputbox

    def initEventTrigger(self):
        self.borderLeft.mousePressEvent = lambda event: self.mousePressEvent(event, 'l')
        self.borderRight.mousePressEvent = lambda event: self.mousePressEvent(event, 'r')
        self.borderTop.mousePressEvent = lambda event: self.mousePressEvent(event, 't')
        self.borderBottom.mousePressEvent = lambda event: self.mousePressEvent(event, 'b')
        self.vertexLT.mousePressEvent = lambda event: self.mousePressEvent(event, 'lt')
        self.vertexRT.mousePressEvent = lambda event: self.mousePressEvent(event, 'rt')
        self.vertexRB.mousePressEvent = lambda event: self.mousePressEvent(event, 'rb')
        self.vertexLB.mousePressEvent = lambda event: self.mousePressEvent(event, 'lb')

        self.inputX1.returnPressed.connect(self.modifyGrabArea)
        self.inputY1.returnPressed.connect(self.modifyGrabArea)
        self.inputX2.returnPressed.connect(self.modifyGrabArea)
        self.inputY2.returnPressed.connect(self.modifyGrabArea)

        self.okbtn.clicked.connect(self.save)

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
            self.mouseGrab()
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

    def mouseGrab(self):
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
        self.grab(x, y, w, h)

    def modifyGrabArea(self):
        x1 = self.inputX1.text()
        y1 = self.inputY1.text()
        x2 = self.inputX2.text()
        y2 = self.inputY2.text()

        if not (x1 + y1 + x2 + y2).isdecimal():
            #영역지정 안하면 오류뜸
            #self.inputX1.setText(str(self.x))
            #self.inputY1.setText(str(self.y))
            #self.inputY1.setText(str(self.x + self.w))
            #self.inputY1.setText(str(self.y + self.h))
            return
        x = int(x1)
        y = int(y1)
        w = int(x2) - int(x1)
        h = int(y2) - int(y1)
        sw = self.screen().geometry().width()
        sh = self.screen().geometry().height()
        if x < 0 or x > sw or w < 0 or w > sw or y < 0 or y > sh or h < 0 or h > sh:
            return

        self.grab(x, y, w, h)

    def grab(self, x, y, w, h):
        #grab border
        self.borderLeft.setGeometry(x - 10, y, 10, h)
        self.borderRight.setGeometry(x + w, y, 10, h)
        self.borderTop.setGeometry(x, y - 10, w, 10)
        self.borderBottom.setGeometry(x, y + h, w, 10)

        self.vertexLT.setGeometry(x - 10, y - 10, 10, 10)
        self.vertexRT.setGeometry(x + w, y - 10, 10, 10)
        self.vertexRB.setGeometry(x + w, y + h, 10, 10)
        self.vertexLB.setGeometry(x - 10, y + h, 10, 10)

        #status bar
        self.status.move(min(x + 20, self.screen().geometry().width() - self.status.geometry().width() - 20),min(y + 20, self.screen().geometry().height() - self.status.geometry().height() - 50))
        self.inputX1.setText(str(x))
        self.inputY1.setText(str(y))
        self.inputX2.setText(str(x+w))
        self.inputY2.setText(str(y+h))


        #set mask
        self.region = QtGui.QRegion(self.screen().availableGeometry())
        self.region -= QtGui.QRegion(x, y, w, h)
        self.region += QtGui.QRegion(self.status.geometry())
        self.setMask(self.region)

        #전역화하는게 맞는가?
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def save(self):
        self.accept()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)

        self.resize(200,200)
        
        self.grabbtn = QtWidgets.QPushButton('capture', self)
        self.grabbtn.clicked.connect(self.grab)
        
        self.caturebtn = QtWidgets.QPushButton('screenshot', self)
        self.caturebtn.clicked.connect(self.cature)



    def grab(self):
        grabwidget = GrabWindow()
        r = grabwidget.exec_()

        if r:
            print(grabwidget.x)
            print(grabwidget.y)
            print(grabwidget.w)
            print(grabwidget.h)
            self.x = grabwidget.x
            self.y = grabwidget.y
            self.w = grabwidget.w
            self.h = grabwidget.h

    def cature(self):
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())
