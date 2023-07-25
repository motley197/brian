

from machine import Pin
import dht
import datetime

from EnvSensorCapability import EnvSensorCapability     

class DHT22_Env_Sensor(EnvSensorCapability):
     def __init__(self, data_pin: int = 2, requirements = ["temp", "humid"]):
          super().__init__(has_temp=True, has_humidity=True, requirements=requirements)
          self.sensor = dht.DHT22(Pin(data_pin))

     def read(self):
          # This everything - this driver is all or nothing
          self.sensor.measure()
          now = datetime.datetime.now() # Log the time

          env_params = {
               "time" : now
          }

          # Populate the required parameters
          if (self.requirements["temp"]):
               env_params["temp"] = self.sensor.temperature()

          if (self.requirements["humid"]):
               env_params["humid"] = self.sensor.humidity()

          return env_params
    
# ***************************************************************************
# ********************************** Tests ********************************** 
# ***************************************************************************

import time
def test1():
    sen = DHT22_Env_Sensor() # Test for both measurements
    cap = sen.capability
    print(cap)
    vals = sen.read()
    print(vals)
    time.sleep(1)
    vals = sen.read()
    print(vals)

def test2():
    sen = DHT22_Env_Sensor(requirements=["temp"]) # Only require temperature
    cap = sen.capability
    print(cap)
    vals = sen.read()
    print(vals)
    time.sleep(1)
    vals = sen.read()
    print(vals)

def test3():
    sen = DHT22_Env_Sensor(requirements=["humid"]) # Only require humidity
    cap = sen.capability
    print(cap)
    vals = sen.read()
    print(vals)
    time.sleep(1)
    vals = sen.read()
    print(vals)

def test4():
    print("Checking exceptions")
    try:     
          sen = DHT22_Env_Sensor(requirements=["pres"]) # We require pressure, but it does not support it!
          cap = sen.capability
          print(cap)
          vals = sen.read()
          print(vals)
          time.sleep(1)
          vals = sen.read()
          print(vals)
    except:
        print("Correctly detected that pressure is not supported with this sensor")

test1()
test2()
test3()
test4()
