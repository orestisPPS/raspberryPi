import time
from dht11.SensorDHT11 import DHT11
from dht22.SensorDHT22 import DHT22
from shtc3.SensorSHTC3 import SHTC3
from SensorMeasurements import TemperatureUnit, PressureUnit, RelativeHumidityUnit, DistanceUnit, TimeUnit, Temperature, Pressure, RelativeHumidity, Distance, Time
import board


def main():
    dht11 = DHT11(board.D21)
    dht22 = DHT22(board.D17)
    # shtc3 = SHTC3()

    while True:
        dht11.measure(consolePrint=True, useSymbol=False)
        dht22.measure(consolePrint=True, useSymbol=False)
        # shtc3.measure(True, True)
        time.sleep(1)
 

if __name__ == "__main__":
    main()