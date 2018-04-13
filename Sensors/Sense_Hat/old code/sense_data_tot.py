from sense_hat import SenseHat
from datetime import datetime
from time import sleep
import spidev
import time
import os
import RPi.GPIO as GPIO, time, os
#settings#

FILENAME = ""
FILENAME_2 = ""
FILENAME_3 = ""


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
    volts=ReadChannel(7)
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

def log_data_2():
  output_string = ",".join(str(value) for value in sense_data_2)
  batch_data_2.append(output_string)


def file_setup(filename):
  header  =["Time", " Avg Temperature", " Min Temperature", " Max Temperature", " Avg Humidity", " Min Humidity", " Max Humidity", " Avg Pressure", " Min Pressure", " Max Pressure"]

  with open(filename,"w") as f:
      f.write(",".join(str(value) for value in header)+ "\n")

##
def avg(list):
    sum = 0
    for elm in list:
        sum += elm
    return (str(sum/(len(list))))

freq1=2
freq2=4
def get_sense_data():
  global freq1
  global freq2
  sense_data=[]
  sense_data_2=[]

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
        avg_dir=avg(wind_dir1)
        min_dir=min(wind_dir1)
        max_dir=max(wind_dir1)
        avg_speed=avg(wind_speed1)
        min_speed=min(wind_speed1)
        max_speed=max(wind_speed1)

        sense_data.extend((datetime.now(),avg_temp,min_temp,max_temp,avg_hum,min_hum,max_hum,avg_press,min_press,max_press,avg_dir,min_dir,max_dir,avg_speed,min_speed,max_speed))


        freq1+=2

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
          avg_dir2=avg(wind_dir2)
          min_dir2=min(wind_dir2)
          max_dir2=max(wind_dir2)
          avg_speed2=avg(wind_speed2)
          min_speed2=min(wind_speed2)
          max_speed2=max(wind_speed2)
          
          sense_data_2.append(datetime.now())
          sense_data_2.append(avg_temp2)
          sense_data_2.append(min_temp2)
          sense_data_2.append(max_temp2)
          sense_data_2.append(avg_hum2)
          sense_data_2.append(min_hum2)
          sense_data_2.append(max_hum2)
          sense_data_2.append(avg_press2)
          sense_data_2.append(min_press2)
          sense_data_2.append(max_press2)
          sense_data_2.append(avg_dir2)
          sense_data_2.append(min_dir2)
          sense_data_2.append(max_dir2)
          sense_data_2.append(avg_speed2)
          sense_data_2.append(min_speed2)
          sense_data_2.append(max_speed2)

          freq2+=4

        return sense_data,sense_data_2
        sense_data=[]
        if len(sense_temp)>= WRITE_FREQUENCY_2 :
          sense_data_2=[]
        

#Main program##################################################################

sense = SenseHat()

batch_data= []
batch_data_2= []

if FILENAME == "":
  filename = "/home/pi/Desktop/Sensors/Sense_Hat/1min-"+str(datetime.now())+".csv"
else:
  filename = FILENAME+"-"+str(datetime.now())+".csv"

if FILENAME_2 == "":
  filename_2 = "/home/pi/Desktop/Sensors/Sense_Hat/10min-"+str(datetime.now())+".csv"
else:
  filename_2 = FILENAME_2+"-"+str(datetime.now())+".csv"

file_setup(filename)
file_setup(filename_2)



sense_data=[]
sense_data_2=[]
sense_data_1h=[]
sense_temp=[]
sense_hum=[]
sense_press=[]
wind_dir=[]
wind_speed=[]


while True:
  sense_data,sense_data_2= get_sense_data()

  
  if len(sense_data) >= 1:
     log_data()
     print("Writing to file..")
     with open(filename,"a") as f:
          for line in batch_data:
              f.write(line + "\n")
          sense_data=[]
          batch_data=[]
          
  if len(sense_data_2)>=1:
    log_data_2()
    print ("writing to file 2")
    with open(filename_2,"a") as f:
        for line in batch_data_2:
            f.write(line + "\n")
        sense_data_2=[]
        batch_data_2=[]

     

      

