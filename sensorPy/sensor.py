from abc import ABC, abstractmethod
from sensor_measurements import Temperature, RelativeHumidity, Pressure
from sensor_units import UnitType
from sensor_utility import Colour, PrintUtil
import time

class Sensor(ABC):
    def __init__(self):
        self.device = None
        self.name = ""
        self.colour = Colour.GREEN
        self.measurements = []

    def measure(self, consolePrint: bool = True, unitType: UnitType = None, useSymbol: bool = True) -> None:
        try:
            temp_measurements = self._measure()
            if all(value is not None for value in temp_measurements):
                for i, measurement in enumerate(self.measurements):
                    measurement.setValue(temp_measurements[i], False)
        except RuntimeError as error:
            print(f"Error reading from sensor {self.name}: {error}")
        except Exception as error:
            print(f"Unexpected error from sensor {self.name}: {error}")
        if consolePrint:
            PrintUtil().printTitle(self.name, self.colour)
            for measurement in self.measurements:
                measurement.printValue(unitType, useSymbol)
            print("")

    def burstMeasure(self, burstNum: int = 5, burstInterval: float = 2.0, burstDelay: float = 30,
                     consolePrint: bool = True, unitType: UnitType = None, useSymbol: bool = False) -> None:
        if burstNum < 1:
            raise ValueError("burstNum must be greater than 0")
        if burstInterval < 1:
            raise ValueError("burstInterval must be greater than or equal to 1")
        if burstDelay < 0:
            raise ValueError("burstDelay must be greater than or equal to 0")
        if consolePrint:
            PrintUtil().printTitle(self.name, self.colour)
        for i in range(burstNum):
            temp_measurements = self._measure()
            if all(value is not None for value in temp_measurements):
                for i, measurement in enumerate(self.measurements):
                    measurement.setValue(temp_measurements[i], True)
            time.sleep(burstInterval)
        if consolePrint:
            for measurement in self.measurements:
                measurement.printBurstValues(unitType, useSymbol)
        for measurement in self.measurements:
            measurement.resetBurstValues()
        time.sleep(burstDelay)
        

    @abstractmethod
    def _measure(self, isBurst: bool) -> list:
        pass
