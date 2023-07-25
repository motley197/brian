####################################################################################################################################
# On-Chip Pico Temperature Sensor
#
# Used for testing or when not all devices are available in hardware
#
# Once you create an instance of this class, there is only one parameter you can enable ("temp")
#
# 
# The following two are identical
#  sensor =  Pico_Temp_Sensor(requirements=["temp"])
#  sensor =  MockedEnvSensor()
#
# If for some reason (I cannot think of) you wanted to drop temperature, you can set requirements to [""]
#
# To read a values as a dictionary of key-value pairs, use the read() API
#  vals = sensor.read()
# 
# Example output:
#   {
#     'time': datetime.datetime(2023, 7, 12, 22, 8, 45, 499411), 
#     'temp': 6.433710564175197, 
#   }
#
# The date and time are a datetime object.
#
####################################################################################################################################

import machine
import datetime

from EnvSensorCapability import EnvSensorCapability     

class Pico_Temp_Sensor(EnvSensorCapability):
     def __init__(self, data_pin: int = 2, requirements = ["temp"]):
          super().__init__(has_temp=True, requirements=requirements)
          self.sensor_temp = machine.ADC(4)
          self.conversion_factor = 3.3 / (65535)

     def read(self):
          # 5th ADC Channel of the Pico is connected to a temperature sensor
          reading = self.sensor_temp.read_u16() * self.conversion_factor
          now = datetime.datetime.now() # Log the time
            
          # From the official example code:
          # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
          # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
          temperature = 27.0 - (reading - 0.706)/0.001721

          env_params = {
               "time" : now
          }

          # Populate the required parameters
          if (self.requirements["temp"]):
               env_params["temp"] = temperature

          return env_params
     

# ***************************************************************************
# ********************************** Tests ********************************** 
# ***************************************************************************

#
# Run this on the pico
#
import time
def generateTempData():
    temp_sensor = Pico_Temp_Sensor()
    print('Testing for (approx) 60 seconds... get ready....')
    time.sleep(10)
    for n in range(0,60,1):
        print(b'{temp_sensor.read()}')
        time.sleep(1)
    
#
# On the desktop, pip install pandas matplotlib pyserial
#
# The data is captured over the serial/USB port (on Linux, /dev/ttyAC0 or /dev/ttyAC1)
#
# ref: https://pyserial.readthedocs.io/en/latest/shortintro.html
import serial
import sys
def test():
    if (sys.implementation.name == "cpython"):
        import matplotlib.pyplot as plt
        times = []
        temp = []
        sp = serial.Serial('/dev/ttyAC0', 115200)
        for n in range(0,60,1):
            pico_line = sp.readline()
            print(pico_line)
            datetime_val = pico_line["time"]
            temp_val = pico_line["temp"]
            times.append(datetime_val)
            temp.append(temp_val)
          
    
        plt.plot(times,temp)
        plt.xticks(rotation=0, ha='right')
        plt.ylabel('Temperature')
        plt.title('Pico Internal Temperature Sensor')
        plt.ylim((0,60))
        plt.show()
    else:
        print("This can only run on a host PC")
