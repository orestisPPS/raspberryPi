from sensor import Sensor, TemperatureSensor, RelativeHumiditySensor
import adafruit_dht

class DHT22(Sensor, TemperatureSensor, RelativeHumiditySensor):
    def __init__(self, pin):
        self.device = adafruit_dht.DHT11(pin)
        self.name = "DHT22"

    def _measure(self):
        self._tempMeasurementValues = {
            self.temperature: self.device.temperature,
            self.relativeHumidity: self.device.humidity
        }


