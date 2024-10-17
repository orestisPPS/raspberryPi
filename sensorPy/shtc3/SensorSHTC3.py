from sensor import Sensor
from SensorMeasurements import TemperatureSensor, RelativeHumiditySensor
import adafruit_shtc3
import board

class SHTC3(Sensor):
    def __init__(self, pin = board.I2C()):
        self.device = adafruit_shtc3.SHTC3(pin)
        self.name = "SHTC3"
        self.temperature = TemperatureSensor()
        self.relativeHumidity = RelativeHumiditySensor()

    def _measure(self):
        t, rh = self.device.measurements
        self._tempMeasurementValues = {
            self.temperature: t,
            self.relativeHumidity: rh
        }