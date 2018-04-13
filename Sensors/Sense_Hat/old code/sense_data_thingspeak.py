from sense_hat import SenseHat
import time
from time import sleep
import httplib, urllib


sleep = 5 # how many seconds to sleep between posts to the channel
key = 'UH91408RP45V0C04'  # Thingspeak channel to update

#temperature to Thingspeak Channel
def temperature():
    while True:
        sense = SenseHat()
        sense.clear()
        temp =sense.get_temperature()
        params = urllib.urlencode({'field1': temp, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print (temp)
            print (response.status, response.reason)
            data = response.read()
            conn.close()
        except:
            print ("connection failed")
        break

def humidity():
    while True:
        sense = SenseHat()
        sense.clear()
        hum =sense.get_humidity()
        params = urllib.urlencode({'field2': hum, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print (hum)
            print (response.status, response.reason)
            data = response.read()
            conn.close()
        except:
            print ("connection failed")
        break

def pressure():
    while True:
        sense = SenseHat()
        sense.clear()
        press =sense.get_pressure()
        params = urllib.urlencode({'field3': press, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print (press)
            print (response.status, response.reason)
            data = response.read()
            conn.close()
        except:
            print ("connection failed")
        break

while True:
    humidity();
    time.sleep(sleep)
    temperature();
    time.sleep(sleep)
    pressure();
    time.sleep(sleep)
