from PyQt5 import QtGui, QtCore, QtWidgets
import pyautogui as ps

keymap = {}
for key, value in vars(QtCore.Qt).items():
    if isinstance(value, QtCore.Qt.Key):
        keymap[value] = key.partition('_')[2]

#modmap = {
#    QtCore.Qt.ControlModifier: keymap[QtCore.Qt.Key_Control],
#    QtCore.Qt.AltModifier: keymap[QtCore.Qt.Key_Alt],
#    QtCore.Qt.ShiftModifier: keymap[QtCore.Qt.Key_Shift],
#    QtCore.Qt.MetaModifier: keymap[QtCore.Qt.Key_Meta],
#    QtCore.Qt.GroupSwitchModifier: keymap[QtCore.Qt.Key_AltGr],
#    QtCore.Qt.KeypadModifier: keymap[QtCore.Qt.Key_NumLock],
#}

def valueToKey(event):
    sequence = []
    #for modifier, text in modmap.items():
        #if event.modifiers() & modifier:
            #print(event.modifiers())
            #sequence.append(text)
    key = keymap.get(event.key(), event.text())
    #if key not in sequence:
    sequence.append(key)
    return '+'.join(sequence)

class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500,500)
    #layout    
        ly = QtWidgets.QHBoxLayout()
        self.setLayout(ly)

        board = self.board = Board()
        ly.addWidget(board)

        tools = self.tools = Tools()
        tools.setFixedWidth(120)
        ly.addWidget(tools)

    #click
        clickbtn = QtWidgets.QPushButton('click')
        clickbtn.clicked.connect(lambda event: self.notMeasure('click'))
        tools.addWidget(clickbtn)
        
    #mousemove
        mousemovebtn = QtWidgets.QPushButton('mousemove')
        mousemovebtn.clicked.connect(lambda event: self.measure('mousemove', 'px'))
        tools.addWidget(mousemovebtn)

    #presskey
        keybtn = QtWidgets.QPushButton('key')
        keybtn.clicked.connect(lambda event: self.measure('key'))
        tools.addWidget(keybtn)

    #capture
        capturebtn = QtWidgets.QPushButton('capture')
        capturebtn.clicked.connect(lambda event: self.measure('cature'))

    #sleep
        sleepwidget = QtWidgets.QWidget()
        sleepwidget.setContentsMargins(0,0,0,0)
        sleeplayout = QtWidgets.QHBoxLayout()
        sleeplayout.setContentsMargins(0,0,0,0)
        sleeplayout.setSpacing(0)
        sleepwidget.setLayout(sleeplayout)

        sleepinput = QtWidgets.QLineEdit()
        sleepinput.setFixedWidth(30)
        sleeplayout.addWidget(sleepinput)
        sleepbtn = QtWidgets.QPushButton('sleep')
        sleepbtn.clicked.connect(lambda event: self.sleep(sleepinput.text()))
        sleeplayout.addWidget(sleepbtn)

        tools.addWidget(sleepwidget)

    #loop
        loopwidget = QtWidgets.QWidget()
        loopwidget.setContentsMargins(0,0,0,0)
        looplayout = QtWidgets.QHBoxLayout()
        looplayout.setContentsMargins(0,0,0,0)
        looplayout.setSpacing(0)
        loopwidget.setLayout(looplayout)

        loopinput = QtWidgets.QLineEdit()
        loopinput.setFixedWidth(30)
        looplayout.addWidget(loopinput)
        loopbtn = QtWidgets.QPushButton('loop')
        loopbtn.clicked.connect(lambda event: self.loop(loopinput.text()))
        looplayout.addWidget(loopbtn)
        loopendbtn = QtWidgets.QPushButton('end')
        loopendbtn.clicked.connect(lambda event: self.notMeasure('loop_end'))
        looplayout.addWidget(loopendbtn)

        tools.addWidget(loopwidget)

    #line
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.HLine)
        hline.setStyleSheet('color:#888')
        tools.addWidget(hline)

    #modify tools

        editbtn = QtWidgets.QPushButton('edit')
        editbtn.clicked.connect(self.edit)
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
    
    #line
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.HLine)
        hline.setStyleSheet('color:#888')
        tools.addWidget(hline)

    #start
        startbtn = QtWidgets.QPushButton('start')
        startbtn.clicked.connect(lambda event: self.start())
        tools.addWidget(startbtn)

