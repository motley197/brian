import sys
import time
import datetime
import math    
from EnvSensorCapability import EnvSensorCapability   

# Simulates a device for measuring air temperature, pressure and humidity
class MockedEnvSensor(EnvSensorCapability):

    def __init__(self, 
                 temp_min:  float = 0.0,  temp_max:  float = 30.0,
                 pres_min:  float = 900,  pres_max:  float = 1010,
                 humid_min: float = 20.0, humid_max: float = 99.0, 
                 cycle_time:int   = 60,   requirements = ["temp", "pres", "humid"]):
        
        # Initialise parent class
        super().__init__(has_temp=True, has_humidity=True, has_pressure=True, requirements=requirements)
        #self.set_requirements(requirements)

        print("Mocked Sensor")
        self.temp_mid = (temp_min + temp_max) * 0.5
        self.temp_amplitude = temp_max - self.temp_mid

        self.pres_mid = (pres_min + pres_max) * 0.5
        self.pres_amplitude = pres_max - self.pres_mid
        
        self.humid_mid = (humid_min + humid_max) * 0.5
        self.humid_amplitude = humid_max - self.humid_mid   

        self.T = cycle_time
        self.f = 1.0 / cycle_time

        self.start_time = time.perf_counter()

    def wave(self, phase=0.0) -> float:
        t = time.perf_counter() - self.start_time
        return math.sin(2*math.pi*self.f*t + phase)

    def read(self):
        ## Build up the data structure of measurements 
        now = datetime.datetime.now()
        env_params = {
            "time" : now
        }

        # Up to three different waveforms 20 degrees apart
        if (self.requirements["temp"]):
            t = self.wave(0.0)
            env_params["temp"] = (self.temp_mid + self.temp_amplitude * t)

        if (self.requirements["pres"]):
            p = self.wave(2.09)
            env_params["pres"] = (self.pres_mid + self.pres_amplitude * p)
        
        if (self.requirements["humid"]):
            h = self.wave(4.18)
            env_params["humid"] = (self.humid_mid + self.humid_amplitude * h)

        return env_params
    

# ***************************************************************************
# ********************************** Tests ********************************** 
# ***************************************************************************
#
# On the desktop, pip install pandas matplotlib
#

def test1():
    sen = MockedEnvSensor() # Default requirements will be ALL
    cap = sen.capability
    print(cap)
    vals = sen.read()
    print(vals)
    time.sleep(1)
    vals = sen.read()
    print(vals)

def test2():
    sen = MockedEnvSensor(cycle_time=6, requirements=["temp", "humid"])   # Limited the required measurements
    cap = sen.capability
    print(cap)
    vals = sen.read()
    print(vals)
    time.sleep(1)
    vals = sen.read()
    print(vals)

def test3():
    temp_sensor = MockedEnvSensor(cycle_time=6)
    readings = []
    times = []
    print('Simulating... please wait')
    for n in range(1,61,1):
        readings.append(temp_sensor.read())
        times.append(datetime.datetime.now())
        time.sleep(0.1)
    
    temp = []
    pres = []
    humid = []
    for n in range(0,60,1):
        print(f'{times[n]} : {readings[n]}')
        temp.append(readings[n]["temp"])
        pres.append(readings[n]["pres"])
        humid.append(readings[n]["humid"])
    
    if (sys.implementation.name == "cpython"):
        import matplotlib.pyplot as plt
        plt.plot(times,temp)
        plt.xticks(rotation=30, ha='right')
        plt.xlabel('Time')
        plt.ylabel('Temperature')
        plt.title('Mocked Temperature Sensor')
        plt.ylim((0,60))
        plt.show()

        plt.plot(times,pres)
        plt.xticks(rotation=30, ha='right')
        plt.xlabel('Time')
        plt.ylabel('Pressure')
        plt.title('Mocked Pressure Sensor')
        # plt.ylim((0,60))
        plt.show()

        plt.plot(times,humid)
        plt.xticks(rotation=30, ha='right')
        plt.xlabel('Time')
        plt.ylabel('Humidity')
        plt.title('Mocked Humidity Sensor')
        plt.ylim((0,100))
        plt.show()


test1()
test2()
test3()



