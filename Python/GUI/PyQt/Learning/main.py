import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QPushButton,QMainWindow, QStatusBar, QToolBar
from PyQt5 import QtWidgets


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("My vilde App")
        
        label = QLabel("THIS IS Vilde!!!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)
        
        toolbar = QToolBar("My Vilde Toolbar")
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("./Python/resources/icons/icons/bug.png"),"Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        
        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self, s):
        print("Click", s)

    


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
