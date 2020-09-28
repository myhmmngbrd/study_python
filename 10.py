from PyQt5 import QtGui, QtCore, QtWidgets

keymap = {}
for key, value in vars(QtCore.Qt).items():
    if isinstance(value, QtCore.Qt.Key):
        keymap[value] = key.partition('_')[2]

modmap = {
    QtCore.Qt.ControlModifier: keymap[QtCore.Qt.Key_Control],
    QtCore.Qt.AltModifier: keymap[QtCore.Qt.Key_Alt],
    QtCore.Qt.ShiftModifier: keymap[QtCore.Qt.Key_Shift],
    QtCore.Qt.MetaModifier: keymap[QtCore.Qt.Key_Meta],
    QtCore.Qt.GroupSwitchModifier: keymap[QtCore.Qt.Key_AltGr],
    QtCore.Qt.KeypadModifier: keymap[QtCore.Qt.Key_NumLock],
}

def valueToKey(event):
    sequence = []
    for modifier, text in modmap.items():
        if event.modifiers() & modifier:
            sequence.append(text)
    key = keymap.get(event.key(), event.text())
    if key not in sequence:
        sequence.append(key)
    return '+'.join(sequence)

keys = {}
for key, value in vars(QtCore.Qt).items():
    if isinstance(value, QtCore.Qt.Key):
        keys[value] = key.partition('_')[2]

class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.editingTask = None
        self.pressedKeys = []

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.resize(500,500)

        #board widgets
        self.board = QtWidgets.QScrollArea()
        self.board.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.board.setWidgetResizable(True)
        bdwidget = QtWidgets.QWidget()
        self.board.setWidget(bdwidget)
        self.board.layout = QtWidgets.QVBoxLayout()
        self.board.layout.setAlignment(QtCore.Qt.AlignTop)
        self.board.layout.setSpacing(0)
        bdwidget.setLayout(self.board.layout)
        
        #tools widgets
        self.tools = QtWidgets.QWidget()
        self.tools.layout = QtWidgets.QVBoxLayout()
        self.tools.layout.setAlignment(QtCore.Qt.AlignTop)
        self.tools.setLayout(self.tools.layout)
        self.initTools()

        #layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.board)
        self.layout.addWidget(self.tools)
        self.setLayout(self.layout)

        #test
        self.addTask('click')
        self.addTask('sleep', [5])
        self.addTask('mousemove', {'x': 500, 'y': 400})

        self.installEventFilter(self)
        self.board.installEventFilter(self)
        self.tools.installEventFilter(self)

    def initTools(self):
        tl = self.tools.layout
        #add
        clickbtn = QtWidgets.QPushButton('click')
        tl.addWidget(clickbtn)

        tl.addWidget(HLine())
        
        #edit
        editbtn = QtWidgets.QPushButton('edit')
        tl.addWidget(editbtn)

        tl.addWidget(HLine())

        #start
        startbtn = QtWidgets.QPushButton('start')
        tl.addWidget(startbtn)
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            self.pressedKeys.append(keys[event.key()])
            return True
        elif event.type() == QtCore.QEvent.KeyRelease:
            if not self.pressedKeys:
                return True
            print(self.pressedKeys)
            self.pressedKeys = []
            return True
        elif isinstance(obj, Task):
            if event.type() == QtCore.QEvent.MouseButtonPress:
                return True
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                self.editTask(obj)
                return True
        elif obj is self.board:
            if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonDblClick:
                self.saveTask()
        
        return super(Main, self).eventFilter(obj, event)

    def addTask(self, taskType: str, options = None):
        task = Task()
        task.setStatus({
            'editable': True,
        })
        task.init(taskType, options)
        task.installEventFilter(self)
        #task.mousePressEvent = lambda event: print('task')
        #task.mouseDoubleClickEvent = lambda event: self.editTask(task)
        self.board.layout.addWidget(task)

    def editTask(self, task):
        if not task.status()['editable'] or not task.options():
            return
        self.editingTask = task
        task.setStatus({ 'edit': True })
        task.edit()
        self.disableEdit(True)

    def saveTask(self):
        if not self.editingTask:
            return
        task = self.editingTask
        if not task.status()['edit']:
            return
        self.editingTask = None
        task.setStatus({ 'edit': False })
        task.save()
        self.disableEdit(False)

    def disableEdit(self, boolean: bool):
        ly = self.board.layout
        for i in range(ly.count()):
            task = ly.itemAt(i).widget()
            task.setStatus({
                'editable': not boolean,
                'moveableUp': not boolean,
                'moveableDown': not boolean,
            })

