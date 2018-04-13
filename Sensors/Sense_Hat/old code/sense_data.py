from sense_hat import SenseHat
from datetime import datetime
from time import sleep

#settings#

FILENAME = ""
#write in the file every minute
WRITE_FREQUENCY = 5

#fuctions#

def log_data():
  output_string = ",".join(str(value) for value in sense_data)
  batch_data.append(output_string)

def file_setup(filename):
  header  =["temperature","humidity","pressure",
  "timestamp"]

  with open(filename,"w") as f:
      f.write(",".join(str(value) for value in header)+ "\n")

def get_sense_data():
  sense_data=[]

  sense_data.append(sense.get_temperature_from_pressure())
  sense_data.append(sense.get_humidity())
  sense_data.append(sense.get_pressure())
  sense_data.append(datetime.now())

  return sense_data

#Main program#

sense = SenseHat()

batch_data= []

if FILENAME == "":
  filename = "/home/pi/Desktop/Sensors/Sense_Hat/SenseLog-"+str(datetime.now())+".csv"
else:
  filename = FILENAME+"-"+str(datetime.now())+".csv"

file_setup(filename)

while True:
  sense_data = get_sense_data()
  log_data()
  sleep (5)

  if len(batch_data) >= WRITE_FREQUENCY:
      print("Writing to file..")
      with open(filename,"a") as f:
          for line in batch_data:
              f.write(line + "\n")
          batch_data = []
          sleep(5)



sense_temp_avg=[]
            sense_hum_avg=[]
            sense_press_avg=[]
            wind_dir_avg=[]
            wind_speed_avg=[]
            sense_temp_min=[]
            sense_hum_min=[]
            sense_press_min=[]
            wind_dir_min=[]
            wind_speed_min=[]
            sense_temp_max=[]
            sense_hum_max=[]
            sense_press_max=[]
            wind_dir_max=[]
            wind_speed_max=[]
          
