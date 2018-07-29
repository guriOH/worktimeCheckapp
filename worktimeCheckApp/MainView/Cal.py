import sys

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QLineEdit, QToolButton, QStyle, QApplication, QHBoxLayout, QMainWindow, QWidget, \
    QCalendarWidget


class CalWidget(QLineEdit):
    def __init__(self, parent=None):
        super(CalWidget, self).__init__(parent)
        self.calButton = QToolButton(self)
        self.calButton.setIcon(QIcon('/usr/dropBox/calIcon.png'))
        self.calButton.setStyleSheet('border: 0px; padding: 0px;')
        self.calButton.setCursor(Qt.ArrowCursor)
        self.calButton.clicked.connect(self.showCalWid)

    def resizeEvent(self, event):
        buttonSize = self.calButton.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.calButton.move(self.rect().right() - frameWidth - buttonSize.width(),
                         (self.rect().bottom() - buttonSize.height() + 1)/2)
        super(CalWidget, self).resizeEvent(event)

    def showCalWid(self):
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.updateDate)
        self.calendar.setWindowFlags(Qt.FramelessWindowHint)
        self.calendar.setStyleSheet('background: white; color: black')
        self.calendar.setGridVisible(True)
        pos = QCursor.pos()
        self.calendar.setGeometry(pos.x(), pos.y(),300, 200)
        self.calendar.show()

    def updateDate(self,*args):
        getDate = self.calendar.selectedDate().toString()
        self.setText(getDate)
        self.calendar.deleteLater()

class MainDialog(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        centralwidget = QWidget(self)
        self.layout = QHBoxLayout(centralwidget)
        self.calButton = CalWidget()
        self.layout.addWidget(self.calButton)
        self.setCentralWidget(centralwidget)


def main():
     app = QApplication(sys.argv)
     form = MainDialog()
     form.show()
     app.exec_()

if __name__ == '__main__':
     main()