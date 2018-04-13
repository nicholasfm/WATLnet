import spidev
import time
import os
from time import sleep

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
    if (data<146.25 and data>123.75) :
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
    
    

while True :
    volts=ReadChannel(7)
    direction=ConvertDir(volts,2)
    cardinal=ConvertCard(direction)

    print (direction)
    print (cardinal)
    sleep(5)

    
