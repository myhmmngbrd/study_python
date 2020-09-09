from PyQt5 import QtCore, QtGui, QtWidgets


class Grabber(QtWidgets.QWidget):
    dirty = True
    def __init__(self):
        super(Grabber, self).__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint) #항상 위에

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        # limit widget AND layout margins
        #self.setContentsMargins(100, 100, 100, 100)
        layout.setContentsMargins(100, 100, 100, 100)
        #layout.setSpacing(0)
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    grabber = Grabber()
    grabber.show()
    sys.exit(app.exec_())