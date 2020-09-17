import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    offset = 0
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        layout.addStretch(1)
        label = QLabel("미지정")
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        self.label = label
        btn = QPushButton("값 얻어오기")
        btn.clicked.connect(self.onButtonClicked)
        layout.addWidget(label)
        layout.addWidget(btn)
        layout.addStretch(1)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    def onButtonClicked(self):
        win = SubWindow()
        r = win.showModal()
        #if r:
        #    text = win.edit.text()
        #    self.label.setText(text)

class SubWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Sub Window')
        self.setGeometry(100, 100, 200, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)
        edit = QLineEdit()
        font = edit.font()
        font.setPointSize(20)
        edit.setFont(font)
        self.edit = edit
        subLayout = QHBoxLayout()
        
        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)
        layout.addWidget(edit)
        
        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        layout.addLayout(subLayout)
        layout.addStretch(1)
        self.setLayout(layout)
    def onOKButtonClicked(self):
        self.accept()
    def onCancelButtonClicked(self):
        self.reject()
    def showModal(self):
        return super().exec_()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())