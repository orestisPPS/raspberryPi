from sensor import Sensor
from sensor_measurements import Temperature, RelativeHumidity
import adafruit_shtc3
import board

class SHTC3(Sensor):
    def __init__(self, pin = board.I2C()):
        super().__init__() 
        self.device = adafruit_shtc3.SHTC3(pin)
        self.name = "SHTC3"
        self.temperature = Temperature()
        self.relativeHumidity = RelativeHumidity()
        self.measurements = [self.temperature, self.relativeHumidity]

    def _measure(self) -> list:
        return list(self.device.measurements)
        