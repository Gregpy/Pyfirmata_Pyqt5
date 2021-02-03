from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,  QLineEdit
from PyQt5.QtCore import QTimer
import sys
from pyfirmata import Arduino, util

# Use standardfirmata on arduino to run this

board = Arduino('COM3')

it = util.Iterator(board)

it.start()
         
times = []
clicks = []

analog_input = board.get_pin('a:0:i')

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.line = QLineEdit(self)
        layout.addWidget(self.line)
        self.setLayout(layout)
        timer = QTimer(self)
        timer.setInterval(100) # change this if want to see shorter pulses
        timer.timeout.connect(self.update_line)
        timer.start()

    def update_line(self):
        val = str(analog_input.read())
        self.line.setText(val)


class AnotherWindow2(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Another Window2")
        layout.addWidget(self.label)
        self.line = QLineEdit(self)
        layout.addWidget(self.line)
        self.setLayout(layout)
        timer = QTimer(self)
        timer.setInterval(100) # change this if want to see shorter pulses
        timer.timeout.connect(self.update_line)
        timer.start()

    def update_line(self):
        val = str(analog_input.read())
        self.line.setText(val)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        l = QVBoxLayout()
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(self.show_new_window)
        l.addWidget(button1)

        button2 = QPushButton("Push for Window 2")
        button2.clicked.connect(self.show_new_window2)
        l.addWidget(button2)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def show_new_window(self):
        self.w = AnotherWindow()
        self.w.show()

    def show_new_window2(self):
        self.w2 = AnotherWindow2()
        self.w2.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
board.pass_time(1)
board.exit()