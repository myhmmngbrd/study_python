from PyQt5 import QtGui, QtCore, QtWidgets
import pyautogui as ps

class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500,500)
    
        ly = QtWidgets.QHBoxLayout()
        self.setLayout(ly)

        board = self.board = Board()
        ly.addWidget(board)

        tools = self.tools = Tools()
        tools.setFixedWidth(120)
        ly.addWidget(tools)

        #click
        clickbtn = QtWidgets.QPushButton('click')
        clickbtn.clicked.connect(lambda event: self.measure('click'))
        tools.addWidget(clickbtn)
        
        #mousemove
        mousemovebtn = QtWidgets.QPushButton('mousemove')
        mousemovebtn.clicked.connect(lambda event: self.measure('mousemove'))
        tools.addWidget(mousemovebtn)
       
        #sleep
        sleepwidget = QtWidgets.QWidget()
        sleepwidget.setContentsMargins(0,0,0,0)
        sleeplayout = QtWidgets.QHBoxLayout()
        sleeplayout.setContentsMargins(0,0,0,0)
        sleepwidget.setLayout(sleeplayout)

        sleepinput = QtWidgets.QLineEdit()
        sleepinput.setFixedWidth(30)
        sleeplayout.addWidget(sleepinput)
        sleepbtn = QtWidgets.QPushButton('sleep')
        sleepbtn.clicked.connect(lambda event: self.measure('sleep'))
        sleeplayout.addWidget(sleepbtn)

        tools.addWidget(sleepwidget)

        editbtn = QtWidgets.QPushButton('edit')
        editbtn.clicked.connect(lambda event: self.measure())
        editbtn.setDisabled(True)
        board.dependentbtns.append(editbtn)
        tools.addWidget(editbtn)

        copybtn = QtWidgets.QPushButton('copy')
        copybtn.setDisabled(True)
        copybtn.clicked.connect(lambda event: self.copy())
        board.dependentbtns.append(copybtn)
        tools.addWidget(copybtn)

        removebtn = QtWidgets.QPushButton('remove')
        removebtn.setDisabled(True)
        removebtn.clicked.connect(lambda event: self.remove())
        board.dependentbtns.append(removebtn)
        tools.addWidget(removebtn)

        moveupbtn = QtWidgets.QPushButton('moveup')
        moveupbtn.setDisabled(True)
        moveupbtn.clicked.connect(lambda event: self.moveup())
        board.dependentbtns.append(moveupbtn)
        tools.addWidget(moveupbtn)

        movedownbtn = QtWidgets.QPushButton('movedown')
        movedownbtn.setDisabled(True)
        movedownbtn.clicked.connect(lambda event: self.movedown())

        board.dependentbtns.append(movedownbtn)
        tools.addWidget(movedownbtn)

    def measure(self, taskType = None):
        if not taskType:
            task = self.board.selected
            taskType = task.taskType
            task.setTask(taskType,{'x': 3, 'y': 4})
        else:
            task = Task()
            task.setTask(taskType,{'x': 1, 'y': 2})
            self.board.addWidget(task)

        if not task: #선택된 위젯이 없는데 이 함수가 호출된 경우
            print('버튼이 비활성화 되어 있어야 합니다')
            return

         #측정 다이얼로그

    def copy(self):
        obj = self.board.selected
        copy = Task()
        copy.setTask(obj.taskType, obj.options)
        self.board.addWidget(copy)

    def remove(self):
        self.board.layout.removeWidget(self.board.selected)

    def moveup(self):
        obj = self.board.selected
        index = self.board.layout.indexOf(obj)
        if index == 0:
            return
        self.board.layout.removeWidget(obj)
        self.board.layout.insertWidget(index-1, obj)
        self.board.select(obj)

    def movedown(self):
        obj = self.board.selected
        index = self.board.layout.indexOf(obj)
        if index == self.board.layout.count() - 1:
            return
        wd = self.board.layout.itemAt(index + 1).widget()
        self.board.layout.removeWidget(wd)
        self.board.layout.insertWidget(index, wd)




class Board(QtWidgets.QScrollArea):
    defualtStyle = 'background:#ddd; color:black; '
    selectedStyle = 'background:#00f; color:white; '
    selected = None
    dependentbtns = []
    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        wd = QtWidgets.QWidget()
        self.setWidget(wd)

        ly = self.layout = QtWidgets.QVBoxLayout()
        ly.setAlignment(QtCore.Qt.AlignTop)
        wd.setLayout(ly)

    def addWidget(self, widget):
        widget.mouseReleaseEvent = lambda event: self.select(widget)
        widget.setStyleSheet(self.defualtStyle)
        self.layout.addWidget(widget)

    def select(self, widget):
        for i in range(self.layout.count()):
            other = self.layout.itemAt(i).widget()
            other.setStyleSheet(self.defualtStyle)
        self.selected = widget
        if not widget:
            for btn in self.dependentbtns:
                btn.setDisabled(True)
        else:
            widget.setStyleSheet(self.selectedStyle)
            for btn in self.dependentbtns:
                btn.setDisabled(False)

    def mouseReleaseEvent(self, widget):
        self.select(None)
        
class Task(QtWidgets.QLabel):
    taskType = None
    options = None
    def __init__(self):
        super().__init__()

    def setTask(self, taskType, options):
        self.taskType = taskType
        self.options = options
        
        text = taskType
        for key, value in options.items():
            text += ', ' + str(key) + ': ' + str(value)
        self.setText(text)

class Tools(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #메인 레이아웃
        ly = self.layout = QtWidgets.QVBoxLayout()
        ly.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(ly)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())