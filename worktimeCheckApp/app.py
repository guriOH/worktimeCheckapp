import sys

from PyQt5.QtWidgets import QApplication
from worktimeCheckApp.MainView.MainView import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainView()
    myWindow.show()
    app.exec_()
