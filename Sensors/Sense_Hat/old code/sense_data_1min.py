from sense_hat import SenseHat
from datetime import datetime
from time import sleep
import spidev
import time
import os
import RPi.GPIO as GPIO, time, os
from shutil import copy
#settings#

FILENAME = ""
#write in the file every minute
WRITE_FREQUENCY =12

#fuctions#

##WIND DIRECTION################################################################
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

#converting the voltage to 360 degrees direction 
def ConvertDir(data,places):
  degrees = (data * 360) / float(1023)
  degrees = round(degrees,places)
  return degrees

#converting degrees to cardinal direction 
def ConvertCard (data) :
    if (data<11.25 or data>348.75):
        return ("N")
    if (data<33.75 and data>11.25):
        return ("NNE")
    if (data<56.25 and data>33.75):
        return ("NE")
    if (data<78.75 and data>56.25):
        return ("ENE")
    if (data<101.25 and data>78.25):
        return ("E")
    if (data<123.75 and data>101.25):
        return ("ESE")
    if (data<146.25 and data>123.75):
        return ("SE")
    if (data<168.75 and data>146.25):
        return ("SSE")
    if (data<191.25 and data>168.75):
        return ("S")
    if (data<213.75 and data>191.25):
        return ("SSW")
    if (data<236.25 and data>213.75):
        return ("SW")    
    if (data<258.75 and data>236.25):
        return ("WSW")
    if (data<281.25 and data>258.75):
        return ("W")
    if (data<303.75 and data>281.25):
        return ("WNW")
    if (data<326.25 and data>303.75):
        return ("NW")
    if (data<348.75 and data>326.25):
        return ("NNW")
    
    
def WindDirection():
  while True :
    volts=ReadChannel(0)
    direction=ConvertDir(volts,2)
    cardinal=ConvertCard(direction)

    return direction

##WIND SPEED####################################################################
    
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
			state = True #closed
		# wait for switch for open
		if ((state == True) and (GPIO.input(speedPin) == False)):
			# State is now open!
			state = False
			# count it!
			counter = counter + 1
#	counter is the number of pulses during the sample time
#	speed is in km/h	
	speed = ((counter / samples)  * rfactor)
	return speed


###############################################################################


def log_data():
  output_string = ",".join(str(value) for value in sense_data)
  batch_data.append(output_string)

def file_setup(filename):
  header  =["Time", " Avg Temperature", " Min Temperature", " Max Temperature", " Avg Humidity", " Min Humidity", " Max Humidity", " Avg Pressure", " Min Pressure", " Max Pressure", " Avg Dir", " Min Dir", " Max Dir" " Avg Speed", " Min Speed", " Max Speed"]

  with open(filename,"w") as f:
      f.write(",".join(str(value) for value in header)+ "\n")

##
def avg(list):
    sum = 0
    for elm in list:
        sum += elm
    return (str(sum/(len(list))))




def get_sense_data():
  sense_data=[]
  sense_temp=[]
  sense_hum=[]
  sense_press=[]
  wind_dir=[]
  wind_speed=[]
  
  while True :
      sense_temp.append(sense.get_temperature_from_pressure())
      sense_hum.append(sense.get_humidity())
      sense_press.append(sense.get_pressure())
      wind_dir.append(WindDirection())
      wind_speed.append(getSpeed())

      if len(sense_temp)>= WRITE_FREQUENCY:
        avg_temp=avg(sense_temp)
        min_temp=min(sense_temp)
        max_temp=max(sense_temp)
        avg_hum=avg(sense_hum)
        min_hum=min(sense_hum)
        max_hum=max(sense_hum)
        avg_press=avg(sense_press)
        min_press=min(sense_press)
        max_press=max(sense_press)
        avg_dir=avg(wind_dir)
        min_dir=min(wind_dir)
        max_dir=max(wind_dir)
        avg_speed=avg(wind_speed)
        min_speed=min(wind_speed)
        max_speed=max(wind_speed)

        sense_data.append(datetime.now())
        sense_data.append(round(float(avg_temp),2))
        sense_data.append(round(float(min_temp),2))
        sense_data.append(round(float(max_temp),2))
        sense_data.append(round(float(avg_hum),2))
        sense_data.append(round(float(min_hum),2))
        sense_data.append(round(float(max_hum),2))
        sense_data.append(round(float(avg_press),2))
        sense_data.append(round(float(min_press),2))
        sense_data.append(round(float(max_press),2))
        sense_data.append(round(float(avg_dir)))
        sense_data.append(round(float(min_dir)))
        sense_data.append(round(float(max_dir)))
        sense_data.append(round(float(avg_speed),2))
        sense_data.append(round(float(min_speed),2))
        sense_data.append(round(float(max_speed),2))

        return sense_data

        sense_temp=[]
        sense_hum=[]
        sense_press=[]
        wind_dir=[]
        wind_speed=[]

        






#Main program##################################################################

sense = SenseHat()
counter=0
batch_data= []

if FILENAME == "":
  filename = "/home/pi/Desktop/Sensors/Sense_Hat/1min"+str(datetime.now())+".csv"
else:
  filename = FILENAME+"-"+str(datetime.now())+".csv"

file_setup(filename)

while True:
  sense_data= get_sense_data()
  log_data()
  sleep(0.1)

  if len(batch_data) >= 1:
      print("Writing to file..")
      
      with open(filename,"a") as f:
          for line in batch_data:
              f.write(line + "\n")
          batch_data = []
          counter+=1

  if counter>=1:
    copy(filename,"/home/pi/usbdrv/1min.csv")
    counter=0
