import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QCheckBox, QLabel, QPushButton,QMainWindow, QStatusBar, QToolBar
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
        
        toolbar.addSeparator()
        
        button_action2 = QAction(QIcon("./Python/resources/icons/icons/bug.png"), "Your button2", self)
        button_action2.setStatusTip("This is your second button")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)
        
        toolbar.addSeparator()
        
        toolbar.addWidget(QLabel("Hello"))
        
        toolbar.addSeparator()
        
        toolbar.addWidget(QCheckBox())
        
        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self, s):
        print("Click", s)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

window = MainWindow()
window.show() # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()


# Your application won't reach here until you exit and the event 
# loop has stopped.
