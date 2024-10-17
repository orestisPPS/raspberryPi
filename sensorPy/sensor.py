from abc import ABC, abstractmethod
from SensorMeasurements import Temperature, RelativeHumidity, Pressure, UnitType, Colour
import time
import board

class Sensor(ABC):
    def __init__(self):
        self.device = None
        self.name = ""
        self.sensorColour = Colour.GREEN.getCode
        self.measurements = []
        self._tempMeasurementValues = {}

def measure(self, consolePrint: bool = True) -> None:
    self._setMeasurementValues(self._measure(), isBurst=False)
    if consolePrint: self._printMeasurements(isBurst=False)

def burstMeasure(self, burstNum: int = 1, burstInterval: float = 2.0, burstDelay: float = 30,
                 consolePrint: bool = True, fileSave: bool = False) -> None:
    if burstNum < 1: raise ValueError("burstNum must be greater than 0")
    if burstInterval < 1: raise ValueError("burstInterval must be greater than or equal to 1")
    if burstDelay < 0: raise ValueError("burstDelay must be greater than or equal to 0")
    if consolePrint: _printName()
    for i in range(burstNum):
        self._setMeasurementValues(self._measure(), isBurst=True)
        time.sleep(burstInterval)
    if consolePrint: self._printMeasurements(isBurst=True)
    time.sleep(burstDelay)


def _printName(self) -> None:
    print(f"{self.sensorColour}{self.name}{Colour.RESET.getCode}")

def _setMeasurementValues(self, values: dict, isBurst: bool) -> None:
    for measurement, value in values.items():
        measurement.setValue(value, isBurst)

def _printMeasurements(self, isBurst) -> None:
    _printName()
    for measurement in self.measurements:
        if isBurst:
            measurement.printBurstValues()
        else:
            measurement.printValue()

def _resetBurstValues(self) -> None:
    for measurement in self.measurements:
        measurement.resetBurstValues()



@abstractmethod
def _measure(self) -> None:
    pass




    def printValue(self, unitType: UnitType = None, useShortName: bool = False) -> None:
        """Print the value in the specified unit."""
        value, unit = self.getValue(unitType)
        self._print(value, unit, useShortName)

    def printBurstValues(self, unitType: UnitType = None, useShortName: bool = False) -> None:
        """Print the burst value in the specified unit."""
        burstValues = self.getBurstValues(unitType)
        if burstValues is None:
            return
        value, unit = burstValues
        self._print(value, unit, useShortName)

    def _print(self, value: float, unit: UnitType, useShortName: bool) -> None:
        """Helper method to handle printing the values in the specified unit."""
        name = self.type.getShortName if useShortName else self.type.name
        colourCode = self.colour.getCode
        resetCode = Colour.RESET.getCode
        print(f"{colourCode}{name} : {resetCode}{value} {colourCode}[{unit.get}]{resetCode}")