#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")
 
raspistill -q 10 -n -vf -hf -o /home/pi/usbdrv/Timelapse/$DATE.jpg