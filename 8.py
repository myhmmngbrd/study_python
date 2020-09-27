from PyQt5 import QtGui, QtCore, QtWidgets
import pyautogui as ps

#keymap = {}
#for key, value in vars(QtCore.Qt).items():
#    if isinstance(value, QtCore.Qt.Key):
#        keymap[value] = key.partition('_')[2]

eventmap = {}
for key, value in vars(QtCore.QEvent).items():
    if isinstance(value, QtCore.QEvent.Type):
        eventmap[value] = key

#def valueToKey(event):
#    sequence = []
#    key = keymap.get(event.key(), event.text())
#    sequence.append(key)
#    return '+'.join(sequence)

def valueToType(event):
    sequence = []
    key = eventmap.get(event.type())
    sequence.append(key)
    return '+'.join(sequence)

keymap = {}
for key, value in vars(QtCore.Qt).items():
    if isinstance(value, QtCore.Qt.Key):
        keymap[value] = key.partition('_')[2]

def valueToKey(event):
    key = keymap.get(event.key(), event.text())
    return key

class Main(QtWidgets.QWidget):
    pressedKeys = []
    selected = []
    def __init__(self):
        super().__init__()

        ly = self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(ly)

        bd = self.board = Board()
        ly.addWidget(bd)

        tl = self.tools = Tools()
        ly.addWidget(tl)

        self.addTask('type1')
        self.addTask('type2', [0])
        self.addTask('type3', {'anyattr': 1}, 'unit')
        self.addTask('type3', {'anyattr': 1}, 'unit')
        self.addTask('type3', {'anyattr': 1}, 'unit')
        self.addTask('type3', {'anyattr': 1}, 'unit')
        self.addTask('type3', {'anyattr': 1}, 'unit')
        self.addTask('type3', {'anyattr': 1}, 'unit')
        self.addTask('type3', {'anyattr': 1}, 'unit')
        self.addTask('type3', {'anyattr': 1}, 'unit')

        #add
        self.clickButton = QtWidgets.QPushButton('click')
        tl.addWidget(self.clickButton)

        self.sleepButton = QtWidgets.QPushButton('sleep')
        tl.addWidget(self.sleepButton)

        self.loopStartButton = QtWidgets.QPushButton('loop')
        tl.addWidget(self.loopStartButton)

        self.loopEndButton = QtWidgets.QPushButton('loop_end')
        tl.addWidget(self.loopEndButton)

        tl.addLine()

        #edit
        ebtn = self.editButton = QtWidgets.QPushButton('edit')
        ebtn.setDisabled(True)
        tl.addWidget(ebtn)

        pbtn = self.copyButton = QtWidgets.QPushButton('copy')
        pbtn.setDisabled(True)
        tl.addWidget(pbtn)

        rbtn = self.removeButton = QtWidgets.QPushButton('remove')
        rbtn.setDisabled(True)
        tl.addWidget(rbtn)

        ubtn = self.moveUpButton = QtWidgets.QPushButton('moveup')
        ubtn.setDisabled(True)
        tl.addWidget(ubtn)

        dbtn = self.moveDownButton = QtWidgets.QPushButton('movedown')
        dbtn.setDisabled(True)
        tl.addWidget(dbtn)

        tl.addLine()

        #start

        sbtn = self.startButton = QtWidgets.QPushButton('start')
        tl.addWidget(sbtn)

        

    def addTask(self, taskType: str, options = None, unit: str = ''):
        task = Task()
        task.setTask(taskType, options, unit)
        task.mousePressEvent = lambda event: self.select(task)
        task.mouseDoubleClickEvent = lambda event: task.change()
        self.board.addWidget(task)

    def keyPressEvent(self, event):
        self.pressedKeys.append(str(valueToKey(event)))

    def keyReleaseEvent(self,event):
        if self.pressedKeys:
            print(self.pressedKeys)
            self.pressedKeys = []

    def mousePressEvent(self, event):
        self.select(None)
        self.setFocus()

    def select(self, task):
        tasks = []
        for i in range(self.board.layout.count()):
            tasks.append(self.board.layout.itemAt(i).widget())
        defaultStyle = 'background: #ddd; color: #000;'
        selectedStyle = 'background: #00f; color: #ddd;'
        taskindex = self.board.layout.indexOf(task)
        if self.selected:
            lastindex = self.board.layout.indexOf(self.selected[len(self.selected) - 1])
        else:
            lastindex = 0
        # 단일 선택
        if not self.pressedKeys:
            for value in tasks:
                value.setStyleSheet(defaultStyle)
            if not task: # 배경 클릭: 모든 선택영역 취소
                self.selected = []
            else: # 라벨 클릭
                task.setStyleSheet(selectedStyle)
                self.selected = [task]
        # 다중 선택
        elif self.pressedKeys: # control or shift
            if not task: # 배경 클릭: 함수 스킵
                return
            if QtCore.Qt.Key_Shift in self.pressedKeys:
                if not QtCore.Qt.Key_Control in self.pressedKeys:
                    for value in tasks:
                        value.setStyleSheet(defaultStyle)
                        self.selected = []
                if taskindex < lastindex: # 정방향 append
                    for i in range(taskindex, lastindex + 1):
                        if tasks[i] in self.selected:
                            self.selected.remove(tasks[i])
                        tasks[i].setStyleSheet(selectedStyle)
                        self.selected.append(tasks[i])
                else: # 역순 append
                    for i in range(lastindex, taskindex + 1):
                        i = lastindex - i + taskindex # i를 역순으로
                        if tasks[i] in self.selected:
                            self.selected.remove(tasks[i])
                        tasks[i].setStyleSheet(selectedStyle)
                        self.selected.append(tasks[i])
            elif QtCore.Qt.Key_Control in self.pressedKeys:
                if task in self.selected: # 중복 클릭: 선택영역 취소
                    task.setStyleSheet(defaultStyle)
                    self.selected.remove(task)
                else: # 일반 클릭
                    task.setStyleSheet(selectedStyle)
                    self.selected.append(task)
        self.activeButtons()
    
    def activeButtons(self):
        ly = self.board.layout

        if len(self.selected) == 1:
            index = ly.indexOf(self.selected[0])
            self.editButton.setDisabled(False)
            self.removeButton.setDisabled(False)
            self.moveUpButton.setDisabled(False)
            self.moveDownButton.setDisabled(False)
            if index == 0: # 맨 위칸인 경우 moveup 비활성화
                self.moveUpButton.setDisabled(True)
            elif index == ly.count() - 1: # 맨 아래칸인 경우 movedown 비활성화
                self.moveDownButton.setDisabled(True)

        elif len(self.selected) > 1:
            self.removeButton.setDisabled(False)
            first = ly.count() - 1
            last = 0
            for value in self.selected:
                index = ly.indexOf(value)
                if index < first:
                    first = index
                if index > last:
                    last = index
            self.moveUpButton.setDisabled(False)
            self.moveDownButton.setDisabled(False)
            if first == 0:
                self.moveUpButton.setDisabled(True)
            if last == ly.count() - 1:
                self.moveDownButton.setDisabled(True)

        else:
            self.editButton.setDisabled(True)
            self.removeButton.setDisabled(True)
            self.moveUpButton.setDisabled(True)
            self.moveDownButton.setDisabled(True)
            

                    
