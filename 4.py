from PyQt5 import QtGui, QtCore, QtWidgets
import time

class GrabApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #App attributes
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        #self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)

        #Event condition var
        self.onMouseDown = False

        #Window geometry
        self.winW = QtWidgets.QDesktopWidget().availableGeometry().width()
        self.winH =  QtWidgets.QDesktopWidget().availableGeometry().height()
        
        print(QtWidgets.QDesktopWidget().availableGeometry().center())

        #App init
        self.resize(self.winW, self.winH)

        #Grab widget init
        self.grabBorder = QtWidgets.QWidget(self)
        self.grabBorder.setStyleSheet("border:2px solid #afa")
        self.grabBorder.resize(0,0)

        #frame
        self.frame = QtWidgets.QFrame(self)
        self.frame.setStyleSheet("background-color:rgba(255,0,0,255)")
        self.frame.resize(100,100)
        fg = self.frame.frameGeometry()
        fg.moveCenter(QtWidgets.QDesktopWidget().availableGeometry().center())

        self.frame.move(fg.left(),10)

    def grab(self):

        region = QtGui.QRegion(0,0,self.winW,self.winH)
        region -= QtGui.QRegion(self.grabX, self.grabY, self.grabW, self.grabH)
        self.grabBorder.move(self.grabX - 2, self.grabY - 2)
        self.grabBorder.resize(self.grabW + 4, self.grabH + 4)
        self.setMask(region)
        
    def paintEvent(self, event):
        print('paint')
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.2)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))   
        painter.drawRect(self.rect())

    def mouseMoveEvent(self, event):
        print('mousemove')
        print('x: ' + str(event.x()) + '\ny: ' + str(event.y()))
        if self.onMouseDown:
            self.endX = event.x()
            self.endY = event.y()
            if self.startX < self.endX:
                x = self.startX
                w = self.endX - x
            else:
                x = self.endX
                w = self.startX - x
            if self.startY < self.endY:
                y = self.startY
                h = self.endY - y
            else:
                y = self.endY
                h = self.startY - y
            self.grabX = x
            self.grabY = y
            self.grabW = w
            self.grabH = h
            self.grab()
         
    def mousePressEvent(self, event):
        print('mousepress')
        self.onMouseDown = True
        self.startX = event.x()
        self.startY = event.y()
    
    def mouseReleaseEvent(self, event):
        #범위가 제대로 지정됐으면, x > startx 캡처 후 앱 종료
        self.onMouseDown = False
        region = QtGui.QRegion(0,0,self.winW,self.winH)
        self.setMask(region)
        self.grabBorder.move(0,0)
        self.grabBorder.resize(0,0)

    def showApp(self):
        super().exec_()

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init()
    
    def init(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        btnlayout = QtWidgets.QVBoxLayout()
        self.setLayout(btnlayout)
        startbtn = QtWidgets.QPushButton('start')
        startbtn.clicked.connect(self.createGrabArea)
        btnlayout.addWidget(startbtn)

    def createGrabArea(self):
        grabarea = Sub()
        grabarea.move(0,0)
        grabarea.showApp()

class Sub(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.resize(500,500)
        self.move(0,0)
    def showApp(self):
        super().exec_()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)


    myapp = MyApp()
    myapp.show()


    sys.exit(app.exec_())