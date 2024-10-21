from enum import Enum
from abc import ABC, abstractmethod
from sensor_units import TemperatureUnit, RelativeHumidityUnit, PressureUnit, DistanceUnit, TimeUnit, UnitType
from sensor_utility import Colour, SensorIO

class MeasurementType(Enum):
    Temperature = ("Temperature", "T", 1)
    RelativeHumidity = ("Relative Humidity", "RH", 2)
    Pressure = ("Pressure", "P", 3)
    Distance = ("Distance", "D", 4)
    Altitude = ("Altitude", "Alt", 5)
    Time = ("Time", "t", 6)
    TypeNone = ("TypeNone", "TypeNone", 0)

    def getName(self):
        return self.value[0]
    
    def getSymbol(self):
        return self.value[1]
    
    def getPriority(self):
        return self.value[2]

class MeasurementBase(ABC):
    def __init__(self):
        self.type = MeasurementType.TypeNone
        self.unit = UnitType.TypeNone
        self.colour = Colour.BLUE
        self.value = 0.0
        self.burstValues = []
        self.avgBurstValue = 0.0

    def getType(self) -> MeasurementType:
        return self.type

    def getUnit(self) -> UnitType:
        return self.unit

    def setValue(self, value: float, isBurst: bool) -> None:
        if isBurst:
            self.burstValues.append(value)
        else:
            self.value = value

    def getValue(self, unitType: UnitType = None) -> tuple:
        if unitType is None:
            return self.value, self.unit
        else:
            return self.unit.convert_value(self.value, unitType)

    def getBurstValues(self, unitType: UnitType = None) -> list:
        if unitType is None:
            return [(value, self.unit) for value in self.burstValues]
        else:
            convertedValues = []
            for value in self.burstValues:
                convertedValues.append((self.unit.convert_value(value, unitType), unitType))
            return convertedValues

    def getAverageBurstValue(self, unitType: UnitType = None) -> float:
        if len(self.burstValues) == 0:
            return 0.0
        if unitType is None:
            return sum(self.burstValues) / len(self.burstValues)
        else:
            convertedValues = []
            for value in self.burstValues:
                convertedValues.append(self.unit.convert_value(value, unitType))
            return sum(convertedValues) / len(convertedValues)

    def resetBurstValues(self) -> None:
        self.burstValues = []

    def printValue(self, unitType: UnitType = None, useSymbol: bool = True) -> None:
        """Print the value in the specified unit."""
        value, unit = self.getValue(unitType)
        string = f"{unit.getSymbol()}" if useSymbol else f"{unit.getType().getSymbol()}"
        label = f"{self.type.getName()}"
        formatted_output = f"{label:<20} : {value:>10.2f}  [{string:<4}]"
        SensorIO.printMessage(formatted_output, self.colour)

    
    def printBurstValues(self, unitType: UnitType = None, useSymbol: bool = False, printArray: bool = True) -> None:
        """Print the value in the specified unit."""
        burstData = self.getBurstValues(unitType)
        values = [value[0] for value in burstData]
        unit = burstData[0][1]
        average = sum(values) / len(values)
        string = f"{unit.getSymbol()}" if useSymbol else f"{unit.getType().getSymbol()}"
        label = f"{self.type.getName()}"
        if printArray:
            formatted_output = f"{label:<20} : {average:>10.2f}  [{string:<4}] {values}"
        else:
            formatted_output = f"{label:<20} : {average:>10.2f}  [{string:<4}]"
        SensorIO.printMessage(formatted_output, self.colour)

class Temperature(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.type = MeasurementType.Temperature
        self.unit = TemperatureUnit()
        self.colour = Colour.ORANGE

class RelativeHumidity(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.type = MeasurementType.RelativeHumidity
        self.unit = RelativeHumidityUnit()
        self.colour = Colour.BLUE

class Pressure(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.type = MeasurementType.Pressure
        self.unit = PressureUnit()
        self.colour = Colour.PURPLE

class Distance(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.unit = DistanceUnit()
        self.colour = Colour.CYAN

class Altitude(Distance):
    def __init__(self):
        super().__init__()
        self.type = MeasurementType.Altitude

class Time(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.unit = TimeUnit()
        self.colour = Colour.YELLOW