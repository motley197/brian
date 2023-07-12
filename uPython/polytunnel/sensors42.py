# Sensors Object

import time
import datetime
from MockedTempSensor import MockedTemp
import sys

PYVER = sys.implementation.name


class TempSensor:

    def __init__(self, concrete_obj):
        print("TempSensor")
        self.obj = concrete_obj
    
    # Power On Self Test
    def post(self):
        print("Temperature Sensor")
        y = self.obj.read()
        print(y)

    def read(self):
        return self.obj.read()
    
    def read_now(self, dp: int = 3, includeDate: bool = False):
        now = datetime.datetime.now()
        temp = self.read()

        if (includeDate == True):
            key = now.strftime("%m/%d/%Y, %H:%M:%S") 
        else:
            key = now.strftime("%H:%M:%S")

        val = str(round(temp,dp))
        res = {
            key : val    
        }

        return res


# 1. Create concrete temperature sensor object
# mocked = MockedTemp(min_temp=0.0, max_temp=30.0, cycle_time=6)

# 2. Pass object to temperature sensor class
# temp_sensor = TempSensor(mocked)





# ***************************************************************************
# ********************************** Tests ********************************** 
# ***************************************************************************
#
# On the desktop, pip install pandas matplotlib
#

def doTest1():
    mocked = MockedTemp(min_temp=5.0, max_temp=30.0, cycle_time=6)
    temp_sensor = TempSensor(mocked)
    temp = []
    times = []
    print('Simulating... please wait')
    for n in range(1,61,1):
        temp.append(temp_sensor.read())
        times.append(datetime.datetime.now())
        time.sleep(0.1)
    
    for n in range(0,60,1):
        print(f'{times[n]} : {temp[n]}')

    if (PYVER == "cpython"):
        import matplotlib.pyplot as plt
        plt.plot(times,temp)
        plt.xticks(rotation=30, ha='right')
        plt.xlabel('Time')
        plt.ylabel('Temperature')
        plt.title('Mocked Temperature Sensor')
        plt.ylim((0,60))
        plt.show()
    
def doTest2():
    mocked = MockedTemp(min_temp=5.0, max_temp=30.0, cycle_time=6)
    temp_sensor = TempSensor(mocked)
    print(temp_sensor.read_now(dp=1))
    print(temp_sensor.read_now(includeDate=True))

doTest1()
doTest2()





