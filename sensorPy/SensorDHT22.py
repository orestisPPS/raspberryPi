from sensor import Sensor, TemperatureSensor, RelativeHumiditySensor
import adafruit_dht

class DHT22(Sensor, TemperatureSensor, RelativeHumiditySensor):
    def __init__(self, pin):
        self.device = adafruit_dht.DHT11(pin)
        self.name = "DHT22"

    def measure(self):
        self.temperature.setValue(self.device.temperature)
        self.humidity.setValue(self.device.humidity)

