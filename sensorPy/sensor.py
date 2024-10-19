from abc import ABC, abstractmethod
from SensorMeasurements import Temperature, RelativeHumidity, Pressure, UnitBase, Colour
import time
import board

class Sensor(ABC):
    def __init__(self):
        self.device = None
        self.name = ""
        self.sensorColour = Colour.GREEN.getCode
        self.measurements = []

    def measure(self, consolePrint: bool = True, unitType: UnitBase = None, useSymbol: bool = False) -> None:
        self._measure(isBurst=False)
        if consolePrint:
            for measurement in self.measurements:
                measurement.printValue(unitType, useSymbol)

    def burstMeasure(self, burstNum: int = 1, burstInterval: float = 2.0, burstDelay: float = 30,
                     consolePrint: bool = True, unitType: UnitBase = None, useSymbol: bool = False) -> None:
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

    def _printName(self) -> None:
        print(f"{self.sensorColour}{self.name}{Colour.RESET.getCode}")

    @abstractmethod
    def _measure(self, isBurst: bool) -> None:
        pass
