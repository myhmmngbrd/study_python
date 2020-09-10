from PyQt5 import QtGui, QtCore, QtWidgets
import time

class MyApp(QtWidgets.QWidget):
    def hidden(self):
        self.setHidden(not self.isHidden())
    def sub(self):
        self.subwindow = SubApp()
        self.subwindow.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)


    myapp = MyApp()


    myapp.sub()
    myapp.show()


    sys.exit(app.exec_())