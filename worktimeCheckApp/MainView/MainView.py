import datetime
import sys

from PyQt5 import *
from PyQt5.QtCore import QDate, QEvent, Qt, QTimer, QTime
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import *


class timeSelectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.id = None
        self.password = None

    def setupUI(self):
        self.setGeometry(400, 400, 300, 100)
        self.setWindowTitle("Sign In")
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.StartTimeed = QTimeEdit(self)
        self.StartTimeed.setDisplayFormat("hh:mm:ss")  # 24 시간으로 표시 self.timeed.setTime(QTime(15,30))
        self.EndTimeed = QTimeEdit(self)
        self.EndTimeed.setDisplayFormat("hh:mm:ss")  # 24 시간으로 표시 self.timeed.setTime(QTime(15,30))
        # 현재 시간으로 Default 설정 추가 필요

        label1 = QLabel("Start Work: ")
        label2 = QLabel("End Work: ")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.pushButton1 = QPushButton("Ok")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.StartTimeed, 0, 1)
        layout.addWidget(self.pushButton1, 0, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.EndTimeed, 1, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        self.startTime= self.StartTimeed.time()
        self.endTime = self.EndTimeed.time()
        self.hide()

    def closeEvent(self, event):
        print
        "User has clicked the red x on the main window"
        event.accept()




class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainUI = createMainUi()
        self.setCentralWidget(self.mainUI)
        self.setWindowTitle("Henry's WorkTime")

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu('File')
        edit_menu = menu_bar.addMenu('Edit')
        new_action = QAction('New', self)
        file_menu.addAction(new_action)
        new_action.setStatusTip("New File")

        self.resize(400, 300)
        self.statusBar().showMessage("Text in status bar")



class createMainUi(QWidget):

    def __init__(self):
        super().__init__()
        menubar = QMenuBar()
        menubar.setNativeMenuBar(False)
        cal = QCalendarWidget()
        cal.setVerticalHeaderFormat(0)  # vertical header 숨기기
        cal.installEventFilter(self)

        cal.clicked[QDate].connect(self.showDayInfo)

        sublayout1 = QVBoxLayout()
        sublayout1.addWidget(cal)

        label2 = QLabel('remain Time!!')
        self.remainTimeLabel = QLabel('Time')
        sublayout2 = QVBoxLayout()
        sublayout2.addWidget(label2)
        sublayout2.addWidget(self.remainTimeLabel)
        button1 = QPushButton("button1")
        button2 = QPushButton("button2")
        button3 = QPushButton("button3")
        grid_layout = QGridLayout(self)
        grid_layout.addLayout(sublayout1, 0, 0, 1, 3)
        grid_layout.addLayout(sublayout2, 1, 0, 1, 3)
        grid_layout.addWidget(button1, 2, 0, 1, 1)
        grid_layout.addWidget(button2, 2, 1, 1, 1)
        grid_layout.addWidget(button3, 2, 2, 1, 1)

    def showDayInfo(self):
        dlg = timeSelectDialog()
        dlg.exec_()
        self.timer_start(dlg.startTime)


    def timer_start(self,startTime):
        self.timer = QTimer()
        self.timer.timeout.connect(lambda *_str: self.timerEvent(startTime))
        self.timer.start(1000)


    def timerEvent(self,startTime):
        stTime = startTime.toString('hh:mm:ss').split(':')
        now = QTime.currentTime().toString('hh:mm:ss').split(':')
        self.hour = str(int(now[0])-int(stTime[0]))
        self.minute = str(int(now[1])-int(stTime[1]))
        self.second = str(int(now[2])-int(stTime[2]))

        self.update_gui()

    def update_gui(self):
        # print(self.hour + ":" + self.minute + ":" + self.second)
        self.remainTimeLabel.setText(self.hour + ":" + self.minute + ":" + self.second)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainView()

    myWindow.show()

    app.exec_()
