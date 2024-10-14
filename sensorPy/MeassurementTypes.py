from enum import Enum
from abc import ABC, abstractmethod

class MeasurmentType(Enum):
    Temperature = "T"
    RelativeHumidity = "RH"
    Pressure = "P"

    @property
    def getShorName(self):
        return self.value

class MeasurementUnitType(Enum):
    Celsius = "°C"
    Fahrenheit = "°F"
    Kelvin = "K"
    Percent = "%"
    Hectopascal = "hPa"
    Pascal = "Pa"
    MillimeterOfMercury = "mmHg"
    InchOfMercury = "inHg"
    Bar = "bar"
    Atmosphere = "atm"

    @property
    def getUnit(self):
        return self.value


class Measurment(ABC):
    def __init__(self):
        self.unitType = None

    @abstractmethod
    def getValue(self, unitType: MeasurementUnitType = None) :
        return self.value, self.unitType

    def setValue(self, value: float) -> None:
        self.value = value
        self.value = value

class Temperature(Measurment):
    def __init__(self):
        self.unitType = MeasurementUnitType.Celsius

    def getValue(self, unitType: MeasurementUnitType = None) -> tuple:
        match unitType:
            case None | MeasurementUnitType.Celsius:
                return self.value, self.unitType
            case MeasurementUnitType.Fahrenheit:
                return self.value * 9/5 + 32, unitType
            case MeasurementUnitType.Kelvin:
                return self.value + 273.15, unitType
            case _:
                raise ValueError(f"Unsupported unit type: {unitType}")