from enum import Enum
from abc import ABC, abstractmethod

class MeasurementType(Enum):
    Temperature = "T"
    RelativeHumidity = "RH"
    Pressure = "P"

    @property
    def getShortName(self):
        return self.value

class UnitType(Enum):
    Celsius = "°C"
    Fahrenheit = "°F"
    Kelvin = "K"
    Percent = "%"
    Pascal = "Pa"
    Hectopascal = "hPa"
    MillimeterOfMercury = "mmHg"
    InchOfMercury = "inHg"
    Bar = "bar"
    Atmosphere = "atm"

    @property
    def get(self):
        return self.value

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
    
    @property
    def print(self, message: str):
        print(f"{self.value[1]}{message}{Colour.RESET.getCode}")

class Measurement(ABC):
    def __init__(self):
        self.measurementType = None
        self.unitType = None
        self.value = None
        self.burstValues = None
        self.supportedUnits = []
        self.colour = Colour.RESET
    
    def getValue(self, unitType: UnitType = None) -> tuple:
        """Get the normal value in the specified unit."""
        return self.convert_value(self.value, unitType)

    def getBurstValues(self, unitType: UnitType = None) -> tuple:
        """Get the burst value in the specified unit."""
        if self.burstValues is None:
            return None
        return self.convert_value(self.burstValues, unitType)

    def setValue(self, value: float) -> None:
        self.value = value

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

    @abstractmethod
    def convert_value(self, value: float, unitType: UnitType = None) -> tuple:
        """Convert value to the requested unit."""
        pass

    def _print(self, value: float, unit: UnitType, useShortName: bool) -> None:
        name = self.measurementType.getShortName if useShortName else self.measurementType.name
        colourCode = self.colour.getCode
        resetCode = Colour.RESET.getCode
        print(f"{colourCode}{name} : {resetCode}{value} {colourCode}[{unit.get}]{resetCode}")

    def _throwUnsupportedUnitError(self, unitType: UnitType) -> None:
        raise ValueError(f"Unsupported unit type: {unitType}. Supported unit types are: {self.supportedUnits}")

class Temperature(Measurement):
    def __init__(self):
        self.measurementType = MeasurementType.Temperature
        self.unitType = UnitType.Celsius
        self.supportedUnits = [UnitType.Celsius, UnitType.Fahrenheit, UnitType.Kelvin]
        self.colour = Colour.ORANGE

    def convert_value(self, value: float, unitType: UnitType = None) -> tuple:
        """Convert temperature to the requested unit."""
        match unitType:
            case None | UnitType.Celsius:
                return value, self.unitType
            case UnitType.Fahrenheit:
                return value * 9/5 + 32, unitType
            case UnitType.Kelvin:
                return value + 273.15, unitType
            case _:
                self._throwUnsupportedUnitError(unitType)

class RelativeHumidity(Measurement):
    def __init__(self):
        self.measurementType = MeasurementType.RelativeHumidity
        self.unitType = UnitType.Percent
        self.supportedUnits = [UnitType.Percent]
        self.colour = Colour.BLUE

    def convert_value(self, value: float, unitType: UnitType = None) -> tuple:
        """Convert relative humidity to the requested unit (no conversion needed)."""
        if unitType is None or unitType == UnitType.Percent:
            return value, self.unitType
        else:
            self._throwUnsupportedUnitError(unitType)

class Pressure(Measurement):
    def __init__(self):
        self.measurementType = MeasurementType.Pressure
        self.unitType = UnitType.Hectopascal
        self.supportedUnits = [UnitType.Hectopascal, UnitType.Pascal, UnitType.MillimeterOfMercury,
                               UnitType.InchOfMercury, UnitType.Bar, UnitType.Atmosphere]
        self.colour = Colour.PURPLE
    def convert_value(self, value: float, unitType: UnitType = None) -> tuple:
        """Convert pressure to the requested unit."""
        match unitType:
            case None | UnitType.Hectopascal:
                return value, self.unitType
            case UnitType.Pascal:
                return value * 100, unitType
            case UnitType.MillimeterOfMercury:
                return value * 0.75006375541921, unitType
            case UnitType.InchOfMercury:
                return value * 0.029529983071445, unitType
            case UnitType.Bar:
                return value / 1000, unitType
            case UnitType.Atmosphere:
                return value / 1013.25, unitType
            case _:
                self._throwUnsupportedUnitError(unitType)
