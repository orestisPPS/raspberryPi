from abc import ABC, abstractmethod
from sensor_measurements import Temperature, RelativeHumidity, Pressure, Colour
from sensor_units import UnitType
import time

class Sensor(ABC):
    def __init__(self):
        self.device = None
        self.name = ""
        self.colour = Colour.GREEN
        self.measurements = []

    def measure(self, consolePrint: bool = True, unitType: UnitType = None, useSymbol: bool = True) -> None:
        self._measure(isBurst=False)
        if consolePrint:
            print(f"{self.colour}{self.name}{Colour.RESET.getCode}")
            self.colour.print(self.name)
            for measurement in self.measurements:
                measurement.printValue(unitType, useSymbol)

    def burstMeasure(self, burstNum: int = 1, burstInterval: float = 2.0, burstDelay: float = 30,
                     consolePrint: bool = True, unitType: UnitType = None, useSymbol: bool = False) -> None:
        if burstNum < 1:
            raise ValueError("burstNum must be greater than 0")
        if burstInterval < 1:
            raise ValueError("burstInterval must be greater than or equal to 1")
        if burstDelay < 0:
            raise ValueError("burstDelay must be greater than or equal to 0")
        if consolePrint:
            self._printName()
        for i in range(burstNum):
            self._measure(isBurst=True)
            time.sleep(burstInterval)
        if consolePrint:
            for measurement in self.measurements:
                measurement.printValue(unitType, useSymbol)
        for measurement in self.measurements:
            measurement.resetBurstValues()
        time.sleep(burstDelay)
        

    @abstractmethod
    def _measure(self, isBurst: bool) -> None:
        pass
