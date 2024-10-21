from abc import ABC, abstractmethod
from sensor_measurements import Temperature, RelativeHumidity, Pressure
from sensor_units import UnitType
from sensor_utility import Colour, SensorIO
import time

class Sensor(ABC):
    def __init__(self):
        self.device = None
        self.name = ""
        self.colour = Colour.GREEN
        self.measurements = []

    def measure(self, unitType: UnitType = None, burstNum: int = 1, burstInterval: float = 2.0,
                burstDelay: float = 30, printArray: bool = False,
                consolePrint: bool = True, useSymbol: bool = False, exportToCSV: bool = False, csvPath: str = None) -> None:
        
        self._checkMeasureInput(burstNum, burstInterval, burstDelay)
        if consolePrint: 
            SensorIO.printTitle(self.name, self.colour)
        isBurst = burstNum > 1
        for i in range(burstNum):
            try:
                temp_measurements = self._measure()
                if all(value is not None for value in temp_measurements):
                    for i, measurement in enumerate(self.measurements):
                        measurement.setValue(temp_measurements[i], isBurst)
            except RuntimeError as error:
                SensorIO.printError(f"Runtime Error reading from sensor {self.name}: {error}")
            except Exception as error:
               SensorIO.printError(f"Unexpected error from sensor {self.name}: {error}")
        if consolePrint:
            for measurement in self.measurements:
                if isBurst:
                    measurement.printBurstValues(unitType, useSymbol, printArray)
                else:
                    measurement.printValue(unitType, useSymbol)
            print("")
        if exportToCSV:
            self._exportSensorDataToCSV(isBurst, csvPath)

        for measurement in self.measurements:
                measurement.resetBurstValues()
        

    @abstractmethod
    def _measure(self, isBurst: bool) -> list:
        pass
        
    def _checkMeasureInput(self, burstNum: int, burstInterval: float, burstDelay: float) -> None:
        errors = []
        if burstNum < 1:
            errors.append("burstNum must be greater than 0")
        if burstInterval < 1:
            errors.append("burstInterval must be greater than or equal to 1")
        if burstDelay < 0:
            errors.append("burstDelay must be greater than or equal to 0")
        if errors:
            for error in errors:
                SensorIO().printError(f"ERROR: {error}")
            raise ValueError("Invalid input parameters")

    def _exportSensorDataToCSV(self, isBurst: bool,  path: str = None) -> None:
        names, data, units = [], [], []
        for measurement in self.measurements:
            names.append(measurement.getType().getSymbol())
            if isBurst:
                data.append(str(measurement.getAverageBurstValue()))
            else:
                data.append(str(measurement.getValue()))
            units.append(measurement.getUnit().getSymbol())
        SensorIO.exportToCSV(self.name, names, data, units, path)