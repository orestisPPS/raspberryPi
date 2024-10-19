from enum import Enum, EnumMeta
from abc import ABC, abstractmethod
import time

class MeasurementType(Enum):
    Temperature = "T"
    RelativeHumidity = "RH"
    Pressure = "P"
    Distance = "D"
    Time = "t"

class UnitBase(ABC):
    @abstractmethod
    def convert_value(self, value: float, target_unit: 'UnitBase') -> tuple:
        """Convert value to the requested unit."""
        pass

    def getName(self):
        """Get the unit name string."""
        return self.name

    @property
    def getSymbol(self):
        return self.value

    def _throwUnsupportedUnitError(self, unit: 'UnitBase', supported_units: list) -> None:
        raise ValueError(f"Unsupported unit type: {unit}. Supported unit types are: {supported_units}")

class TemperatureUnit(UnitBase):
    Celsius = "°C"
    Fahrenheit = "°F"
    Kelvin = "K"

    def convert_value(self, value: float, target_unit: 'TemperatureUnit') -> tuple:
        """Convert temperature to the requested unit."""
        if target_unit == self.Celsius:
            return value, target_unit
        elif target_unit == self.Fahrenheit:
            return value * 9/5 + 32, target_unit
        elif target_unit == self.Kelvin:
            return value + 273.15, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [self.Celsius, self.Fahrenheit, self.Kelvin])

class RelativeHumidityUnit(UnitBase):
    Percent = "%"

    def convert_value(self, value: float, target_unit: 'RelativeHumidityUnit') -> tuple:
        """Convert relative humidity to the requested unit (no conversion needed)."""
        if target_unit == self.Percent:
            return value, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [self.Percent])

class PressureUnit(UnitBase):
    Hectopascal = "hPa"
    Pascal = "Pa"
    MillimeterOfMercury = "mmHg"
    InchOfMercury = "inHg"
    Bar = "bar"
    Atmosphere = "atm"

    def convert_value(self, value: float, target_unit: 'PressureUnit') -> tuple:
        """Convert pressure to the requested unit."""
        if target_unit == self.Pascal:
            return value, target_unit
        elif target_unit == self.Hectopascal:
            return value / 100, target_unit
        elif target_unit == self.MillimeterOfMercury:
            return value * 0.75006375541921, target_unit
        elif target_unit == self.InchOfMercury:
            return value * 0.029529983071445, target_unit
        elif target_unit == self.Bar:
            return value / 1000, target_unit
        elif target_unit == self.Atmosphere:
            return value / 1013.25, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [self.Pascal, self.Hectopascal, self.MillimeterOfMercury, self.InchOfMercury, self.Bar, self.Atmosphere])

class DistanceUnit(UnitBase):
    Meter = "m"
    Kilometer = "km"
    Centimeter = "cm"
    Millimeter = "mm"
    Inch = "in"
    Foot = "ft"
    Yard = "yd"

    def convert_value(self, value: float, target_unit: 'DistanceUnit') -> tuple:
        """Convert distance to the requested unit."""
        if target_unit == self.Meter:
            return value, target_unit
        elif target_unit == self.Kilometer:
            return value / 1000, target_unit
        elif target_unit == self.Centimeter:
            return value * 100, target_unit
        elif target_unit == self.Millimeter:
            return value * 1000, target_unit
        elif target_unit == self.Inch:
            return value * 39.3701, target_unit
        elif target_unit == self.Foot:
            return value * 3.28084, target_unit
        elif target_unit == self.Yard:
            return value * 1.09361, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [self.Meter, self.Kilometer, self.Centimeter, self.Millimeter, self.Inch, self.Foot, self.Yard])

class TimeUnit(UnitBase):
    Second = "s"
    Minute = "min"
    Hour = "h"
    Day = "d"

    def convert_value(self, value: float, target_unit: 'TimeUnit') -> tuple:
        """Convert time to the requested unit."""
        if target_unit == self.Second:
            return value, target_unit
        elif target_unit == self.Minute:
            return value / 60, target_unit
        elif target_unit == self.Hour:
            return value / 3600, target_unit
        elif target_unit == self.Day:
            return value / 86400, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [self.Second, self.Minute, self.Hour, self.Day])


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
    def getName(self):
        return self.value[0]
    
    @property
    def getCode(self):
        return self.value[1].replace("\033[", "").replace("m", "")

    def print(self, message: str):
        print(f"{self.value[1]}{message}{self.RESET.getCode}")

class MeasurementBase(ABC):
    def __init__(self):
        self.type = None
        self.unit = None
        self.colour = Colour.RESET
        self.value = 0.0
        self.burstValues = []
        self.avgBurstValue = 0.0

    def setValue(self, value: float, isBurst: bool) -> None:
        if isBurst:
            self.burstValues.append(value)
        else:
            self.value = value

    def getValue(self, unitType: UnitBase = None) -> tuple:
        if unitType is None:
            print(self.value, self.unit)
            return self.value, self.unit
        else:
            return self.unit.convert_value(self.value, unitType)

    def getBurstValues(self, unitType: UnitBase = None) -> list:
        if unitType is None:
            return self.burstValues
        else:
            convertedValues = []
            for value in self.burstValues:
                convertedValues.append(self.unit.convert_value(value, unitType))
            return convertedValues

    def resetBurstValues(self) -> None:
        self.burstValues = []

    def printValue(self, unitType: UnitBase = None, useSymbol: bool = False) -> None:
        """Print the value in the specified unit."""
        value, unit = self.getValue(unitType)
        # if useSymbol:
        #     self.colour.print(f"{value} {unit.getSymbol()}")
        # else:
        #     self.colour.print(f"{value} {unit.getName()}")

    def printBurstValues(self, unitType: UnitBase = None, useSymbol: bool = False, printArray: bool = True) -> None:
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
        self.unit = TemperatureUnit
        self.colour = Colour.ORANGE

class RelativeHumidity(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.type = MeasurementType.RelativeHumidity
        self.unit = RelativeHumidityUnit
        self.colour = Colour.BLUE

class Pressure(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.type = MeasurementType.Pressure
        self.unit = PressureUnit
        self.colour = Colour.GREEN

class Distance(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.unit = DistanceUnit
        self.colour = Colour.CYAN

class Time(MeasurementBase):
    def __init__(self):
        super().__init__()
        self.unit = TimeUnit
        self.colour = Colour.YELLOW