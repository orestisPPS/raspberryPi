from enum import Enum
from abc import ABC, abstractmethod
from sensor_units import TemperatureUnit, RelativeHumidityUnit, PressureUnit, DistanceUnit, TimeUnit, UnitType

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

class Colour(Enum):
    RED = ("Red", "\033[91m")
    GREEN = ("Green", "\033[92m")
    YELLOW = ("Yellow", "\033[93m")
    BLUE = ("Blue", "\033[94m")
    MAGENTA = ("Magenta", "\033[95m")
    CYAN = ("Cyan", "\033[96m")
    WHITE = ("White", "\033[97m")
    ORANGE = ("Orange", "\033[38;5;208m")
    PURPLE = ("Purple", "\033[38;5;141m")
    RESET = ("Reset", "\033[0m")

    @property
    def getName(self) -> str:
        return self.value[0]
    
    @property
    def getCode(self) -> str:
        import re
        return re.sub(r'\033\[(\d+)(;\d+)*m', '', self.value[1])

    def print(self, message: str) -> None:
        print(f"{self.value[1]}{message}{self.RESET.getCode}")

class MeasurementBase(ABC):
    def __init__(self):
        self.type = MeasurementType.TypeNone
        self.unit = UnitType.TypeNone
        self.colour = Colour.RESET
        self.value = 0.0
        self.burstValues = []
        self.avgBurstValue = 0.0

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
            return self.burstValues
        else:
            convertedValues = []
            for value in self.burstValues:
                convertedValues.append(self.unit.convert_value(value, unitType))
            return convertedValues

    def resetBurstValues(self) -> None:
        self.burstValues = []

    def printValue(self, unitType: UnitType = None, useSymbol: bool = True) -> None:
        """Print the value in the specified unit."""
        value, unit = self.getValue(unitType)
        string = f"{unit.getSymbol()}" if useSymbol else f"{unit.getType().getSymbol()}"
        label = f"{self.type.getName()}"
        formatted_output = f"{label:<20} : {value:>10.2f}  [{string:<4}]"
        self.colour.print(formatted_output)

    
    def printBurstValues(self, unitType: UnitType = None, useSymbol: bool = False, printArray: bool = True) -> None:
        """Print the burst values in the specified unit."""
        burstValues = self.getBurstValues(unitType)
        if not burstValues:
            return

        if printArray:
            values_str = ', '.join(f"{value[0]}" for value in burstValues)
            unit_str = unitType.getSymbol() if useSymbol else unitType.getName()
            print(f"{values_str} {unit_str}")
        else:
            for value in burstValues:
                value_str = f"{value[0]} {value[1].getSymbol()}" if useSymbol else f"{value[0]} {value[1].getName()}"
                self.colour.print(value_str)

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
        self.colour = Colour.GREEN

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