#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")
 
raspistill -t 43200000 -tl 5000 -q 10 -n -vf -hf -o /home/pi/usbdrv/Timelapse/$DATE.jpg