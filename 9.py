from PyQt5 import QtGui, QtCore, QtWidgets


class Main(QtWidgets.QWidget):
    pressed = []
    selected = []
    def __init__(self):
        super().__init__()


        self.pressed = []
        self.selected = []

        self.resize(500,500)

        bd = self.board = Board()
        tl = self.tools = Tools()

        ly = self.layout = QtWidgets.QHBoxLayout()

        ly.addWidget(bd)
        ly.addWidget(tl)

        self.setLayout(ly)

        self.addTask('click')
        self.addTask('sleep', [500], 's')
        self.addTask('mousemove', {'x': 300, 'y': 500}, 'px')

        bd.mousePressEvent = self.unselect

    def addTask(self, taskType: str, options = None, unit: str = ''):
        task = Task()
        task.set(taskType, options, unit)
        task.mousePressEvent = lambda event: self.select(task)
        self.board.add(task)

    def keyPressEvent(self, event):
        self.pressed.append(event.key())

    def keyReleaseEvent(self,event):
        if self.pressed:
            self.pressed = []

    def saveAll(self):
        ly = self.board.layout
        for i in range(ly.count()):
            task = ly.itemAt(i).widget()
            task.saveAll()

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
        if not self.pressed:
            for value in tasks:
                value.setStyleSheet(defaultStyle)
            if not task: # 배경 클릭: 모든 선택영역 취소
                self.selected = []
            else: # 라벨 클릭
                task.setStyleSheet(selectedStyle)
                self.selected = [task]
        # 다중 선택
        elif self.pressed: # control or shift
            if not task: # 배경 클릭: 함수 스킵
                return
            if QtCore.Qt.Key_Shift in self.pressed:
                if not QtCore.Qt.Key_Control in self.pressed:
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
            elif QtCore.Qt.Key_Control in self.pressed:
                if task in self.selected: # 중복 클릭: 선택영역 취소
                    task.setStyleSheet(defaultStyle)
                    self.selected.remove(task)
                else: # 일반 클릭
                    task.setStyleSheet(selectedStyle)
                    self.selected.append(task)

        self.setButton()

    def unselect(self, event): #board 배경클릭시 실행
        self.saveAll()
        self.select(None)

    def setButton(self): #select 함수 끄트머리에 실행
        print(1)

class Board(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        wd = QtWidgets.QWidget()
        self.setWidget(wd)

        ly = self.layout = QtWidgets.QVBoxLayout()
        ly.setAlignment(QtCore.Qt.AlignTop)
        ly.setSpacing(10)
        wd.setLayout(ly)

    def add(self, widget):
        self.layout.addWidget(widget)

    def remove(self, widget):
        self.layout.removeWidget(widget)
        widget.deleteLater()

    def move(self, index, widget):
        oldindex = self.layout.indexOf(widget)
        print(oldindex)


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
    labels = []
    inputs = []
    def __init__(self):
        super().__init__()
        self.labels = []
        self.inputs = []
        
        self.setStyleSheet('background:#ddd')
        self.setFixedHeight(20)
        self.setContentsMargins(0,0,0,0)


        ly = self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(ly)
        ly.setAlignment(QtCore.Qt.AlignLeft)
        ly.setContentsMargins(0,0,0,0)
        ly.setSpacing(0)

    def set(self, taskType: str, options = None, unit: str = ''):
        self.layout.addWidget(QtWidgets.QLabel(taskType))
        if options:
            if type(options) is type({}): # type, x: a, y: b
                for key, value in options.items():
                    label = QtWidgets.QLabel(str(value))

                    inputframe = QtWidgets.QWidget()
                    inputframe.setFixedWidth(50)
                    inputframe.setVisible(False)
                    inputbox = QtWidgets.QLineEdit(str(value), inputframe)
                    inputbox.editingFinished.connect(self.save)
                    
                    self.layout.addWidget(QtWidgets.QLabel(', ' + key + ': '))
                    self.layout.addWidget(label)
                    self.layout.addWidget(inputframe)
                    self.layout.addWidget(QtWidgets.QLabel(unit))

                    self.labels.append(label)
                    self.inputs.append(inputframe)
            elif type(options) is type([]): # type, a, b
                for value in options:
                    label = QtWidgets.QLabel(str(value))

                    inputframe = QtWidgets.QWidget()
                    inputframe.setFixedWidth(50)
                    inputframe.setVisible(False)
                    inputbox = QtWidgets.QLineEdit(str(value), inputframe)
                    inputbox.editingFinished.connect(self.save)

                    self.layout.addWidget(QtWidgets.QLabel(', '))
                    self.layout.addWidget(label)
                    self.layout.addWidget(inputframe)
                    self.layout.addWidget(QtWidgets.QLabel(unit))

                    self.labels.append(label)
                    self.inputs.append(inputframe)

    def mouseDoubleClickEvent(self, event):
        self.editAll()

    def editAll(self):
        if self.labels:
            for value in self.labels:
                value.setVisible(False)
            for value in self.inputs:
                value.setVisible(True)

    def saveAll(self):
        if self.inputs:
            for value in self.inputs:
                index = self.inputs.index(value)
                inputbox = value.children()[0]
                label = self.labels[index]
                if not inputbox.text().isdigit():
                    inputbox.setText(label.text())
                else: 
                    label.setText(inputbox.text())
                value.setVisible(False)
            for value in self.labels:
                value.setVisible(True)

    def save(self, inputbox = None):
        if not inputbox:
            inputbox = self.sender()
        index = self.inputs.index(inputbox.parentWidget())
        label = self.labels[index]
        if not inputbox.text().isdigit():
            inputbox.setText(label.text())
        else: 
            label.setText(inputbox.text())
        label.setVisible(True)
        inputbox.parentWidget().setVisible(False)



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())