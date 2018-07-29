from PyQt5.QtCore import QTime, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QTimeEdit, QLabel, QLineEdit, QPushButton, QGridLayout

startWorkTime = None

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

