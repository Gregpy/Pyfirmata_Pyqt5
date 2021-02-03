from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys 
import os
from random import randint
from pyfirmata import Arduino, util
import matplotlib.pyplot as plt

# Use standardfirmata on arduino to run this

board = Arduino('COM3')

it = util.Iterator(board)

it.start()
         
times = []
clicks = []
    
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = list(range(100))  
        self.y = [0 for _ in range(100)] 

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        self.analog_input = board.get_pin('a:0:i')
        self.timer = QtCore.QTimer()
        self.timer.setInterval(0.0001) # msec
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        print(self.analog_input.read())
        self.x = self.x[1:]  
        self.x.append(self.x[-1] + 1)  

        self.y = self.y[1:]  
        self.y.append(self.analog_input.read()) 

        self.data_line.setData(self.x, self.y)  
        if self.y[-1] > 0.5 and self.y[-3] < 0.5 and self.y[-2] < 0.5:
            times.append(self.x[-1])
            #clicks.append(self.y[-1])
            clicks.append(1)

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()

board.pass_time(1)
board.exit()

plt.plot(times, clicks, 'o')
plt.xlabel('Time')
plt.ylabel('Clicks')
plt.show()
print('Timestamps: ', times)