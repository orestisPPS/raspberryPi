from abc import ABC, abstractmethod
from MeassurementTypes import Measurement, Temperature, RelativeHumidity, Pressure, MeasurementUnitType, Colour
import time
import board

class Sensor(ABC):
    def __init__(self):
        self.device = None

@abstractmethod
def measure(self) -> None:
    pass

def burstMeasure(self, burstNum: int, burstInterval: float, burstDelay: float,
                 consolePrint: bool = True, fileSave: bool = False) -> None:
    for i in range(burstNum):
        self.measure()
        time.sleep(burstInterval)
    time.sleep(burstDelay)
    

class TemperatureSensor(Sensor):
    def __init__(self):
        self.device = None
        self.temperature = Temperature()

    def measure(self):
        pass

class RelativeHumiditySensor(Sensor):
    def __init__(self):
        self.device = None
        self.relativeHumidity = RelativeHumidity()

    def measure(self):
        pass

class PressureSensor(Sensor):
    def __init__(self):
        self.device = None
        self.pressure = Pressure()

    def measure(self):
        pass

