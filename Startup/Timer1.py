import os
import sys
import time
import datetime
import subprocess
starttime=time.time()
while True:
	subprocess.call("/home/pi/Desktop/Sensors/Camera/camera.sh", shell=True)
	time.sleep(0.5)
