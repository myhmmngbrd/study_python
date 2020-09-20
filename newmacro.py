from PyQt5 import QtGui, QtCore, QtWidgets

class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        print('application is running...')

        self.resize(500,500)

        ly = QtWidgets.QHBoxLayout()
        self.setLayout(ly)

        bd = self.board = Board()
        ly.addWidget(bd)

        tl = self.tools = Tools()
        ly.addWidget(tl)

        mcbtn = self.mouseClickButton = QtWidgets.QPushButton('mouse click')
        mcbtn.clicked.connect(self.mouseClick)
        tl.addWidget(mcbtn)

        editbtn = self.editButton = QtWidgets.QPushButton('edit')
        #editbtn.clicked.connect(self.edit) 
        editbtn.setDisabled(True)
        tl.addWidget(editbtn)

    def mouseClick(self, event):
        self.hide()
        dialog = Commander('click')
        r = dialog.exec_()
        if r:
            status = dialog.returnValue
            self.board.addCommand('click', status, [self.editButton])
        self.show()




class Board(QtWidgets.QScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        wg = self.widget = QtWidgets.QWidget()
        ly = self.layout = QtWidgets.QVBoxLayout()
        ly.setAlignment(QtCore.Qt.AlignTop)

        self.setWidget(wg)
        wg.setLayout(ly)

    def addCommand(self, eventType, status, options):
        self.layout.addWidget(Command(self, eventType, status, options))

    def select(self, widget):
        #선택한 위젯만 파랗게
        for i in range(self.layout.count()):
            other = self.layout.itemAt(i).widget()
            other.setStyleSheet('background: #ddd; color: #000')
        widget.setStyleSheet('background: #00f; color: #fff')
        self.selected = widget

    def moveUp(self, widget):
        print()
    
    def moveDown(self, widget):
        print()

    

class Tools(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        ly = self.layout = QtWidgets.QVBoxLayout()
        ly.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(ly)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
        


class Command(QtWidgets.QWidget):
    pressed = False
    def __init__(self, main, eventType, status, options):
        super().__init__()
        self.main = main

        self.setStyleSheet('background:#ddd')

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        text = eventType
        for key, value in status.items():
            text += (', ' + str(key) + ': ' + str(value))

        label = QtWidgets.QLabel()
        label.setText(text)
        layout.addWidget(label)

        self.options = options
        
    def mousePressEvent(self, event):
        self.pressed = True

    def mouseReleaseEvent(self, event):
        if self.pressed:
            self.pressed = False
            self.main.select(self)

    def focusOutEvent(self, evnet):
        print(self)

class Commander(QtWidgets.QDialog):
    def __init__(self, eventType):
        super().__init__()

        self.eventType = eventType
        #attrs
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #background
        self.setGeometry(0, 0, self.screen().geometry().width(), self.screen().geometry().height())

        self.status = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout()
        self.status.setLayout(layout)

        self.status.setStyleSheet('background:#333; color:#aaa')

        if self.eventType == 'click':
            self.mousepos = QtWidgets.QLabel()
            self.mousepos.setText('x: 0 y: 0')
            self.mousepos.setFixedWidth(85)
            layout.addWidget(self.mousepos)
            
        self.maxWidth = self.rect().width() - self.status.rect().width() - 20
        self.maxHeight = self.rect().height() - self.status.rect().height() - 40

        self.status.hide()

    def mouseMoveEvent(self, event):
        if not self.status.isVisible():
            self.status.show()
        if self.eventType == 'click':
            self.mousepos.setText('x: ' + str(event.x()) + ' y: ' + str(event.y()))
            self.status.move(
                min(event.x() + 20, self.maxWidth),
                min(event.y() + 10, self.maxHeight)
            )

    def mousePressEvent(self, event):
        if self.eventType == 'click':
            self.returnValue = {'x': event.x(), 'y': event.y()}
            self.accept()


    

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.2)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))   
        painter.drawRect(self.rect())



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())