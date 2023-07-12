from machine import I2C, Pin
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
import utime
import dht
import time

#import serial

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

sensor = dht.DHT22(Pin(2))

i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

file = open("Temps.txt", "w")

lcd.clear()

while True:
     sensor.measure()
     temp = sensor.temperature()
     hum = sensor.humidity()
     lcd.move_to(0,0)
     lcd.putstr("    Temp: ")
     lcd.move_to(10,0)
     lcd.putstr(str(temp))
     lcd.move_to(0,1)
     lcd.putstr("Humidity: ")
     lcd.move_to(10,1)
     lcd.putstr(str(hum))
     print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
     stamp = time.gmtime()
     hour = stamp[3]
     minute = stamp[4]
     file.write(str(hour) + ":" + str(minute) + " " + str(temp) + " " + str(hum) + '\n')
     sleep(300)