import time
import board
import adafruit_shtc3

# uses board.SCL and board.SDA
sht = adafruit_shtc3.SHTC3(board.I2C())

while True:
    temperature, relative_humidity = sht.measurements
    print("Temperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % relative_humidity)
    print("")
    time.sleep(1)