class Board(QtWidgets.QScrollArea):
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
        self.layout.addWidget(widget)

    


class Tools(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        ly = self.layout = QtWidgets.QVBoxLayout()
        ly.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(ly)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addLine(self):  
        hline = QtWidgets.QFrame()
        hline.setFrameShape(QtWidgets.QFrame.HLine)
        hline.setStyleSheet('color:#888')
        self.layout.addWidget(hline)

class Task(QtWidgets.QWidget):
    taskType = ''
    hovered = False
    options = {}
    values = []
    inputs = []
    def __init__(self):
        super().__init__()

        self.options = {}
        self.values = []
        self.inputs = []

        ly = self.layout = QtWidgets.QHBoxLayout()
        ly.setAlignment(QtCore.Qt.AlignLeft)
        ly.setSpacing(0)
        self.setLayout(ly)


    def setTask(self, taskType: str, options = None, unit: str = ''):
        #text = taskType
        typeLabel = QtWidgets.QLabel(taskType)
        self.layout.addWidget(typeLabel)


        if type(options) == type({}):
            for key, value in options.items():
                #value: int
                #text += ', ' + key + ': ' + str(value) + unit
                keyLabel = QtWidgets.QLabel(', ' + key + ': ')
                self.layout.addWidget(keyLabel)
                valueLabel = QtWidgets.QLabel(str(value))
                self.values.append(valueLabel)
                self.layout.addWidget(valueLabel)
                valueInput = QtWidgets.QLineEdit(str(value))
                valueInput.setVisible(False)
                valueInput.returnPressed.connect(self.valueChanged)
                valueInput.focusOutEvent = lambda event: self.valueChanged(valueInput)
                self.inputs.append(valueInput)
                self.layout.addWidget(valueInput)
                if unit:
                    unitLabel = QtWidgets.QLabel(unit)
                    self.layout.addWidget(unitLabel)
        elif type(options) == type([]):
            for value in options:
                keyLabel = QtWidgets.QLabel(', ')
                self.layout.addWidget(keyLabel)
                valueLabel = QtWidgets.QLabel(str(value))
                self.values.append(valueLabel)
                self.layout.addWidget(valueLabel)
                valueInput = QtWidgets.QLineEdit(str(value))
                valueInput.setVisible(False)
                valueInput.returnPressed.connect(self.valueChanged)
                valueInput.focusOutEvent = lambda event: self.valueChanged(valueInput)
                self.inputs.append(valueInput)
                self.layout.addWidget(valueInput)
                if unit:
                    unitLabel = QtWidgets.QLabel(unit)
                    self.layout.addWidget(unitLabel)
                #value: int
                #text += ', ' + str(value) + unit
        #self.setText(text)

    def change(self):
        print(self.values)
        if not self.values:
            return
        for value in self.values:
            value.setVisible(False)
        for edit in self.inputs:
            edit.setVisible(True)

    def valueChanged(self, edit = None):
        if not edit:
            edit = self.sender()
        index = self.inputs.index(edit)
        value = self.values[index]
        if not edit.text().isdigit():
            edit.setText(value.text())
        value.setText(str(edit.text()))
        edit.setVisible(False)
        value.setVisible(True)

class Ruler(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)

        screenW = self.screenW = self.screen().geometry().width()
        screenH = self.screenH = self.screen().geometry().height()
        self.setGeometry(0,0, screenW, screenH)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())