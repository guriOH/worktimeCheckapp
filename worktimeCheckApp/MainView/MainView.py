import datetime
import sys
import psycopg2

from PyQt5.QtCore import QDate, QEvent, Qt, QTimer, QTime, pyqtSlot
from PyQt5.QtGui import QIcon, QCursor, QTextCharFormat, QMouseEvent
from PyQt5.QtWidgets import *
import datetime
import time

startWorkTime = None
remainTime_one_week = 144000.0
t = ['월', '화', '수', '목', '금', '토', '일']
con = None
scheduletableName = "schedule"

class timeSelectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()


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
        self.endWorkTime = self.EndTimeed.time()
        global startWorkTime
        startWorkTime = self.StartTimeed.time()
        global endWorkTime
        endWorkTime = self.EndTimeed.time()
        print(startWorkTime)
        print(endWorkTime)
        self.close()
        self.reject()

    def closeEvent(self, event):
        print
        "User has clicked the red x on the main window"
        event.accept()



class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        global db
        db = dbUtils()
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
        db.insertData(self.cal.selectDay, dlg.startWorkTime,dlg.endWorkTime)


    def getWorkTime(self):
        workTime = db.selectDay(self.cal.selectDay)
        workTime = self.convertTimeFormat(workTime, "%d:%02d:%02d")
        self.workTimeLabel.setText(workTime)


    def resultByDate(self):
        db.resetByDate(self.today)
        global startWorkTime
        startWorkTime = None
        print("reset Data is date = " + self.today)

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
        resultTime = self.convertTimeFormat(remainTime_one_week-time, "%d:%02d:%02d")


        self.remainTimeLabel.setText(resultTime)

    def convertTimeFormat(self, time, format):
        resultTime = "0"
        if(time != None):
            m, s = divmod(time, 60)
            h, m = divmod(m, 60)
            resultTime = format % (h, m, s)
        print(resultTime)
        return resultTime


class dbUtils():

    def __init__(self):
        self.getConn()
        self.createScheduleTable()

    def createScheduleTable(self):
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS "+scheduletableName+"(date DATE PRIMARY KEY, start_w TIME NOT NULL, end_w TIME NOT NULL, work_time DOUBLE PRECISION)")
        con.commit()
        print("create schedule table")

    def getConn(self):
        global con
        con = psycopg2.connect(host="localhost", dbname="hoon", user="postgres")

    def insertData(self, today, startWorkTime, endWorkTime):
        todayworktime = (datetime.datetime.now().strptime(endWorkTime.toString('hh:mm:ss'), '%H:%M:%S')-
              datetime.datetime.now().strptime(startWorkTime.toString('hh:mm:ss'),'%H:%M:%S')).total_seconds()
        print(todayworktime)
        cur = con.cursor()
        sql ="INSERT INTO " + scheduletableName + "(date,start_w,end_w,work_time) VALUES('"\
             +today+"','"+startWorkTime.toString('hh:mm:ss')+"', '"\
             +endWorkTime.toString('hh:mm:ss')+"', '"\
             +str(todayworktime)+"')"
        try:
            cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
        con.commit()

    def updateData(self, today, endtime):
        cur = con.cursor()
        sql = "UPDATE " + scheduletableName + " SET end_w = '"+endtime+ "' WHERE date = '"+today+"'"
        try:
           cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
        con.commit()

    def resetByDate(self, day):
        cur = con.cursor()
        sql = "DELETE FROM " + scheduletableName + " WHERE date = '"+day+"'"
        try:
            cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
        con.commit()

    def selectDay(self, day):
        cur = con.cursor()
        sql = "SELECT work_time FROM " + scheduletableName + " WHERE date = '" + day + "'"

        print(sql)
        try:
            cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
        con.commit()
        rows = cur.fetchall()
        print("\nRows: \n")
        for row in rows:
            return row[0]

    def calcRemainTime(self,startDay):
        cur = con.cursor()
        sql = "select sum(work_time) FROM " + scheduletableName + " WHERE date >= '"+startDay+"'"
        print(sql)
        try:
            cur.execute(sql)

        except psycopg2.Error as e:
            print(e)
        con.commit()

        rows = cur.fetchall()
        print("\nRows: \n")
        for row in rows:
            return row[0]


    def closeConn(self):
        con.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainView()

    myWindow.show()

    app.exec_()
