from enum import Enum
from abc import ABC, abstractmethod

class UnitType(Enum):
    # Temperature
    Celsius = ("Celsius", "°C", 1)
    Fahrenheit = ("Fahrenheit", "°F", 2)
    Kelvin = ("Kelvin", "K", 3)
    # Relative Humidity
    Percent = ("Percent", "%", 4)
    # Pressure
    Pascal = ("Pascal", "Pa", 5)
    Hectopascal = ("Hectopascal", "hPa", 6)
    Kilopascal = ("Kilopascal", "kPa", 7)
    MillimeterOfMercury = ("Millimeter of Mercury", "mmHg", 8)
    InchOfMercury = ("Inch of Mercury", "inHg", 9)
    Bar = ("Bar", "bar", 10)
    Atmosphere = ("Atmosphere", "atm", 11)
    PSI = ("PSI", "psi", 12)
    # Distance
    Meter = ("Meter", "m", 13)
    Kilometer = ("Kilometer", "km", 14)
    Centimeter = ("Centimeter", "cm", 15)
    Millimeter = ("Millimeter", "mm", 16)
    Inch = ("Inch", "in", 17)
    Foot = ("Foot", "ft", 18)
    Yard = ("Yard", "yd", 19)
    # Time
    Microsecond = ("Microsecond", "µs", 20)
    Millisecond = ("Millisecond", "ms", 21)
    Second = ("Second", "s", 22)
    Minute = ("Minute", "min", 23)
    Hour = ("Hour", "h", 24)
    Day = ("Day", "d", 25)
    # None
    TypeNone= ("TypeNone", "TypeNone", 0)

    def getName(self):
        return self.value[0]
    
    def getSymbol(self):
        return self.value[1]
    
    def getID(self):
        return self.value[2]
    
    
class UnitBase(ABC):
    def __init__(self):
        self._type = UnitType.TypeNone

    def getType(self) -> UnitType:
        return self._type

    @abstractmethod
    def convert_value(self, value: float, target_unit: UnitType) -> tuple:
        pass
    
    def _throwUnsupportedUnitError(self, target_unit: UnitType, supported_units: list):
        raise ValueError(f"Conversion to {target_unit} is not supported. Supported units are {supported_units}.")
    
class TemperatureUnit(UnitBase):
    def __init__(self):
        self._type = UnitType.Celsius

    def convert_value(self, value: float, target_unit: UnitType) -> tuple:
        if target_unit == UnitType.Celsius:
            return value, target_unit
        elif target_unit == UnitType.Fahrenheit:
            return value * 9/5 + 32, target_unit
        elif target_unit == UnitType.Kelvin:
            return value + 273.15, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [UnitType.Celsius, UnitType.Fahrenheit, UnitType.Kelvin])

class RelativeHumidityUnit(UnitBase):
    def __init__(self):
        self._type = UnitType.Percent

    def convert_value(self, value: float, target_unit: UnitType) -> tuple:
        if target_unit == UnitType.Percent:
            return value, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [UnitType.Percent])

class PressureUnit(UnitBase):
    def __init__(self):
        self._type = UnitType.Hectopascal

    def convert_value(self, value: float, target_unit: UnitType) -> tuple:
        if target_unit == UnitType.Pascal:
            return value, target_unit
        elif target_unit == UnitType.Hectopascal:
            return value / 100, target_unit
        elif target_unit == UnitType.Kilopascal:
            return value / 1000, target_unit
        elif target_unit == UnitType.MillimeterOfMercury:
            return value / 133.322, target_unit
        elif target_unit == UnitType.InchOfMercury:
            return value / 3386.39, target_unit
        elif target_unit == UnitType.Bar:
            return value / 100000, target_unit
        elif target_unit == UnitType.Atmosphere:
            return value / 101325, target_unit
        elif target_unit == UnitType.PSI:
            return value / 6894.76, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [UnitType.Pascal, UnitType.Hectopascal, UnitType.Kilopascal, UnitType.MillimeterOfMercury, UnitType.InchOfMercury, UnitType.Bar, UnitType.Atmosphere, UnitType.PSI])

class DistanceUnit(UnitBase):
    def __init__(self):
        self._type = UnitType.Meter

    def convert_value(self, value: float, target_unit: UnitType) -> tuple:
        if target_unit == UnitType.Meter:
            return value, target_unit
        elif target_unit == UnitType.Kilometer:
            return value / 1000, target_unit
        elif target_unit == UnitType.Centimeter:
            return value * 100, target_unit
        elif target_unit == UnitType.Millimeter:
            return value * 1000, target_unit
        elif target_unit == UnitType.Inch:
            return value * 39.3701, target_unit
        elif target_unit == UnitType.Foot:
            return value * 3.28084, target_unit
        elif target_unit == UnitType.Yard:
            return value * 1.09361, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [UnitType.Meter, UnitType.Kilometer, UnitType.Centimeter, UnitType.Millimeter, UnitType.Inch, UnitType.Foot, UnitType.Yard])

