from PyQt5 import QtGui, QtCore, QtWidgets

events = {}
for key, value in vars(QtCore.QEvent).items():
    if isinstance(value, QtCore.QEvent.Type):
        events[value] = key

keys = {}
for key, value in vars(QtCore.Qt).items():
    if isinstance(value, QtCore.Qt.Key):
        keys[value] = key.partition('_')[2]

class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.pressedKeys = []
        self.lastSelectedTask = None

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
        clickbtn.clicked.connect(self.addClick)
        tl.addWidget(clickbtn)

        sleepbtn = QtWidgets.QPushButton('sleep')
        sleepbtn.clicked.connect(self.addSleep)
        tl.addWidget(sleepbtn)

        loopbtn = QtWidgets.QPushButton('loop')
        loopbtn.clicked.connect(self.addLoopStart)
        tl.addWidget(loopbtn)

        loopendbtn = QtWidgets.QPushButton('loopend')
        loopendbtn.clicked.connect(self.addLoopEnd)
        tl.addWidget(loopendbtn)


        tl.addWidget(HLine())
        
        #edit
        editbtn = QtWidgets.QPushButton('edit')
        tl.addWidget(editbtn)

        removebtn = QtWidgets.QPushButton('remove')
        tl.addWidget(removebtn)

        copybtn = QtWidgets.QPushButton('copy')
        tl.addWidget(copybtn)

        moveupbtn = QtWidgets.QPushButton('moveup')
        tl.addWidget(moveupbtn)

        movedownbtn = QtWidgets.QPushButton('movedown')
        tl.addWidget(movedownbtn)



        tl.addWidget(HLine())

        #start
        startbtn = QtWidgets.QPushButton('start')
        tl.addWidget(startbtn)
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.ActivationChange:
            self.pressedKeys = []
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return and not self.pressedKeys:
                self.saveTask()
            self.pressedKeys.append(keys[event.key()])
            return True
        elif event.type() == QtCore.QEvent.KeyRelease:
            if not self.pressedKeys:
                return True
            self.pressedKeys.remove(keys[event.key()])
            return True
        elif isinstance(obj, Task):
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.selectTask(obj)
                return True
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                self.editTask(obj)
                return True
        elif obj is self.board:
            if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonDblClick:
                self.saveTask()
                if not self.pressedKeys:
                    self.clearSelection()
                    self.lastSelectedTask = None
        
        return super(Main, self).eventFilter(obj, event)

    def addTask(self, taskType: str, options = None):
        task = Task()
        task.init(taskType, options)
        if not options:
            editable = False
        else:
            editable = True
        task.setStatus({
            'selectable': True,
            'editable': editable,
        })
        task.installEventFilter(self)
        self.board.layout.addWidget(task)

        return task

    def editTask(self, task):
        if not task.status()['editable'] or not task.options():
            return
        task.edit()
        self.disableTask(True)

    def saveTask(self):
        task = None
        ly = self.board.layout
        for i in range(ly.count()):
            wd = ly.itemAt(i).widget()
            if wd.status()['edit']:
                task = wd
        if not task:
            return
        task.save()
        self.disableTask(False)

    def disableTask(self, boolean: bool):
        ly = self.board.layout
        self.clearSelection()
        for i in range(ly.count()):
            task = ly.itemAt(i).widget()
            task.setStatus({
                'selectable': not boolean,
                'editable': not boolean,
                'moveableUp': not boolean,
                'moveableDown': not boolean,
            })

    def selectTask(self, task):
        if not task.status()['selectable']:
            return
        ly = self.board.layout
        keys = self.pressedKeys
        if not keys:
            self.clearSelection()
            task.select()
            self.lastSelectedTask = task
        elif len(keys) == 1:
            if 'Control' in keys:
                task.select()
                self.lastSelectedTask = task
            if 'Shift' in keys:
                self.clearSelection()
                index = ly.indexOf(task)
                oldindex = 0
                if self.lastSelectedTask:
                    oldindex = ly.indexOf(self.lastSelectedTask)
                for i in range(min(index, oldindex), max(index, oldindex) + 1):
                    wd = ly.itemAt(i).widget()
                    wd.select()
        elif len(keys) == 2:
            if 'Control' in keys and 'Shift' in keys:
                index = ly.indexOf(task)
                if not self.lastSelectedTask:
                    return
                oldindex = ly.indexOf(self.lastSelectedTask)               
                for i in range(min(index, oldindex), max(index, oldindex) + 1):
                    wd = ly.itemAt(i).widget()
                    if not wd.status()['edit']:
                        wd.select()


    def clearSelection(self):
        ly = self.board.layout
        for i in range(ly.count()):
            task = ly.itemAt(i).widget()
            task.unselect()

    def addClick(self):
        self.addTask('click')

    def addSleep(self):
        self.addTask('sleep',[0])
    
    def addLoopStart(self):
        self.addTask('loop',[0])
    
    def addLoopEnd(self):
        self.addTask('loopend')

class Task(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.__taskType = ''
        self.__options = {}
        self.__status = {
            'edit': False,
            'selected': False,
            'selectable': False,
            'editable': False,
            'moveableUp': False,
            'moveableDown': False,
        }
        self.setFixedHeight(30)
        self.setContentsMargins(0,5,0,5)

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
        self.__status['edit'] = True
        self.clear()
        ly = self.layout
        ly.addWidget(QtWidgets.QLabel(self.__taskType))
        if type(self.__options) is type({}):
            for key, value in self.__options.items():
                ly.addWidget(QtWidgets.QLabel(', ' + key + ': '))
                frame = QtWidgets.QWidget()
                frame.setFixedWidth(40)
                edit = QtWidgets.QLineEdit(str(value), frame)
                edit.setStyleSheet('background: #fff; color: #000')
                edit.setFixedWidth(40)
                edit.key = key
                ly.addWidget(frame)
        elif type(self.__options) is type([]):
            for value in self.__options:
                ly.addWidget(QtWidgets.QLabel(', '))
                frame = QtWidgets.QWidget()
                frame.setFixedWidth(40)
                edit = QtWidgets.QLineEdit(str(value), frame)
                edit.setStyleSheet('background: #fff; color: #000')
                edit.setFixedWidth(40)
                ly.addWidget(frame)

    def save(self):
        self.__status['edit'] = False
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

    def select(self):
        self.__status['selected'] = True
        self.setStyleSheet('background: #00f; color: #ddd;')

    def unselect(self):
        self.__status['selected'] = False
        self.setStyleSheet('background: #ddd; color: #000;')

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