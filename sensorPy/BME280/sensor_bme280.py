from sensor import Sensor
from sensor_measurements import Temperature, RelativeHumidity, Pressure, Altitude
from adafruit_bme280 import basic as adafruit_bme280
import board



class BME280(Sensor):
    def __init__(self, pin = board.I2C(), address = 0x76):
        super().__init__() 
        self.device = adafruit_bme280.Adafruit_BME280_I2C(pin, address=address)
        self.name = "BME280"
        self.temperature = Temperature()
        self.relativeHumidity = RelativeHumidity()
        self.pressure = Pressure()
        self.altitude = Altitude()
        self.measurements = [self.temperature, self.relativeHumidity, self.pressure, self.altitude]
        self.sea_level_pressure = 1013.25
        self.device.sea_level_pressure = self.sea_level_pressure

    def _measure(self) -> None:
        return [
            round(self.device.temperature, 2),
            round(self.device.humidity, 2),
            round(self.device.pressure, 2),
            round(self.device.altitude, 2)
        ]

    def setSeaLevelPressure(self, pressure: float) -> None:
        self.sea_level_pressure = pressure
        self.device.sea_level_pressure = pressure