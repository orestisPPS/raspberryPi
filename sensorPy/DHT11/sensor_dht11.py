from sensor import Sensor
from sensor_measurements import Temperature, RelativeHumidity
import adafruit_dht

class DHT11(Sensor):
    def __init__(self, pin):
        super().__init__() 
        self.device = adafruit_dht.DHT11(pin)
        self.name = "DHT11"
        self.temperature = Temperature()
        self.relativeHumidity = RelativeHumidity()
        self.measurements = [self.temperature, self.relativeHumidity]

    def _measure(self) -> None:
        return [self.device.temperature, self.device.humidity]

