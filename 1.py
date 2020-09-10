from PyQt5 import QtCore, QtGui, QtWidgets


class Grabber(QtWidgets.QWidget):
    dirty = True
    def __init__(self):
        super(Grabber, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        # limit widget AND layout margins
        self.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.grabWidget = QtWidgets.QWidget()
        self.grabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.grabWidget)

        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

    def updateMask(self):
        frameRect = self.frameGeometry() #프레임오프셋
        print(frameRect)

        grabGeometry = self.grabWidget.geometry() #그랩오프셋
        print(grabGeometry)
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))
        print(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))

        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()

        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        grabGeometry.moveTopLeft(QtCore.QPoint(0, 0))

        region = QtGui.QRegion(frameRect.adjusted(left, top, right, bottom))
        region -= QtGui.QRegion(grabGeometry)
        self.setMask(region)



    def resizeEvent(self, event):
        super(Grabber, self).resizeEvent(event)
        if not self.dirty:
            self.updateMask()

    def paintEvent(self, event):
        super(Grabber, self).paintEvent(event)
        if self.dirty:
            self.updateMask()
            self.dirty = False
        frameRect = self.frameGeometry() #프레임오프셋

        grabGeometry = self.grabWidget.geometry() #그랩오프셋
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))
        print(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))

        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()

        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        grabGeometry.moveTopLeft(QtCore.QPoint(0, 0))

        region = QtGui.QRegion(frameRect.adjusted(left, top, right, bottom))
        print(frameRect.adjusted(left, top, right, bottom))
        region -= QtGui.QRegion(grabGeometry)
        self.setMask(region)
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    grabber = Grabber()
    grabber.show()
    sys.exit(app.exec_())