from sensor import Sensor, TemperatureSensor, RelativeHumiditySensor
import adafruit_shtc3
import board

class DHT22(Sensor, TemperatureSensor, RelativeHumiditySensor):
    def __init__(self, pin = board.I2C()):
        self.device = adafruit_shtc3.SHTC3(pin)
        self.name = "SHTC3"

    def _measure(self):
        t, rh = self.device.measurements
        self._tempMeasurementValues = {
            self.temperature: t,
            self.relativeHumidity: rh
        }