from time import sleep
import time
import RPi.GPIO as GPIO, time, os

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

while True :
    speed=getSpeed()
    print (speed)
