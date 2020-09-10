from PyQt5 import QtGui, QtCore, QtWidgets
import time

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.grabWidget = QtWidgets.QWidget()
        self.grabWidget.setStyleSheet("background-color: #f00")
        self.grabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.grabWidget)

        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)


    def paintEvent(self, event):
        frameRect = self.frameGeometry()
        grabGeometry = self.grabWidget.geometry()
        print(grabGeometry)
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))
        print(grabGeometry)

        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()

        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        grabGeometry.moveTopLeft(QtCore.QPoint(0, 0))

        region = QtGui.QRegion(frameRect.adjusted(left, top, right, bottom))
        #region -= QtGui.QRegion(grabGeometry)
        self.setMask(region)



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())