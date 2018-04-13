# WATLnet
Necessary code for building a Weather And TimeLapse (WATL) station network. Inspired by the Mesonet network (https://www.mesonet.org/) with an Australian twist for collecting fire behaviour data.

## Background

This code was originally written by Roland B. during his internship (2015), and then later adapted by Stan B. During his internship. Nick M. updated the doc into this readme, but the procedure and code described has not been tested since Stan's work, which may have included some on-the-fly updates for use in the field in 2016.

Still, it hopefully provides some use for those getting started with DIY weather stations.

## Introduction

### Linux and Raspbian and Basic functions - Some basics (by Stanislaus):

Take some time to play with the terminal, and make sure you are familiar with the basics commands. I won't list all of them, but I will rather point you the concept you should understand:

- From the Terminal, you generally operate in the directory /home/pi. So if you want to execute a script somewhere else, you need to provide the path to the other directory. That is very important. It is also very useful to understand the directory and how the folders are organised. Sometimes, you will spend days wondering why a script doesn't work whereas the only reason is that you are not executing it in the right directory.

- shebangs: this concept is linked with directories. The shebangs are at the beginning of each script, and enable you to call your script wherever they are provided you give the right path.

- permissions: some directories won't be accessible for everyone, but only for the root user. You need to ask yourself the question of the permission each time you create a script. Sometime you won't manage to run a script. Try again with root permission.

- scripts : most of my scripts are bash script (.sh) or python script (.py).

#### Typical commands:

`sudo` gives you root permission

`nano` open the nano editor, that will allow to edit your codes. For example, if I want to create the script test.sh in the Desktop, I will run 'nano /home/pi/Desktop/test.sh'

`shutdown -h now`

`reboot`

`cd` changes the directory


`python` this is when you want to run a python script. For example, if I want to run the script test.py written in the Desktop, I will run 'python /home/pi/Desktop/test.py'.
IMPORTANT : most of my python codes are written in Python 3, so instead of 'python' you need to run the command 'python3'

`apt-get update` This is a very useful command. Most of the time, when the installation of a software won't work, running this piece of code will get you out of trouble. For example, if I want to update Apache, I will run 'apt-get update Apache'. You need to have an Internet access to run this command.

Connecting to the Wifi :

To connect a raspberry Pi to the Wifi just follow those steps because you can find a lot of things on the internet and most of them are just going to make things worse.

Make the file:
`sudo nano /etc/network/interfaces`

Enter the script:

```
# interfaces(5) file used by ifup(8) and ifdown(8)
# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d


auto lo
iface lo inet loopback

iface eth0 inet manual

allow-hotplug wlan0
iface wlan0 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

allow-hotplug wlan1
iface wlan1 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

Make another:

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Enter the script:

```
ctrl_interface=/var/run/wpa_supplicant
eapol_version=1
ap_scan=1
fast_reauth=1
network={
       ssid="eduroam"
        scan_ssid=1
        key_mgmt=WPA-EAP
        eap=PEAP
        phase2="auth=PAP auth=MSCHAPV2"
        identity="uqxxxxxx@uq.edu.au"
        password="xxxxxxxxx"
}

```

### Mount a USB device:

To store the pictures and to save the data we use a USB flash drive here is how to install it and write into it:
```
sudo mkdir /home/pi/usbdrv
sudo chown -R pi:pi /home/pi/usbdrv
sudo mount /dev/sda1 /home/pi/usbdrv -o uid=pi,gid=pi
```

To check if it is mounted just do:
`ls -l /dev/sda*`

If you want to dismount the device:
```
sudo umount /dev/sda1
```

## WATLnet architecture

All the scripts that are used are on GitHub in the repository : uq-crg/watlnet
You need to ask to PhD Nicholas McCarthy to give you access to this repository, so you can add your stuffs.

Startup Script : The point of the global code is to run whenever the Raspberry is boot up. That is the role of the startup script. It is an inner script, stored in with the full path `/etc/rc.local`
This `rc.local` script is run each time the Raspberry is boot up. Therefore, I wrote the `Master.sh` code in the last lines of the Startup Script, so it is called each time the Raspberry start as below

```
#!/bin/sh -e

# rc.local

# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other value on error.

# In order to enable or disable this script just changes the execution bits.
# by default this script does nothing.
#put there all the script that you want to run when you boot the raspberry

/home/pi/Desktop/Startup/Master.sh

exit 0
```

You can see on the last line of the code that I call the `Master.sh` code.

`Master.sh` script: This code allows all the Timers codes to run together simultaneously.

`Timers` scripts : Each Timer runs a code in a loop. Therefore, to change the frequency of an action, you just need to modify this code. Keep in mind that the internal clock of the Raspberry is not perfect, and that you have time drifting. As the Timers codes call the internal time, the loops can be delayed as time drifts. To prevent time drifting from the internal clock of the Raspberry, an option is to use a Real Time Clock, an external device that you connect to the Raspberry, and the Raspberry will import this time instead of its own internal time.

The whole process looks like this:
![alt text](https://github.com/nicholasfm/WATLnet/blob/master/images/Workflow.png "Text")


## Connecting the sensors

![alt text](https://github.com/nicholasfm/WATLnet/blob/master/images/Pi_GPIO.png "Text")


Sense Hat :
![alt text](https://github.com/nicholasfm/WATLnet/blob/master/images/pins.png "Text")
- The Sense-Hat is made to be simple and use by kids..
- The easy way to connect it to the Pi is to plug it right in top of it but this solution uses all the GPIO and we need some room for the other sensors.
- The GPIO pins that have to be linked to the Sense-Hat are coloured in red : 15 connections


## Windvane Setup : Davis Anemometer 7911
The Davis anemometer has 4 output cables (Yellow, Green, Red, Black) corresponding to Power, Wind direction output, Ground and Wind speed output.

The wind speed output is easy to process using the Raspberry Pi because it gives a digital signal for each revolution of the wind cups.

The wind direction has an analogic output and so need a A/D converter to be read by the Pi. The converter we use is a MCP3008 with a 10-bit resolution using the SPI serial interface available on the Pi. The wiring of this converter goes like this:

![alt text](https://github.com/nicholasfm/WATLnet/blob/master/images/windvein.png "Text")

6 GPIO pins are used by the converter and the green cable from the anemometer can be plugged to any of the 7 channels.
You will see the wind direction going from 0 to 1023, and so easily convert it to degrees and cardinals.

### Enable the SPI interface :
Run: `sudo raspi-config`
-	Advanced Options -> SPI ->yes->OK->yes->OK->Finish


## Internal Clock :

The Raspberry has no internal clock. To set up the clock, you need to connect to a network that will give you automatically the UTC. Yet we might want to operate the weather station out of the network. Having a precise time even without Internet is crucial since we are going to take measures and timelapses that need to be precisely timed.

First, you need to wire the RTC module
VCC - PIN 2 (5.0 V)
GND - PIN 9 (GND)
SDA - PIN 3 (SDA)
SCL - PIN 5 (SCL)

See [Adafruit](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/wiring-the-rtc)

Then, you need to configure the Raspberry to detect the RTC:

Again, [Adafruit](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time)

NOTE : for a reason I still ignore, the UTC given by the UQ network is 2 hours in advance. That is important because you give the time to your clock thanks to the network. To make sure the clock is giving you the right time (and not the false UQ network time), you need first to manually set up the Raspberry time with this command
`sudo dpkg-reconfigure tzdata`
You will be proposed several UTC, check the Brisbane one. Once your Raspberry is manually set up to Brisbane UTC, you need to give this time to your clock once for all, by running
`sudo hwclock -w`
Check if it's working with the command
`sudo hwclock -r`
From now on, the RTC will always give this time.


## Set up a static IP address

Summary: The IP address of the Raspberry is dynamically assigned by the DHCP each time you boot up, and it is likely to change. To remotely access your raspberry, you need to make sure you have a static IP address. See [here](http://www.suntimebox.com/raspberry-pi-tutorial-course/week-3/day-5/)

#### Issues:
The static address given to the raspberry might be assigned to another device while the Raspberry is out of the network. You still need to figure out how to prevent this from happening.

## IO
In order to allow all the connections from the Pi to the different modules we decided to us a mini breadboard. The mini breadboard allows us to plug all the GPIO pins we need from the Raspberry Pi and connect them to one or more sensors. On the breadboard we will also have the A/D converter which converts the wind direction to a digital signal.


## More fun

Send an email from the Pi :
```
sudo apt-get install postfix mailutils
sudo apt-get install ssmtp
sudo nano /etc/ssmtp/ssmtp.conf:
root=postmaster
mailhub=smtp.gmail.com:587
hostname=raspberrypi
AuthUser=AGmailUserName@gmail.com
AuthPass=TheGmailPassword
FromLineOverride=YES
UseSTARTTLS=YES

echo "Hello world email body" | mail -s "Test Subject" recipientname@domain.com
```
