#!/usr/bin/env python
import serial
import time
import plotly.plotly as py
import plotly.tools as tls   
import numpy as np
from plotly.graph_objs import *
 
arduinoFile = '/dev/ttyACM0'
logFile = 'log.csv'
sensorOutput = [0.0, 0.0]
 
py.sign_in('blessmurk','ufcmiq1n96')
stream_ids= tls.get_credentials_file()['stream_ids']

#print stream_ids[0]
#print stream_ids[1]
my_data = Data([
    Scatter(x=[], y=[],
         name='Sensor 1 temperature',
         mode='lines',
         line= Line(color='rgba(250,30,30,0.9)',width=2.5),
         stream=dict(token=stream_ids[0],maxpoints=900)),
     ])
    
my_layout = Layout(
    title='Temperature and RH in DHST',
    xaxis=XAxis(
         showline=True,
         linecolor='#bdbdbd',
         title='Time',
         showticklabels=True),
    yaxis=YAxis(
         showline=True,
         linecolor='#bdbdbd',
         title='Temperature [*C]',
         showticklabels=True,
         titlefont=Font(size=18,color='#ee3333')),
         legend=Legend(x=0,y=1), showlegend=True
    )
         
   
my_fig = Figure(data=my_data, layout=my_layout)
py.plot(my_fig, filename='Temperature_in_DHST')
time.sleep(3)
 
s1temp = py.Stream(stream_ids[0])
#s1hum = py.Stream(stream_ids[1])
ser = serial.Serial(arduinoFile, baudrate=9600, bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=10)
time.sleep(1)
#ser.flushInput()
 
def gettemp():
    print("connected to: " + ser.portstr)
    ser.write('t')
    time.sleep(5)
    #ser.flush()
    line=ser.readline().strip('\r').strip('\n')
    print line
    return line
timeStart = time.time()
while True:
    timeDelay = time.time()-timeStart
    timeStamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    sensorOutputString = gettemp()
    print sensorOutputString

    """
    sensorOutputRaw = sensorOutputString.split(',')
    sensorOutput[0] = float(sensorOutputRaw[0]) + 0.4  # calibration
    sensorOutput[1] = float(sensorOutputRaw[1]) + 0.2
    """    
    resultString = str(timeDelay)+','+timeStamp+','+str(sensorOutputString) #+','+str(sensorOutput[1])
    print(resultString)
    my_file = open(logFile,'a')
    my_file.write(resultString+'\n')
    my_file.close()
    s1temp.open()
    #s1hum.open()
    s1temp.write(dict(x=timeStamp,y=sensorOutputString))
    #s1hum.write(dict(x=timeStamp,y=sensorOutput[1]))
    s1temp.close()
    #s1hum.close()
    time.sleep(.08)
 
ser.close()
