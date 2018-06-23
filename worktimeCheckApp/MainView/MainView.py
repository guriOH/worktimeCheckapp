import sys

from PyQt5 import *
from PyQt5.QtWidgets import *


class gridlayout_example(QWidget):
    def __init__(self, parent=None):
        super(gridlayout_example, self).__init__(parent)

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
    myWindow = gridlayout_example()

    myWindow.show()

    app.exec_()
