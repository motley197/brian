# Sensors Object
import sys
import time
import datetime
from MockedEnvSensor import MockedEnvSensor
from dht22sensor import DHT22_Env_Sensor


PYVER = sys.implementation.name

now = datetime.datetime.now()
now.strftime("%m/%d/%Y, %H:%M:%S")

def test_dht():
    sen = DHT22_Env_Sensor()
    cap = sen.capability
    print(cap)
    vals = sen.read()
    print(vals)
    time.sleep(1)
    vals = sen.read()
    print(vals)

def test_sim():
    sen = MockedEnvSensor() # Default requirements will be ALL
    cap = sen.capability
    print(cap)
    vals = sen.read()
    print(vals)
    time.sleep(1)
    vals = sen.read()
    print(vals)









