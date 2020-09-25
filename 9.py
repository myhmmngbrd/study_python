from PyQt5 import QtGui, QtCore, QtWidgets

class Main(QtWidgets.QWidget):
    selected = None
    initWidth = 100
    initColor = 0
    colors = ['background:#f00','background:#0f0','background:#00f']
    count = 0
    def __init__(self):
        super().__init__()

        resetbtn = QtWidgets.QPushButton('reset', self)
        resetbtn.setGeometry(30,0,50,20)

        btn = QtWidgets.QPushButton('+', self)
        btn.resize(20,20)

        self.label = QtWidgets.QLabel('시행횟수: ' + str(self.count), self)
        self.label.setGeometry(90,0,100,20)

        self.setContentsMargins(10,30,10,10)

        ly = QtWidgets.QHBoxLayout()
        self.setLayout(ly)

        wd1 = QtWidgets.QWidget()
        wd1.setStyleSheet('border: 1px solid black')
        wd1.setFixedSize(300, 500)
        wd1.mousePressEvent = lambda event: self.move(wd1)
        ly.addWidget(wd1)
        ly1 = self.ly1 = QtWidgets.QVBoxLayout()
        ly1.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        #ly1.setSpacing(0)
        wd1.setLayout(ly1)

        wd2 = QtWidgets.QWidget()
        wd2.setStyleSheet('border: 1px solid black')
        wd2.setFixedSize(300, 500)
        wd2.mousePressEvent = lambda event: self.move(wd2)
        ly.addWidget(wd2)
        ly2 = self.ly2 = QtWidgets.QVBoxLayout()
        ly2.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        #ly2.setSpacing(0)
        wd2.setLayout(ly2)

        wd3 = QtWidgets.QWidget()
        wd3.setStyleSheet('border: 1px solid black')
        wd3.setFixedSize(300, 500)
        wd3.mousePressEvent = lambda event: self.move(wd3)
        ly.addWidget(wd3)
        ly3 = self.ly3 = QtWidgets.QVBoxLayout()
        ly3.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        #ly3.setSpacing(0)
        wd3.setLayout(ly3)

        btn.clicked.connect(lambda evnet: self.addBlock(ly1))

        resetbtn.clicked.connect(self.reset)


    def addBlock(self, layout):
        block = QtWidgets.QLineEdit()
        block.setFixedSize(self.initWidth, 40)
        block.setStyleSheet(self.colors[self.initColor])
        block.mousePressEvent = lambda event: self.select(block)
        block.currentFrame = layout
        layout.addWidget(block)

        self.initWidth += 15
        self.initColor += 1
        if self.initColor == 3:
            self.initColor = 0
        self.count = 0
        self.label.setText('시행횟수: ' + str(self.count))
        

    def move(self, widget):
        if not self.selected:
            print('선택된 위젯 없음')
            return
        bl = self.selected
        if bl.currentFrame.parentWidget() == widget:
            print('같은 기둥 선택')
            return
        if widget.children()[0].count():
            if widget.children()[0].itemAt(0).widget().rect().width() < self.selected.rect().width():
                print('작은 블럭 위에 큰 블럭')
                self.selected = None
                return
        bl.currentFrame.removeWidget(bl)
        widget.children()[0].insertWidget(0,bl)
        bl.currentFrame = widget.children()[0]
        self.selected = None
        self.count += 1
        self.label.setText('시행횟수: ' + str(self.count))

    def select(self, widget):
        if self.selected:
            print('배경대신 블럭클릭')
            self.move(widget.currentFrame.parentWidget())
            return
        if not widget == widget.currentFrame.itemAt(0).widget():
            print('맨 위 블럭이 아님')
            return
        self.selected = widget

    def reset(self, event):
        for i in reversed(range(self.ly1.count())): 
            self.ly1.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.ly2.count())): 
            self.ly2.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.ly3.count())): 
            self.ly3.itemAt(i).widget().setParent(None)

        self.initWidth = 100
        self.initColor = 0


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())