class Task(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.__taskType = ''
        self.__options = {}
        self.__status = {
            'edit': False,
            'editable': False,
            'moveableUp': False,
            'moveableDown': False,
        }
        self.setFixedHeight(20)
        self.setContentsMargins(0,0,0,0)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)

    def init(self, taskType: str = '', options = None):
        self.clear()
        if not taskType:
            taskType = self.__taskType
        else:
            self.__taskType = taskType
        if not options and self.__options:
            options = self.__options
        elif options and not self.__options:
            self.__options = options
        ly = self.layout
        text = taskType
        if options:
            if type(options) is type({}):
                for key, value in options.items():
                    text += ', ' + key + ': ' + str(value)
            elif type(options) is type([]):
                for value in options:
                    text += ', ' + str(value)
        ly.addWidget(QtWidgets.QLabel(text))

    def clear(self):
        ly = self.layout
        for i in reversed(range(ly.count())):
            widget = ly.takeAt(i).widget()
            widget.deleteLater()

    def edit(self):
        print(self.__status['editable'])
        if not self.__taskType:
            print('Task().edit 함수가 인스턴스 초기화 이전에 호출됨')
            return
        if not self.__options:
            print('편집 불가능한 Task 인스턴스의 edit 함수 호출')
            return
        if not self.__status['editable']:
            print('편집 불가능한 Task')
            return
        self.clear()
        ly = self.layout
        ly.addWidget(QtWidgets.QLabel(self.__taskType))
        if type(self.__options) is type({}):
            for key, value in self.__options.items():
                ly.addWidget(QtWidgets.QLabel(', ' + key + ': '))
                frame = QtWidgets.QWidget()
                frame.setFixedWidth(40)
                edit = QtWidgets.QLineEdit(str(value), frame)
                edit.setFixedWidth(40)
                edit.key = key
                ly.addWidget(frame)
        elif type(self.__options) is type([]):
            for value in self.__options:
                ly.addWidget(QtWidgets.QLabel(', '))
                frame = QtWidgets.QWidget()
                frame.setFixedWidth(40)
                edit = QtWidgets.QLineEdit(str(value), frame)
                edit.setFixedWidth(40)
                ly.addWidget(frame)

    def save(self):
        if not self.__taskType:
            print('Task().save 함수가 인스턴스 초기화 이전에 호출됨')
            return
        if not self.__options:
            print('편집 불가능한 Task 인스턴스의 save 함수 호출')
            return
        ly = self.layout
        index = 0
        for i in range(ly.count()):
            widget = ly.itemAt(i).widget()
            if not isinstance(widget, QtWidgets.QLabel):
                edit = widget.children()[0]
                if edit.text().isdigit():
                    if type(self.__options) is type({}):
                        self.__options[edit.key] = edit.text()
                    elif type(self.__options) is type([]):
                        self.__options[index] = edit.text()
                        index = index + 1
        self.init()

    #gets and sets
    def setStatus(self, status: dict):
        for key, value in status.items():
            if not key in self.__status:
                print('올바른 status를 입력해주세요')
                return
        for key, value in status.items():
            self.__status[key] = value
    def status(self):
        returnValue = {}
        for key, value in self.__status.items():
            returnValue[key] = value
        return returnValue
    def options(self):
        if not self.__options:
            return None
        elif type(self.__options) is type({}):
            returnValue = {}
            for key, value in self.__options.items():
                returnValue[key] = value
        elif type(self.__options) is type([]):
            returnValue = []
            for value in self.__options:
                returnValue.append(value)
        return returnValue
    def taskType(self):
        return self.__taskType

class HLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setStyleSheet('color:#888')


        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())