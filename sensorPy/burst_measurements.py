import time
from dht11.SensorDHT11 import DHT11
from dht22.SensorDHT22 import DHT22
from bme280.sensor_bme280 import BME280
# from shtc3.SensorSHTC3 import SHTC3it, PressureUnit, RelativeHumidityUnit, DistanceUnit, TimeUnit, Temperature, Pressure, RelativeHumidity, Distance, Time
import board


def main():
    sensors = {
        "DHT11": DHT11(board.D21),
        "DHT22": DHT22(board.D17),
        "BME280": BME280()
        # "SHTC3": SHTC3()
    }
    while True:
        for sensor in sensors.values():
            sensor.measure(burstNum=5, burstInterval=2, burstDelay=10, exportToCSV=True)

if __name__ == "__main__":
    main()

