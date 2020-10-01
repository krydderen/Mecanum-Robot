import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QPalette
from PyQt5.QtWidgets import QAction, QApplication, QBoxLayout, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton,QMainWindow, QStackedLayout, QStatusBar, QTabWidget, QToolBar, QVBoxLayout, QWidget
from PyQt5 import QtWidgets

class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("HELLO!")
        
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("My Awesome App")
        
        label = QLabel("THIS IS AWESOME!!!")
        label.setAlignment(Qt.AlignCenter)
        
        self.setCentralWidget(label)
        
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(30,30))
        self.addToolBar(toolbar)
        
        button_action = QAction(QIcon("./Python/resources/icons/icons/bug.png"), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        
        toolbar.addSeparator()
        
        button_action2 = QAction(QIcon("./Python/resources/icons/icons/bug.png"), "Your button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)
        
        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())
        
        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self, s):
        print("click", s)
        
        
        dlg = CustomDialog(self)
        if dlg.exec_():
            print("Success!")
        else:
            print("Cancel!")
        
        
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
