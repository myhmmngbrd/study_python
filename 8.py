from PyQt5 import QtGui, QtCore, QtWidgets
import pyautogui as ps

keymap = {}
for key, value in vars(QtCore.Qt).items():
    if isinstance(value, QtCore.Qt.Key):
        keymap[value] = key.partition('_')[2]

eventmap = {}
for key, value in vars(QtCore.QEvent).items():
    if isinstance(value, QtCore.QEvent.Type):
        eventmap[value] = key

def valueToKey(event):
    sequence = []
    key = keymap.get(event.key(), event.text())
    sequence.append(key)
    return '+'.join(sequence)

def valueToType(event):
    sequence = []
    key = eventmap.get(event.type())
    sequence.append(key)
    return '+'.join(sequence)

class Main(QtWidgets.QWidget):
    pressedKeys = []
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

    def addTask(self, taskType: str, options = None, unit: str = ''):
        task = Task()
        task.setTask(taskType, options, unit)
        self.board.addWidget(task)

        # shift 눌린 경우,
        # 이미 여러개 선택된 경우,
        # 새로 눌린 위젯이 기존에 눌린 위젯 영역보다 위에 있는 경우(이미 눌린 범위에 포함되어있으면 리턴),
        # 선택 영역 가장 위 위젯 - 1 ~ 선택된 위젯까지 새로 넣음
        # 새로 눌린 위젯이 기존 영역보다 아래에 있는 경우,
        # 선택 영역 가장 아래 위젯 + 1 ~ 선택된 위젯까지 새로 넣음

        # ctrl 눌린 경우,
        # 새로 누른 위젯을 선택 영역에 추가

        # 이렇게 구현했을 때,
        # shift 영역에 빈 공간이 있는 경우,
        # 공백이 채워지지 않음 -> 이렇게 구현해야 ctrl 기능과 섞어쓰기 적합하다 사료됨


    def keyPressEvent(self, event):
        self.pressedKeys.append(str(valueToKey(event)))

    def keyReleaseEvent(self,event):
        if self.pressedKeys:
            print(self.pressedKeys)
            self.pressedKeys = []

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

class Task(QtWidgets.QLabel):
    taskType = ''
    hovered = False
    options = {}
    def __init__(self):
        super().__init__()
        self.installEventFilter(self)

    def setTask(self, taskType: str, options = None, unit: str = ''):
        text = taskType
        if type(options) == type({}):
            for key, value in options.items():
                #value: int
                text += ', ' + key + ': ' + str(value) + unit
        elif type(options) == type([]):
            for value in options:
                #value: int
                text += ', ' + str(value) + unit
        self.setText(text)

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == QtCore.QEvent.Enter:
                self.hovered = True
            elif event.type() == QtCore.QEvent.Leave:
                self.hovered = False

        return super(Task, self).eventFilter(obj, event)

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