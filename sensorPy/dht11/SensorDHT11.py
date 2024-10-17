from sensor import Sensor
from SensorMeasurements import Temperature, RelativeHumidity
import adafruit_dht

class DHT11(Sensor):
    def __init__(self, pin):
        self.device = adafruit_dht.DHT11(pin)
        self.name = "DHT11"
        self.temperature = Temperature()
        self.relativeHumidity = RelativeHumidity()

    def _measure(self):
        self._tempMeasurementValues = {
            self.temperature: self.device.temperature,
            self.relativeHumidity: self.device.humidity
        }
