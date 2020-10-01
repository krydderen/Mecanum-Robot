import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QPalette
from PyQt5.QtWidgets import QAction, QApplication, QBoxLayout, QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton,QMainWindow, QStatusBar, QToolBar, QVBoxLayout, QWidget
from PyQt5 import QtWidgets

class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("My Vilde App")
        
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        
        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(0)
        
        layout1.addWidget(Color('green'))
        
        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('yellow'))
        layout2.addWidget(Color('purple'))
        
        layout1.addLayout(layout2)
        
        layout3.addWidget(Color('red'))
        layout3.addWidget(Color('blue'))
        
        layout1.addLayout(layout3)
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
        
        
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
