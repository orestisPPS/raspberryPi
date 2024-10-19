from sensor import Sensor
from SensorMeasurements import Temperature, RelativeHumidity
import adafruit_dht

class DHT11(Sensor):
    def __init__(self, pin):
        self.device = adafruit_dht.DHT11(pin)
        self.name = "DHT11"
        self.temperature = Temperature()
        self.relativeHumidity = RelativeHumidity()
        self.measurements = [self.temperature, self.relativeHumidity]

    def _measure(self, isBurst: bool) -> None:
        self.temperature.setValue(self.device.temperature, isBurst)
        self.relativeHumidity.setValue(self.device.humidity, isBurst)
