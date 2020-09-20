from PyQt5 import QtGui, QtCore, QtWidgets
import pyautogui as ps


#선생님
class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #종방향 메인 레이아웃
        ly = self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(ly)

        #레이아웃 1: 보드
        bd = self.board = Board()
        ly.addWidget(bd)

        #레이아웃 2: 메뉴
        me = self.menu = QtWidgets.QWidget()
        me.setFixedWidth(100)
        ly.addWidget(me)
        mely = self.memulayout = QtWidgets.QVBoxLayout()
        me.setLayout(mely)

        #클릭
        me.click = QtWidgets.QPushButton('click')
        me.click.clicked.connect(lambda event: bd.addOrder('click'))
        mely.addWidget(me.click)

        #키보드
        #동시입력 지원해야 함
        me.key = QtWidgets.QPushButton('key')
        mely.addWidget(me.key)

        #슬립
        me.sleepWidget = QtWidgets.QWidget()
        mely.addWidget(me.sleepWidget)

        sleeplayout = QtWidgets.QHBoxLayout()
        mely.sleepWidget.setLayout(sleeplayout)

        sleeplayout.setContentsMargins(0,0,0,0)
        sleeplayout.setSpacing(0)

        me.sleepInput = QtWidgets.QLineEdit()
        me.sleepInput.setFixedWidth(40)
        sleeplayout.addWidget(me.sleepInput)

        me.sleep = QtWidgets.QPushButton('sleep')
        sleeplayout.addWidget(me.sleep)

        #편집
        me.edit = QtWidgets.QPushButton('edit')
        me.edit.setDisabled(True)
        bd.editbtns.append(me.edit)
        me.addWidget(me.edit)
        me.moveup = QtWidgets.QPushButton('moveup')
        bd.editbtns.append(me.moveup)
        me.addWidget(me.moveup)
        me.movedown = QtWidgets.QPushButton('movedown')
        bd.editbtns.append(me.movedown)
        me.addWidget(me.movedown)





#칠판
class Board(QtWidgets.QScrollArea):
    selected = None
    editbtns = []
    def __init__(self):
        super().__init__()

        #횡바 제거, 동적인 사이즈 변경 가능
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)


        #스크롤 영역에 위젯 등록
        wd = self.widget = QtWidgets.QWidget()
        self.setWidget(wd)

        #종방향 레이아웃
        ly = self.layout = QtWidgets.QVBoxLayout()

        ly.setAlignment(QtCore.Qt.AlignTop)
        wd.setLayout(ly)

        self.id = self.layout.count()
    
    #분필
    def addWidget(self, widget):
        self.orders
        self.layout.addWidget(widget)

    def addOrder(self, orderType):
        ruler = Ruler(orderType)
        r = ruler.exec_()
        if r:
            self.layout.addWidget(Order(self, orderType, ruler.returnValues))

    def select(self, order):
        for i in range(self.layout.count()):
            otherOrder = self.layout.itemAt(i).widget()
            otherOrder.setStyleSheet('background:#ddd; color:#000')
        order.setStyleSheet('background:#00f; color:#fff')
        self.selected = order
        for value in self.editbtns:
            value.setDisabled(False)

    def mouseReleaseEvent(self, event):
        for i in range(self.layout.count()):
            otherOrder = self.layout.itemAt(i).widget()
            otherOrder.setStyleSheet('background:#ddd; color:#000')
        self.selected = None
        for value in self.editbtns:
            value.setDisabled(True)

#줄자
class Ruler(QtWidgets.QDialog):
    def __init__(self, orderType):
        super().__init__()
        self.orderType = orderType
        #최대화
        screenW = self.screen().geometry().width()
        screenH = self.screen().geometry().height()
        self.setGeometry(0, 0, screenW, screenH)
        #투명화, 상태바 제거, 항상 위에, 마우스 추적
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        #상태창
        wd = self.statusbar = QtWidgets.QWidget(self)
        wd.setContentsMargins(10,0,10,0)
        wd.setStyleSheet('background:#333; color:#aaa')
        ly = self.statusbarlayout = QtWidgets.QHBoxLayout()
        ly.setContentsMargins(0,0,0,0)
        wd.setLayout(ly)
        #클릭계열 이벤트는 x와 y 좌표 표시
        if self.orderType == 'click':
            x = ps.position().x
            y = ps.position().y
            #widgets
            ly.addWidget(QtWidgets.QLabel('x:'))
            self.posX = QtWidgets.QLabel(str(x))
            self.posX.setFixedWidth(30)
            ly.addWidget(self.posX)
            ly.addWidget(QtWidgets.QLabel('y:'))
            self.posY = QtWidgets.QLabel(str(y))
            self.posY.setFixedHeight(30)
            ly.addWidget(self.posY)
            #move
            self.widgetMaxX = screenW - self.statusbar.geometry().width() - 20
            self.widgetMaxY = screenH - self.statusbar.geometry().height() - 40
            wd.move(min(x + 20, self.widgetMaxX), min(y + 10, self.widgetMaxY))

        


    def mouseMoveEvent(self, event):
        if self.orderType == 'click':
            x = event.x()
            y = event.y()
            self.posX.setText(str(x))
            self.posY.setText(str(y))
            self.statusbar.move(min(x + 20, self.widgetMaxX), min(y + 10, self.widgetMaxY))

    def mousePressEvent(self, event):
        if self.orderType == 'click':
            self.x = event.x()
            self.y = event.y()

    def mouseReleaseEvent(self, event):
        if self.orderType == 'click':
            if self.x == event.x() and self.y == event.y():
                self.returnValues = {'x': self.x, 'y': self.y}
                self.accept()

    #반투명 유지
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.2)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtCore.Qt.white)
        painter.drawRect(self.rect())

class Order(QtWidgets.QWidget):
    def __init__(self, board, orderType, status):
        super().__init__()
        self.board = board

        self.setStyleSheet('background:#ddd')

        ly = self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(ly)

        lb = self.label = QtWidgets.QLabel()
        text = orderType
        for key, value in status.items():
            text += ', ' + str(key) + ': ' + str(value)
        lb.setText(text)
        ly.addWidget(lb)


    def mouseReleaseEvent(self, event):
        self.board.select(self)



class Menu(QtWidgets.QWidget):
    setbtns = []
    modbtns = []
    def __init__(self):
        super().__init__()
        ly = self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(ly)

        click = QtWidgets.QPushButton('click')
        setbtn

    def addWidget(self, widget):
        self.layout.addWidget(widget)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())