#func
    def measure(self, taskType = None, unit = ''):
        if not taskType:
            task = self.board.selected
            taskType = task.taskType
            if not task: #선택된 위젯이 없는데 이 함수가 호출된 경우
                print('버튼이 비활성화 되어 있어야 합니다')
                return
        else:
            ruler = Ruler()
            ruler.setStatus(taskType)
            r = ruler.exec_()
            if r:
                task = Task()
                task.setTask(taskType, ruler.returnValues, unit)
                self.board.addWidget(task)

    def notMeasure(self, taskType):
        task = Task()
        task.setTask(taskType, {})
        self.board.addWidget(task)

    def sleep(self, time):
        if not time.isdigit():
            return
        task = Task()
        task.setTask('sleep', [time ], 's')
        self.board.addWidget(task)

    def loop(self, count):
        if not count.isdigit():
            return
        task = Task()
        task.setTask('loop', [count ])
        self.board.addWidget(task)

    def edit(self):
        obj = self.board.selected
        taskType = obj.taskType
        ruler = Ruler()
        ruler.setStatus(taskType)
        r = ruler.exec_()
        if r:
            obj.setTask(taskType, ruler.returnValues)


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

    def start(self):
        print('start...')

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

    def setTask(self, taskType, options, unit = ''):
        self.taskType = taskType
        self.options = options
        
        text = taskType
        if type(options) == type({}):
            for key, value in options.items():
                text += ', ' + str(key) + ': ' + str(value) + unit
        elif type(options) == type([]):
            for value in options:
                text += ', ' + str(value) + unit
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

class Ruler(QtWidgets.QDialog):
    taskType = None
    returnValues = {}
    def __init__(self):
        super().__init__()

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)

        screenW = self.screenW = self.screen().geometry().width()
        screenH = self.screenH = self.screen().geometry().height()
        self.setGeometry(0,0, screenW, screenH)

        self.status = QtWidgets.QWidget(self)
        self.status.setStyleSheet('background:#333; color:#aaa')
        self.statuslayout = QtWidgets.QHBoxLayout()
        self.status.setLayout(self.statuslayout)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.2)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtCore.Qt.white)
        painter.drawRect(self.rect())

    def addWidget(self, widget):
        self.statuslayout.addWidget(widget)
    def move(self, x, y):
        self.status.move(x, y)

    def setStatus(self, taskType):
        self.taskType = taskType
        if taskType == 'mousemove':
            print('mousemove')
            x = ps.position().x
            y = ps.position().y
            self.addWidget(QtWidgets.QLabel('x: '))
            posX = self.posX = QtWidgets.QLabel(str(x))
            posX.setFixedWidth(25)
            self.addWidget(posX)
            self.addWidget(QtWidgets.QLabel(', y: '))
            posY = self.posY = QtWidgets.QLabel(str(y))
            posY.setFixedWidth(25)
            self.addWidget(posY)

            if x + 20 > self.screenW - self.status.geometry().width() - 20:
                x = x - self.status.geometry().width() - 20
            else:
                x += 20
            if y + 10 > self.screenH - self.status.geometry().height() - 40:
                y = y - self.status.geometry().height() - 40
            else:
                y += 10
            self.move(x, y)
        if taskType == 'key':
            print('key')
            self.status.setStyleSheet('background:none; color:#aaa')
            sign = QtWidgets.QLabel('Press any key')
            sign.setFont(QtGui.QFont('Arial', 30))
            sign.setFixedWidth(300)
            #sign.setAlignment(QtCore.Qt.AlignCenter)
            self.addWidget(sign)
            print(sign.geometry())
            x = self.screenW * 0.5 - sign.geometry().width() / 2
            y = self.screenH * 0.3 - self.status.geometry().height() / 2
            self.move(int(x), int(y))

    def mouseMoveEvent(self, event):
        if self.taskType == 'mousemove':
            x = event.x()
            y = event.y()
            self.posX.setText(str(x))
            self.posY.setText(str(y))
            if x + 20 > self.screenW - self.status.geometry().width() - 20:
                x = x - self.status.geometry().width() - 20
            else:
                x += 20
            if y + 10 > self.screenH - self.status.geometry().height() - 40:
                y = y - self.status.geometry().height() - 20
            else:
                y += 10
            self.move(x, y)

    def mousePressEvent(self, event):
        if self.taskType == 'mousemove':
            self.x = event.x()
            self.y = event.y()
    def mouseReleaseEvent(self, event):
        if self.taskType == 'mousemove':
            if self.x == event.x() and self.y == event.y():
                self.returnValues = {'x': self.x, 'y': self.y}
                self.accept()
    def keyPressEvent(self, event):
        if self.taskType == 'key':
            if not hasattr(self, 'keys'):
                self.keys = []
            self.keys.append(str(valueToKey(event)))
    def keyReleaseEvent(self, event):
        if self.taskType == 'key' and hasattr(self, 'keys'):
            self.returnValues = {'key': '+'.join(self.keys)}
            self.accept()
       


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
#    myapp = Ruler()
    myapp.show()

    sys.exit(app.exec_())