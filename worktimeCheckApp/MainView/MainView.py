import sys

from PyQt5 import *
from PyQt5.QtWidgets import *


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

        sublayout1 = QVBoxLayout()
        sublayout1.addWidget(cal)

        label2 = QLabel('remain Time!!')
        line_edit2 = QLineEdit()
        sublayout2 = QVBoxLayout()
        sublayout2.addWidget(label2)
        sublayout2.addWidget(line_edit2)

        button1 = QPushButton("button1")
        button2 = QPushButton("button2")
        button3 = QPushButton("button3")

        grid_layout = QGridLayout(self)
        grid_layout.addLayout(sublayout1, 0, 0, 1, 3)
        grid_layout.addLayout(sublayout2, 1, 0, 1, 3)
        grid_layout.addWidget(button1, 2, 0, 1, 1)
        grid_layout.addWidget(button2, 2, 1, 1, 1)
        grid_layout.addWidget(button3, 2, 2, 1, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainView()

    myWindow.show()

    app.exec_()
