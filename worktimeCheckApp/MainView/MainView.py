

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtWidgets import *
from worktimeCheckApp.Config.Config import *
from worktimeCheckApp.DataBase.dbUtils import *
from worktimeCheckApp.MainView.Dialog.timeSelectDlg import *
import datetime




remainTime_one_week = 144000.0
lunchTime = 3600.0
t = ['월', '화', '수', '목', '금', '토', '일']

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        global db
        props = PropertiesReader()
        db = dbUtils(props)

        self.mainUI = createMainUi()
        self.setCentralWidget(self.mainUI)
        self.setWindowTitle("Henry's WorkTime")


        self.resize(400, 300)
        # self.statusBar().showMessage(self.mainUI.resultTime)


class calendar(QCalendarWidget):
    def __init__(self):
        super().__init__()
        self.selectDay = str(datetime.datetime.now().date())
        print(self.selectDay)
        self.cal = QCalendarWidget()
        self.cal.setVerticalHeaderFormat(0)  # vertical header 숨기기
        self.cal.installEventFilter(self)
        self.cal.clicked[QDate].connect(self.selectDate)


    def selectDate(self,date):
        self.selectDay = str(date.toPyDate())
        print(self.selectDay)


class createMainUi(QWidget):

    def __init__(self):
        super().__init__()
        self.resultTime = self.convertTimeFormat(remainTime_one_week, "%d:%02d:%02d")
        menubar = QMenuBar()
        menubar.setNativeMenuBar(False)
        self.selectDay = None
        self.cal = calendar()


        fm = QTextCharFormat()
        fm.setForeground(Qt.red)
        fm.setBackground(Qt.yellow)

        self.today = str(datetime.datetime.now().date())
        self.cal.setDateTextFormat(QDate.fromString(self.today, "yyyy-MM-dd"), fm)

        sublayout1 = QVBoxLayout()
        sublayout1.addWidget(self.cal.cal)

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

        button1 = QPushButton("Show work time")
        button1.clicked.connect(self.getWorkTime)
        button2 = QPushButton("Remained work time (at week)")
        button2.clicked.connect(self.calcremainTime)
        button3 = QPushButton("resetByDate")
        button3.clicked.connect(self.resultByDate)
        button4 = QPushButton("Insert Work Time")
        button4.clicked.connect(self.showDayInfo)
        grid_layout = QGridLayout(self)
        grid_layout.addLayout(sublayout1, 0, 0, 1, 4)
        grid_layout.addLayout(sublayout2, 1, 0, 1, 4)
        grid_layout.addLayout(sublayout3, 2, 0, 1, 4)
        grid_layout.addWidget(button1, 4, 0, 1, 1)
        grid_layout.addWidget(button2, 4, 1, 1, 1)
        grid_layout.addWidget(button3, 4, 2, 1, 1)
        grid_layout.addWidget(button4, 4, 3, 1, 1)


    def showDayInfo(self):
        dlg = timeSelectDialog()
        dlg.exec_()
        dlg.close()
        db.insertData(self.cal.selectDay, dlg.startWorkTime,dlg.endWorkTime,lunchTime)



    def getWorkTime(self):
        workTime = db.selectDay(self.cal.selectDay)
        workTime = self.convertTimeFormat(workTime, "%d:%02d:%02d")
        self.workTimeLabel.setText(workTime)


    def resultByDate(self):
        db.resetByDate(self.cal.selectDay)
        global startWorkTime
        startWorkTime = None
        print("reset Data is date = " + self.cal.selectDay)

    def calcremainTime(self):
        print(str(datetime.datetime.now().date()).split('-')[2])
        r = datetime.datetime.today().weekday()
        today = str(datetime.datetime.now().date()).split('-')
        theDay = int(today[2])-r
        print(theDay)
        startDay = str(today[0]+"-"+today[1]+"-"+str(int(today[2])-r))
        reformat = QDate.fromString(startDay, "yyyy-MM-dd")
        print(reformat.toString("yyyy-MM-dd"))

        time = db.calcRemainTime(reformat.toString("yyyy-MM-dd"))
        self.resultTime = self.convertTimeFormat(remainTime_one_week-time, "%d:%02d:%02d")
        self.remainTimeLabel.setText(self.resultTime)

    def convertTimeFormat(self, time, format):
        resultTime = "0"
        if(time != None):
            m, s = divmod(time, 60)
            h, m = divmod(m, 60)
            resultTime = format % (h, m, s)
        print(resultTime)
        return resultTime


