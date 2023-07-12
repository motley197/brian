import time
import math

class MockedTemp:

    def __init__(self, min_temp: float =0.0, max_temp: float =30.0, cycle_time: int = 60*60*24):
        print("Mocked Sensor")
        self._min = min_temp
        self._max = max_temp
        self._zero = (max_temp + min_temp) * 0.5
        self._amplitude = max_temp - self._zero
        self._T = cycle_time
        self._f = 1.0 / cycle_time

        self.start_time = time.perf_counter()

    def wave(self) -> float:
        t = time.perf_counter() - self.start_time
        return math.sin(2*math.pi*self._f*t)

    def read(self):
        y = self._zero + self._amplitude * self.wave()
        return y
    
    def read_u16(self):
        u16 = 0.5*(self.wave() + 1.0)*65535
        return math.floor(u16+0.5)