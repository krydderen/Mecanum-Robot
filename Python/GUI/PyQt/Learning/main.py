import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)


window = QWidget()
window.setWindowTitle("Fy faen kom i røva mit")
window.show()


app.exec_()
