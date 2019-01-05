import serial  # import Serial Library
import re
import glob
from functions import *
import initExample
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import rtdclass as rt

# variables
c_t = 1
t = 0
show = 0
c = 0
x = 4
y = 6
r_data = []
for i in range(x):
    r_data.append([])
s_data = []
for i in range(y):
    s_data.append([])
time = []

# get the port
arduinoData = serial.Serial(ask_for_port(), 115200)  # Creating our serial object named arduinoData

# open a graph page
win = pg.GraphicsWindow(title="T-P-H Monitoring System", size=(1900, 1000))
win.setWindowTitle('Monitoring System')
lasttime = pg.ptime.time()

# lets define our RTDs
# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    In these examples, the array size is fixed.
# =====Creating our Graps====

# RTD plotting
RTD = []
s = []
time_r = []
time_s = []
columns = 0

r = []
s1 = []

Colors = ['r', 'g', 'b', 'w', 'g', 'y']
symbol = ['star', 't', 't1', 'p', 'h', 't3']
symb = [(195, 46, 212), (0, 128, 0), (126, 47, 142), (119, 172, 48), (0, 114, 189), (237, 177, 32)]
for i in range(4):
    RTD.append(rt.sensor("RTD_" + str(i + 1)))
    #print(RTD[i].name)
    if (i == 0):
        RTD[i].plot = win.addPlot(title="RTDs")
        RTD[i].plot.addLegend()
        RTD[i].plot.setLabel('left', 'Voltage', 'v')


    RTD[i].time = np.array([0, 0])
    RTD[i].data = np.array([0, 0])
    RTD[i].pen = Colors[i]
    RTD[i].symbols = symbol[i]
    RTD[i].symb = symb[i]

    RTD[i].graph(RTD[0])

win.nextRow()
count = 0
tagg = ['Temperature','Pressure','Humidity', '%', 'Torr','C']
for i in range(3):
    for k in range(2):
        s.append(rt.sensor(name(i) + str(k + 1)))
        if (count % 2 == 0):
            s[i].plot = win.addPlot(title=name(i))
            s[i].plot.addLegend()
            s[i].plot.setLabel('left', tagg[i], tagg[5 - i])



        s[count].time = np.array([0, 0])
        s[count].data = np.array([0, 0])
        s[count].pen = Colors[count]
        s[count].symbols = symbol[count]
        s[count].symb = symb[5 - i]

        s[count].graph(s[i])
        #print(s[count].name)
        count = count + 1

# titles on file
RTD[0].fName = "rtd_data.csv"
RTD[0].start()

for i in range(x):
    RTD[0].write(RTD[i].name, (4 - i))

s[0].fName = "Bm280.csv"
s[0].start()
for i in range(y):
    s[0].write(s[i].name, 6 - i)


def showtime():  # While loop that loops forever
    global show, t, lasttime, r_data, s_data, r, s, RTD, s1, time_r, time_s, once
    x = 4
    y = 6
    while (arduinoData.inWaiting() == 0):  # Wait here until there is data
        if (show == 0):
            print("\n\033[1;31;40m Waiting to Receive Data from Arduino....\033[0m \n")
            print("\033[1;31;47m Press CTRL+C to CANCEL waiting\033[0m  \n")
            show = 1

        pass

    arduinoString = arduinoData.readline()  # read the line of text from the serial port
    # rtd1.write(arduinoString)s
    print (arduinoString)
    dataArray = arduinoString.decode('utf8').split(' ')  # Split it into an array called dataArray
    #print (dataArray)
    now = pg.ptime.time()
    t = (now - lasttime)
    if len(dataArray) == 5 and dataArray[0] == "rtd":
        RTD[0].write(arduinoString.replace("rtd","").strip() + " " + str(t), -1)
        try:
            for i in range(x):
                r.append((float(dataArray[i + 1])))

        except ValueError:
            showtime()
        time_r.append(t)
        for i in range(x):
            r_data[i].append(r[i])

        if (len(time_r) <= 40):
            # Asigning data
            for i in range(x):
                RTD[i].data = np.array(r_data[i])
                RTD[i].time = np.array(time_r)
        else:
            for i in range(x):
                RTD[i].update(r[i], t)
        r = []




    elif len(dataArray) == 7 and dataArray[0] == "bme":
        s[0].write(arduinoString.replace("bme","").strip() + " " + str(t), -1)
        try:

            for i in range(y):
                s1.append(float(dataArray[i + 1]))

        except ValueError:
            showtime()
        time_s.append(t)
        for i in range(y):
            s_data[i].append(s1[i])

        if (len(time_s) <= 40):
            # Asigning data
            for i in range(y):
                s[i].data = np.array(s_data[i])
                s[i].time = np.array(time_s)
        else:
            for i in range(y):
                s[i].update(s1[i], t)
        s1 = []


# timer
timer = pg.QtCore.QTimer()
timer.timeout.connect(showtime)
timer.start(c_t)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

