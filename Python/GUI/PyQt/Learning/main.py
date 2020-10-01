import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget,QMainWindow

class CustomButton(QPushButton):
    
    def keyPressEvent(self, event):
        super(CustomButton, self).keyPressEvent(event)
    

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Heia Vilde")
        
        label = QLabel("Hei igjen Vilde")
        
        label.setAlignment(Qt.AlignCenter)
        
        self.setCentralWidget(label)
    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
