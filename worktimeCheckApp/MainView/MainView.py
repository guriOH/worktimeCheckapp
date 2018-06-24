import datetime
import sys
from time import strftime

from PyQt5 import *
from PyQt5.QtCore import QDate, QEvent, Qt, QTimer, QTime, pyqtSlot
from PyQt5.QtGui import QIcon, QCursor, QTextCharFormat
from PyQt5.QtWidgets import *

startWorkTime = None
remainTime_one_week = "40:00:00"

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

        if startWorkTime is None:
            self.StartTimeed.setTime(QTime.currentTime())
        else:
            self.StartTimeed.setTime(startWorkTime)
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
        self.startWorkTime = self.StartTimeed.time()
        self.EndWorkTime = self.EndTimeed.time()
        global startWorkTime
        startWorkTime = self.startWorkTime
        print(startWorkTime)
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

        self.workTime = ""
        self.cal = QCalendarWidget()
        self.cal.setVerticalHeaderFormat(0)  # vertical header 숨기기
        self.cal.installEventFilter(self)

        self.cal.clicked[QDate].connect(self.showDayInfo)

        fm = QTextCharFormat()
        fm.setForeground(Qt.red)
        fm.setBackground(Qt.yellow)

        self.today = str(datetime.datetime.now().date())
        print(self.today)
        self.cal.setDateTextFormat(QDate.fromString(self.today, "yyyy-MM-dd"), fm)



        sublayout1 = QVBoxLayout()
        sublayout1.addWidget(self.cal)

        label2 = QLabel('Worked Time!!')
        self.workTimeLabel = QLabel('Time')
        sublayout2 = QHBoxLayout()
        sublayout2.addWidget(label2)
        sublayout2.addWidget(self.workTimeLabel)

        label3 = QLabel('Remain Time!!')
        self.remainTimeLabel = QLabel('Time')
        sublayout3 = QHBoxLayout()
        sublayout3.addWidget(label3)
        sublayout3.addWidget(self.remainTimeLabel)

        button1 = QPushButton("Get off work")
        button1.clicked.connect(self.getOffwork)
        button2 = QPushButton("Remained work time (at week)")
        button3 = QPushButton("------")
        grid_layout = QGridLayout(self)
        grid_layout.addLayout(sublayout1, 0, 0, 1, 3)
        grid_layout.addLayout(sublayout2, 1, 0, 1, 3)
        grid_layout.addLayout(sublayout3, 2, 0, 1, 3)
        grid_layout.addWidget(button1, 3, 0, 1, 1)
        grid_layout.addWidget(button2, 3, 1, 1, 1)
        grid_layout.addWidget(button3, 3, 2, 1, 1)

    @pyqtSlot(QDate)
    def showDayInfo(self,date):
        print(str(date.toPyDate()))
        if str(date.toPyDate()).__ne__(self.today):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Not toDay")
            msg.exec_()
        else:
            dlg = timeSelectDialog()
            dlg.exec_()
            self.timer_start(dlg.startWorkTime)

    def timer_start(self, startTime):
        self.timer = QTimer()
        self.time = QTime(0, 0, 0)
        self.timer.timeout.connect(lambda *_str: self.timerEvent(startTime))
        self.timer.start(1000)

    def timerEvent(self, startTime):
        global time
        self.time = self.time.addSecs(1)
        self.update_gui()

    def update_gui(self):
        # print(self.hour + ":" + self.minute + ":" + self.second)
        self.workTime =self.time.toString("hh:mm:ss")
        self.workTimeLabel.setText(self.time.toString("hh:mm:ss"))

    def getOffwork(self):
        print("Go Home!! Current Time - " + QTime.currentTime().toString('hh:mm:ss'))
        print("Your worked time for the day is " + self.workTime)
        self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainView()

    myWindow.show()

    app.exec_()
