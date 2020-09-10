from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
import operator
###############################################################
class WinDin(qw.QDialog):
    def __init__(self):
        super(WinDin, self).__init__()
        self.setLayout(qw.QVBoxLayout())
        self.setFixedSize(500,500)

        button_00 = qw.QPushButton('death')
        self.layout().addWidget(button_00)

        ##################################################
        # IM USING A QLABEL FOR EASY LOOK THROUGH ...
        #
        self._mainWidget = qw.QLabel(self)
        self._mainWidget.setFixedSize(500,500)
        self._mainWidget.setStyleSheet("background-color: rgba(255,0,0,5)")

        lay_out = qw.QHBoxLayout(self._mainWidget)
        button_01 = qw.QPushButton('trick')

        lay_out.setAlignment(qc.Qt.AlignBottom)
        lay_out.addWidget(button_01)

        self.settingMask()
    ############################################################################################################################################
    def settingMask(self):
        ### SAW THIS EXAMPLE IN OTHER FORO IN C++

        frame_geometry = self._mainWidget.frameGeometry()
        wd_geo = self._mainWidget.geometry()
        child_reg = self._mainWidget.childrenRegion()


        ##############################
        # TESTING WITH OPERATOR MODULE I GET AND ERRROR . 'PySide.QtCore.QRect' is not iterable
        #
        #this = operator.__contains__(wd_geo,wd_geo)
        #self._mainWidget.setMask(this)

        region = qg.QRegion(frame_geometry)
        region -= qg.QRegion(wd_geo)
        region += qg.QRegion(child_reg)
        self._mainWidget.setMask(region)

        ###
        ###
        ###  THIS WAY I GET : NotImplementedError: reverse operator not implemented.

##########################################
def main():
    import sys
    qtApp=qw.QApplication(sys.argv)
    myWinPos=WinDin()
    myWinPos.show()
    sys.exit(qtApp.exec_())

if __name__=="__main__":
    main()