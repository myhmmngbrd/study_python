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

        test = QtWidgets.QPushButton('add')
        test.clicked.connect(self.addCommand)
        ly.addWidget(test)
    
    def addCommand(self):
        self.board.addWidget(QtWidgets.QLabel('abc'))

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

    def addWidget(self, widget):
        self.layout.addWidget(widget)

class Tools(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        ly = self.layout = QtWidgets.QVBoxLayout()
        ly.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(ly)
        


class Command(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)


class Sub(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        print('set sub widget')

        self.setStyleSheet('background:red')

        ly = QtWidgets.QHBoxLayout()
        self.setLayout(ly)

        ly.addWidget(QtWidgets.QPushButton('test'))
        ly.addWidget(QtWidgets.QPushButton('test'))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())