from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys 
import os
from random import randint
from pyfirmata import Arduino, util
import matplotlib.pyplot as plt
import sys
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Use standardfirmata on arduino to run this

board = Arduino('COM3')

it = util.Iterator(board)

it.start()
         
times = []
clicks = []
    
analog_input = board.get_pin('a:0:i')

class MainWindowg(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindowg, self).__init__(*args, **kwargs)
        l = QtWidgets.QVBoxLayout()
        button1 = QtWidgets.QPushButton("Stop data")
        button1.clicked.connect(self.stop_timer)
        l.addWidget(button1)
        self.graphWidget = pg.PlotWidget()
        l.addWidget(self.graphWidget)

        w = QtWidgets.QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)
        self.x = list(range(100))  
        self.y = [0 for _ in range(100)] 

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(0.0001) # msec
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        print(analog_input.read())
        self.x = self.x[1:]  
        self.x.append(self.x[-1] + 1)  

        self.y = self.y[1:]  
        self.y.append(analog_input.read()) 

        self.data_line.setData(self.x, self.y)  
        if self.y[-1] > 0.3 and self.y[-3] < 0.3 and self.y[-2] < 0.3:
            times.append(self.x[-1])
            #clicks.append(self.y[-1])
            clicks.append(1)
            
    def stop_timer(self):
        
            self.timer.stop()
            
   
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        l = QtWidgets.QVBoxLayout()
        button1 = QtWidgets.QPushButton("Push to take data and show plot window")
        button1.clicked.connect(self.show_new_window)
        l.addWidget(button1)

        w = QtWidgets.QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def show_new_window(self):
        self.wg = MainWindowg()
        self.wg.show()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()

board.pass_time(1)
board.exit()

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Clicks')
        super(MplCanvas, self).__init__(fig)


class MainWindowm(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindowm, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(times, clicks, 'o')
        self.setCentralWidget(sc)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindowm()
app.exec_()
#plt.plot(times, clicks, 'o')
#plt.xlabel('Time')
#plt.ylabel('Clicks')
#plt.show()
print('Timestamps: ', times)
