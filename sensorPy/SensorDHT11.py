from sensor import Sensor, TemperatureSensor, RelativeHumiditySensor
import adafruit_dht

class DHT11(Sensor, TemperatureSensor, RelativeHumiditySensor):
    def __init__(self, pin):
        self.device = adafruit_dht.DHT11(pin)
        self.name = "DHT11"

    def measure(self):
        self.temperature.setValue(self.device.temperature)
        self.relativeHumidity.setValue(self.device.humidity)