class TimeUnit(UnitBase):
    def __init__(self):
        self._type = UnitType.Second

    def convert_value(self, value: float, target_unit: UnitType) -> tuple:
        if target_unit == UnitType.Microsecond:
            return value * 1000000, target_unit
        elif target_unit == UnitType.Millisecond:
            return value * 1000, target_unit
        elif target_unit == UnitType.Second:
            return value, target_unit
        elif target_unit == UnitType.Minute:
            return value / 60, target_unit
        elif target_unit == UnitType.Hour:
            return value / 3600, target_unit
        elif target_unit == UnitType.Day:
            return value / 86400, target_unit
        else:
            self._throwUnsupportedUnitError(target_unit, [UnitType.Microsecond, UnitType.Millisecond, UnitType.Second, UnitType.Minute, UnitType.Hour, UnitType.Day])



def unitConverter(value: float, fromType: UnitType, toType: UnitType) -> float:
    converter = {
        # Temperature
        (UnitType.Celsius, UnitType.Fahrenheit): lambda x: x * 9/5 + 32,
        (UnitType.Celsius, UnitType.Kelvin): lambda x: x + 273.15,
        (UnitType.Fahrenheit, UnitType.Celsius): lambda x: (x - 32) * 5/9,
        (UnitType.Fahrenheit, UnitType.Kelvin): lambda x: (x - 32) * 5/9 + 273.15,
        (UnitType.Kelvin, UnitType.Celsius): lambda x: x - 273.15,
        (UnitType.Kelvin, UnitType.Fahrenheit): lambda x: (x - 273.15) * 9/5 + 32,
        # Pressure
        (UnitType.Pascal, UnitType.Hectopascal): lambda x: x / 100,
        (UnitType.Pascal, UnitType.Kilopascal): lambda x: x / 1000,
        (UnitType.Pascal, UnitType.MillimeterOfMercury): lambda x: x / 133.322,
        (UnitType.Pascal, UnitType.InchOfMercury): lambda x: x / 3386.39,
        (UnitType.Pascal, UnitType.Bar): lambda x: x / 100000,
        (UnitType.Pascal, UnitType.Atmosphere): lambda x: x / 101325,
        (UnitType.Pascal, UnitType.PSI): lambda x: x / 6894.76,
        (UnitType.Hectopascal, UnitType.Pascal): lambda x: x * 100,
        (UnitType.Hectopascal, UnitType.Kilopascal): lambda x: x / 10,
        (UnitType.Hectopascal, UnitType.MillimeterOfMercury): lambda x: x / 1.33322,
        (UnitType.Hectopascal, UnitType.InchOfMercury): lambda x: x / 33.8639,
        (UnitType.Hectopascal, UnitType.Bar): lambda x: x / 1000,
        (UnitType.Hectopascal, UnitType.Atmosphere): lambda x: x / 1013.25,
        (UnitType.Hectopascal, UnitType.PSI): lambda x: x / 68.9476,
        (UnitType.Kilopascal, UnitType.Pascal): lambda x: x * 1000,
        (UnitType.Kilopascal, UnitType.Hectopascal): lambda x: x * 10,
        (UnitType.Kilopascal, UnitType.MillimeterOfMercury): lambda x: x * 7.50062,
        (UnitType.Kilopascal, UnitType.InchOfMercury): lambda x: x / 3.38639,
        (UnitType.Kilopascal, UnitType.Bar): lambda x: x / 100,
        (UnitType.Kilopascal, UnitType.Atmosphere): lambda x: x / 101.325,
        (UnitType.Kilopascal, UnitType.PSI): lambda x: x / 6.89476,
        (UnitType.MillimeterOfMercury, UnitType.Pascal): lambda x: x * 133.322,
        (UnitType.MillimeterOfMercury, UnitType.Hectopascal): lambda x: x * 1.33322,
        (UnitType.MillimeterOfMercury, UnitType.Kilopascal): lambda x: x / 7.50062,
        (UnitType.MillimeterOfMercury, UnitType.InchOfMercury): lambda x: x / 25.4,
        (UnitType.MillimeterOfMercury, UnitType.Bar): lambda x: x / 750.062,
        (UnitType.MillimeterOfMercury, UnitType.Atmosphere): lambda x: x / 760,
        (UnitType.MillimeterOfMercury, UnitType.PSI): lambda x: x / 51.7149,
        (UnitType.InchOfMercury, UnitType.Pascal): lambda x: x * 3386.39,
        (UnitType.InchOfMercury, UnitType.Hectopascal): lambda x: x * 33.8639,
        (UnitType.InchOfMercury, UnitType.Kilopascal): lambda x: x * 3.38639,
        (UnitType.InchOfMercury, UnitType.MillimeterOfMercury): lambda x: x * 25.4,
        (UnitType.InchOfMercury, UnitType.Bar): lambda x: x / 29.53,
        (UnitType.InchOfMercury, UnitType.Atmosphere): lambda x: x / 29.9213,
        (UnitType.InchOfMercury, UnitType.PSI): lambda x: x / 2.03602,
        (UnitType.Bar, UnitType.Pascal): lambda x: x * 100000,
        (UnitType.Bar, UnitType.Hectopascal): lambda x: x * 1000,
        (UnitType.Bar, UnitType.Kilopascal): lambda x: x * 100,
        (UnitType.Bar, UnitType.MillimeterOfMercury): lambda x: x * 750.062,
        (UnitType.Bar, UnitType.InchOfMercury): lambda x: x * 29.53,
        (UnitType.Bar, UnitType.Atmosphere): lambda x: x / 1.01325,
        (UnitType.Bar, UnitType.PSI): lambda x: x * 14.5038,
        (UnitType.Atmosphere, UnitType.Pascal): lambda x: x * 101325,
        (UnitType.Atmosphere, UnitType.Hectopascal): lambda x: x * 1013.25,
        (UnitType.Atmosphere, UnitType.Kilopascal): lambda x: x * 101.325,
        (UnitType.Atmosphere, UnitType.MillimeterOfMercury): lambda x: x * 760,
        (UnitType.Atmosphere, UnitType.InchOfMercury): lambda x: x * 29.9213,
        (UnitType.Atmosphere, UnitType.Bar): lambda x: x * 1.01325,
        (UnitType.Atmosphere, UnitType.PSI): lambda x: x * 14.696,
        (UnitType.PSI, UnitType.Pascal): lambda x: x * 6894.76,
        (UnitType.PSI, UnitType.Hectopascal): lambda x: x * 68.9476,
        (UnitType.PSI, UnitType.Kilopascal): lambda x: x * 6.89476,
        (UnitType.PSI, UnitType.MillimeterOfMercury): lambda x: x * 51.7149,
        (UnitType.PSI, UnitType.InchOfMercury): lambda x: x * 2.03602,
        (UnitType.PSI, UnitType.Bar): lambda x: x / 14.5038,
        (UnitType.PSI, UnitType.Atmosphere): lambda x: x / 14.696,
        # Distance
        (UnitType.Millimeter, UnitType.Centimeter): lambda x: x / 10,
        (UnitType.Millimeter, UnitType.Meter): lambda x: x / 1000,
        (UnitType.Millimeter, UnitType.Kilometer): lambda x: x / 1000000,
        (UnitType.Millimeter, UnitType.Inch): lambda x: x / 25.4,
        (UnitType.Millimeter, UnitType.Foot): lambda x: x / 304.8,
        (UnitType.Millimeter, UnitType.Yard): lambda x: x / 914.4,
        (UnitType.Centimeter, UnitType.Millimeter): lambda x: x * 10,
        (UnitType.Centimeter, UnitType.Meter): lambda x: x / 100,
        (UnitType.Centimeter, UnitType.Kilometer): lambda x: x / 100000,
        (UnitType.Centimeter, UnitType.Inch): lambda x: x / 2.54,
        (UnitType.Centimeter, UnitType.Foot): lambda x: x / 30.48,
        (UnitType.Centimeter, UnitType.Yard): lambda x: x / 91.44,
        (UnitType.Meter, UnitType.Millimeter): lambda x: x * 1000,
        (UnitType.Meter, UnitType.Centimeter): lambda x: x * 100,
        (UnitType.Meter, UnitType.Kilometer): lambda x: x / 1000,
        (UnitType.Meter, UnitType.Inch): lambda x: x * 39.3701,
        (UnitType.Meter, UnitType.Foot): lambda x: x * 3.28084,
        (UnitType.Meter, UnitType.Yard): lambda x: x * 1.09361,
        (UnitType.Kilometer, UnitType.Millimeter): lambda x: x * 1000000,
        (UnitType.Kilometer, UnitType.Centimeter): lambda x: x * 100000,
        (UnitType.Kilometer, UnitType.Meter): lambda x: x * 1000,
        (UnitType.Kilometer, UnitType.Inch): lambda x: x * 39370.1,
        (UnitType.Kilometer, UnitType.Foot): lambda x: x * 3280.84,
        (UnitType.Kilometer, UnitType.Yard): lambda x: x * 1093.61,
        (UnitType.Inch, UnitType.Millimeter): lambda x: x * 25.4,
        (UnitType.Inch, UnitType.Centimeter): lambda x: x * 2.54,
        (UnitType.Inch, UnitType.Meter): lambda x: x / 39.3701,
        (UnitType.Inch, UnitType.Kilometer): lambda x: x / 39370.1,
        (UnitType.Inch, UnitType.Foot): lambda x: x / 12,
        (UnitType.Inch, UnitType.Yard): lambda x: x / 36,
        (UnitType.Foot, UnitType.Millimeter): lambda x: x * 304.8,
        (UnitType.Foot, UnitType.Centimeter): lambda x: x * 30.48,
        (UnitType.Foot, UnitType.Meter): lambda x: x / 3.28084,
        (UnitType.Foot, UnitType.Kilometer): lambda x: x / 3280.84,
        (UnitType.Foot, UnitType.Inch): lambda x: x * 12,
        (UnitType.Foot, UnitType.Yard): lambda x: x / 3,
        (UnitType.Yard, UnitType.Millimeter): lambda x: x * 914.4,
        (UnitType.Yard, UnitType.Centimeter): lambda x: x * 91.44,
        (UnitType.Yard, UnitType.Meter): lambda x: x / 1.09361,
        (UnitType.Yard, UnitType.Kilometer): lambda x: x / 1093.61,
        (UnitType.Yard, UnitType.Inch): lambda x: x * 36,
        (UnitType.Yard, UnitType.Foot): lambda x: x * 3,
        # Time
        (UnitType.Microsecond, UnitType.Millisecond): lambda x: x / 1000,
        (UnitType.Microsecond, UnitType.Second): lambda x: x / 1000000,
        (UnitType.Microsecond, UnitType.Minute): lambda x: x / 60000000,
        (UnitType.Microsecond, UnitType.Hour): lambda x: x / 3600000000,
        (UnitType.Microsecond, UnitType.Day): lambda x: x / 86400000000,
        (UnitType.Millisecond, UnitType.Microsecond): lambda x: x * 1000,
        (UnitType.Millisecond, UnitType.Second): lambda x: x / 1000,
        (UnitType.Millisecond, UnitType.Minute): lambda x: x / 60000,
        (UnitType.Millisecond, UnitType.Hour): lambda x: x / 3600000,
        (UnitType.Millisecond, UnitType.Day): lambda x: x / 86400000,
        (UnitType.Second, UnitType.Microsecond): lambda x: x * 1000000,
        (UnitType.Second, UnitType.Millisecond): lambda x: x * 1000,
        (UnitType.Second, UnitType.Minute): lambda x: x / 60,
        (UnitType.Second, UnitType.Hour): lambda x: x / 3600,
        (UnitType.Second, UnitType.Day): lambda x: x / 86400,
        (UnitType.Minute, UnitType.Microsecond): lambda x: x * 60000000,
        (UnitType.Minute, UnitType.Millisecond): lambda x: x * 60000,
        (UnitType.Minute, UnitType.Second): lambda x: x * 60,
        (UnitType.Minute, UnitType.Hour): lambda x: x / 60,
        (UnitType.Minute, UnitType.Day): lambda x: x / 1440,
        (UnitType.Hour, UnitType.Microsecond): lambda x: x * 3600000000,
        (UnitType.Hour, UnitType.Millisecond): lambda x: x * 3600000,
        (UnitType.Hour, UnitType.Second): lambda x: x * 3600,
        (UnitType.Hour, UnitType.Minute): lambda x: x * 60,
        (UnitType.Hour, UnitType.Day): lambda x: x / 24,
        (UnitType.Day, UnitType.Microsecond): lambda x: x * 86400000000,
        (UnitType.Day, UnitType.Millisecond): lambda x: x * 86400000,
        (UnitType.Day, UnitType.Second): lambda x: x * 86400,
        (UnitType.Day, UnitType.Minute): lambda x: x * 1440,
        (UnitType.Day, UnitType.Hour): lambda x: x * 24,
    }
    
    if (fromType, toType) in converter:
        return converter[(fromType, toType)](value)
    else:
        raise ValueError(f"Conversion from {fromType} to {toType} is not supported.")