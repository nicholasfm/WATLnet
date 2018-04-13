from sense_hat import SenseHat
from datetime import datetime
from time import sleep
import spidev
import time
import os
import RPi.GPIO as GPIO, time, os
from shutil import copy
import sys
from cmath import rect, phase
from math import radians, degrees
#settings#

###file frequencies####
freq1=12
add1=12
freq2=120
add2=120
freq3=720
add3=720

#WIND DIRECTION
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

#converting the voltage to 360 degrees direction 
def ConvertDir(data,places):
  degrees = (data * 360) / float(1023)
  degrees = round(degrees,places)
  return degrees

def WindDirection():
  while True :
    volts=ReadChannel(7)
    direction=ConvertDir(volts,2)
    return direction
#mean angles as cos and sin vectors
def mean_angle(deg):
    return degrees(phase(sum(rect(1, radians(d)) for d in deg)/len(deg)))

#WIND SPEED
rfactor = 2.25*1.609
samples = 5
speed = 0
speedPin = 17
state = False

#setup GPIO's
GPIO.setmode(GPIO.BCM)
GPIO.setup(speedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Speed measurment
def getSpeed():
#    Loop 5 seconds (samples) and record pulses
	counter = 0
	endTime = (int(time.time()) + samples)
	state = False
	while (int(time.time()) < endTime):
		if ( GPIO.input(speedPin) == True ):
			state = True
		if ((state == True) and (GPIO.input(speedPin) == False)):
			state = False
			counter = counter + 1
#	counter is the number of pulses during the sample time
#	speed is in km/h	
	speed = ((counter / samples)  * rfactor)
	return speed


#get the data from the sensors
def log_data():
  output_string = ",".join(str(value) for value in sense_data)
  batch_data.append(output_string)

def log_data_2():
  output_string = ",".join(str(value) for value in sense_data_2)
  batch_data_2.append(output_string)

def log_data_3():
  output_string = ",".join(str(value) for value in sense_data_3)
  batch_data_3.append(output_string)

def log_data_4():
    output_string = ",".join(str(value) for value in five_sec_data)
    batch_data_4.append(output_string)

def file_setup(filename):
  header  =["Time", " Avg Temperature", " Min Temperature", " Max Temperature", " Avg Humidity", " Min Humidity", " Max Humidity", " Avg Pressure", " Min Pressure", " Max Pressure", " Avg Wind Dir", " Min Wind Dir", " Max Wind Dir", " Avg Wind Speed", " Min Wind Speed", " Max Wind Speed", "angle"]
  with open(filename,"w") as f:
      f.write(",".join(str(value) for value in header)+ "\n")

def avg(list):
    sum = 0
    for elm in list:
        sum += elm
    return (str(sum/(len(list))))
  
def compass():
  sense = SenseHat()
  sense.set_rotation(0)
  sense.clear()
  compass = sense.get_compass()
  return compass

def get_sense_data():
  global freq1
  global freq2
  global freq3
  global add1
  global add2
  global add3
  sense_data=[]
  sense_data_2=[]
  sense_data_3=[]
  five_sec_data=[]
  
  while True :
      sense_temp.append(sense.get_temperature_from_pressure())
      sense_hum.append(sense.get_humidity())
      sense_press.append(sense.get_pressure())
      wind_dir.append(WindDirection())
      wind_speed.append(getSpeed())
      sense_hum1=sense_hum[-12:]
      sense_hum2=sense_hum[-120:]
      sense_hum3=sense_hum[-720:]
      sense_press1=sense_press[-12:]
      sense_press2=sense_press[-120:]
      sense_press3=sense_press[-720:]
      sense_temp1=sense_temp[-12:]
      sense_temp2=sense_temp[-120:]
      sense_temp3=sense_temp[-720:]
      wind_dir1=wind_dir[-12:]
      wind_dir2=wind_dir[-120:]
      wind_dir3=wind_dir[-720:]
      wind_speed1=wind_speed[-12:]
      wind_speed2=wind_speed[-120:]
      wind_speed3=wind_speed[-720:]
      five_sec_data.extend((datetime.now(),sense_hum[-1:],sense_press[-1:],sense_temp[-1:],wind_dir[-1:],wind_speed[-1:]))

      if len(sense_temp)>= freq1:
        avg_temp=avg(sense_temp1)
        min_temp=min(sense_temp1)
        max_temp=max(sense_temp1)
        avg_hum=avg(sense_hum1)
        min_hum=min(sense_hum1)
        max_hum=max(sense_hum1)
        avg_press=avg(sense_press1)
        min_press=min(sense_press1)
        max_press=max(sense_press1)
        avg_dir=mean_angle(wind_dir1)
        min_dir=min(wind_dir1)
        max_dir=max(wind_dir1)
        avg_speed=avg(wind_speed1)
        min_speed=min(wind_speed1)
        max_speed=max(wind_speed1)        
        sense_data.extend((datetime.now(),avg_temp,min_temp,max_temp,avg_hum,min_hum,max_hum,avg_press,min_press,max_press,avg_dir,min_dir,max_dir,avg_speed,min_speed,max_speed, compass()))
        freq1+=add1
        

        if len(sense_temp)>= freq2:        
          avg_temp2=avg(sense_temp2)
          min_temp2=min(sense_temp2)
          max_temp2=max(sense_temp2)
          avg_hum2=avg(sense_hum2)
          min_hum2=min(sense_hum2)
          max_hum2=max(sense_hum2)
          avg_press2=avg(sense_press2)
          min_press2=min(sense_press2)
          max_press2=max(sense_press2)
          avg_dir2=mean_angle(wind_dir2)
          min_dir2=min(wind_dir2)
          max_dir2=max(wind_dir2)
          avg_speed2=avg(wind_speed2)
          min_speed2=min(wind_speed2)
          max_speed2=max(wind_speed2)          
          sense_data_2.extend((datetime.now(),avg_temp2,min_temp2,max_temp2,avg_hum2,min_hum2,max_hum2,avg_press2,min_press2,max_press2,avg_dir2,min_dir2,max_dir2,avg_speed2,min_speed2,max_speed2, compass()))
          freq2+=add2

          if len(sense_temp)>= freq3:        
            avg_temp3=avg(sense_temp3)
            min_temp3=min(sense_temp3)
            max_temp3=max(sense_temp3)
            avg_hum3=avg(sense_hum3)
            min_hum3=min(sense_hum3)
            max_hum3=max(sense_hum3)
            avg_press3=avg(sense_press3)
            min_press3=min(sense_press3)
            max_press3=max(sense_press3)
            avg_dir3=mean_angle(wind_dir3)
            min_dir3=min(wind_dir3)
            max_dir3=max(wind_dir3)
            avg_speed3=avg(wind_speed3)
            min_speed3=min(wind_speed3)
            max_speed3=max(wind_speed3)           
            sense_data_3.extend((datetime.now(),avg_temp3,min_temp3,max_temp3,avg_hum3,min_hum3,max_hum3,avg_press3,min_press3,max_press3,avg_dir3,min_dir3,max_dir3,avg_speed3,min_speed3,max_speed3, compass()))
            freq3+=add3

        return sense_data,sense_data_2,sense_data_3,five_sec_data
        sense_data=[]
        if len(sense_temp)>=freq2 :
          sense_data_2=[]
        if len(sense_temp)>=freq3:
          sense_data_3=[]
        
#Main program################################################################
FILENAME = ""
FILENAME_2 = ""
FILENAME_3 = ""
FILENAME_4 = ""
#####File one minute
if FILENAME == "":
  filename = "/home/pi/Desktop/Sensors/Sense_Hat/1min-"+str(datetime.now())+".csv"
else:
  filename = FILENAME+"-"+str(datetime.now())+".csv"
#####File ten minutes
if FILENAME_2 == "":
  filename_2 = "/home/pi/Desktop/Sensors/Sense_Hat/10min-"+str(datetime.now())+".csv"
else:
  filename_2 = FILENAME_2+"-"+str(datetime.now())+".csv"
#####File one hour
if FILENAME_3 == "":
  filename_3 = "/home/pi/Desktop/Sensors/Sense_Hat/1hour-"+str(datetime.now())+".csv"
else:
  filename_3 = FILENAME_3+"-"+str(datetime.now())+".csv"
####File 5 sec
if FILENAME_4 == "":
    filename_4 = "/home/pi/Desktop/Sensors/Sense_Hat/5sec-"+str(datetime.now())+".csv"
else:
    filename_4 = FILENAME_4+"-"+str(datetime.now())+".csv"
#####creating files
file_setup(filename)
file_setup(filename_2)
file_setup(filename_3)
file_setup(filename_4)

#####initialization 
sense = SenseHat()
batch_data= []
batch_data_2= []
batch_data_3= []
batch_data_4= []
sense_data=[]
sense_data_2=[]
sense_data_3=[]
sense_temp=[]
sense_hum=[]
sense_press=[]
wind_dir=[]
wind_speed=[]
five_sec_data=[]

#while loop
#write every minute in the 1min file
while True:
  sense_data,sense_data_2,sense_data_3,five_sec_data= get_sense_data()
  if len(sense_data) >= 1:
     log_data()
     log_data_4()
     print("Writing to file..")
     with open(filename,"a") as f:
          for line in batch_data:
              f.write(line + "\n")
          sense_data=[]
          batch_data=[]
          copy(filename,"/home/pi/usbdrv/1min.csv")
    with open(filename_4,"a") as f:
        for line in batch_data_4:
            f.write(line+ "\n")
        five_sec_data=[]
        batch_data_4=[]
        copy(filename_4,"/home/pi/usbdrv/5sec.csv")


#write every 10 minutes in the 10min file
  if len(sense_data_2)>=1:
    log_data_2()
    print ("writing to file 2")
    with open(filename_2,"a") as f:
        for line in batch_data_2:
            f.write(line + "\n")
        sense_data_2=[]
        batch_data_2=[]
        copy(filename_2,"/home/pi/usbdrv/10min.csv")
        
#write every hour in the 1hour file      
  if len(sense_data_3)>=1:
    log_data_3()
    print ("writing to file 3")
    with open(filename_3,"a") as f:
        for line in batch_data_3:
            f.write(line + "\n")
        sense_data_3=[]
        batch_data_3=[]
        copy(filename_3,"/home/pi/usbdrv/1hour.csv")

