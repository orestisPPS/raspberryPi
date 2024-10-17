from enum import Enum
from abc import ABC, abstractmethod

class MeasurementType(Enum):
    Temperature = "T"
    RelativeHumidity = "RH"
    Pressure = "P"

    @property
    def getShortName(self):
        return self.value

class UnitBase(Enum, ABC):
    @abstractmethod
    def convert_value(self, value: float, target_unit: 'UnitBase') -> tuple:
        """Convert value to the requested unit."""
        pass

    @property
    @abstractmethod
    def get(self):
        """Get the unit symbol."""
        pass

    @property
    def get(self):
        return self.value
        
class UnitType(Enum):

    Meter = "m",         
    Gram = "g"         
    Second = "s"       
    Ampere = "A"        
    Kelvin = "K"        
    Candela = "cd"      
    Hertz = "Hz"       
    Newton = "N"       
    Pascal = "Pa"      
    Joule = "J"        
    Watt = "W"         
    Coulomb = "C"       
    Volt = "V"          
    Farad = "F"        
    Ohm = "Ω"           
    Siemens = "S"       
    Weber = "Wb"        
    Henry = "H"        
    Lumen = "lm"        
    Lux = "lx"         

    Celsius = "°C"
    Fahrenheit = "°F"
    Percent = "%"
    MillimeterOfMercury = "mmHg"
    InchOfMercury = "inHg"
    Bar = "bar"
    Atmosphere = "atm"

    @property
    def get(self):
        return self.value


class MetricPrefix(Enum):
    Yocto = "y" , 1e-24
    Zepto = "z" , 1e-21
    Atto  = "a" , 1e-18
    Femto = "f" , 1e-15
    Pico  = "p" , 1e-12
    Nano  = "n" , 1e-9
    Micro = "µ" , 1e-6
    Milli = "m" , 1e-3
    Centi = "c" , 1e-2
    Deci  = "d" , 1e-1
    Deca  = "da", 1e1
    Hecto = "h" , 1e2
    Kilo  = "k" , 1e3
    Mega  = "M" , 1e6
    Giga  = "G" , 1e9
    Tera  = "T" , 1e12
    Peta  = "P" , 1e15
    Exa   = "E" , 1e18
    Zetta = "Z" , 1e21
    Yotta = "Y" , 1e24
    

    def __init__(self, symbol):
        self._symbol = symbol
        self._factor = {
            "y": 1e-24, "z": 1e-21, "a": 1e-18, "f": 1e-15, "p": 1e-12, "n": 1e-9, "µ": 1e-6,
            "m": 1e-3, "c": 1e-2, "d": 1e-1, "da": 1e1, "h": 1e2, "k": 1e3, "M": 1e6, "G": 1e9,
            "T": 1e12, "P": 1e15, "E": 1e18, "Z": 1e21, "Y": 1e24
        }[symbol]
        self._description = {
            "y": "Yocto", "z": "Zepto", "a": "Atto", "f": "Femto", "p": "Pico", "n": "Nano", "µ": "Micro",
            "m": "Milli", "c": "Centi", "d": "Deci", "da": "Deca", "h": "Hecto", "k": "Kilo", "M": "Mega",
            "G": "Giga", "T": "Tera", "P": "Peta", "E": "Exa", "Z": "Zetta", "Y": "Yotta"
        }[symbol]

    @property
    def getSymbol(self):
        return self._symbol

    @property
    def getFullName(self):
        return self.name

    @property
    def getFactor(self):
        return self._factor

    @property
    def getDescription(self):
        return self._description
    
    class SIUnit(UnitBase):
        Meter = "m"        # Distance
        Gram = "g"         # Mass
        Second = "s"       # Time
        Ampere = "A"       # Electric current
        Kelvin = "K"       # Thermodynamic temperature
        Candela = "cd"     # Luminous intensity
        Hertz = "Hz"       # Frequency
        Newton = "N"       # Force
        Pascal = "Pa"      # Pressure
        Joule = "J"        # Energy
        Watt = "W"         # Power
        Coulomb = "C"      # Electric charge
        Volt = "V"         # Electric potential
        Farad = "F"        # Capacitance
        Ohm = "Ω"          # Electrical resistance
        Siemens = "S"      # Electrical conductance
        Weber = "Wb"       # Magnetic flux
        Tesla = "T"        # Magnetic flux density
        Henry = "H"        # Inductance
        Lumen = "lm"       # Luminous flux
        Lux = "lx"         # Illuminance

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

class MeasurementBase(ABC):
    def __init__(self):
        self.type = None
        self.unit = None
        self.supportedUnits = [None]
        self.colour = Colour.RESET
        self.value = 0.0
        self.burstValues = []

    @abstractmethod
    def convert_value(self, value: float, type: UnitType = None) -> tuple:
        """Convert value to the requested unit."""
        pass

    def _throwUnsupportedUnitError(self, unit: UnitType) -> None:
        raise ValueError(f"Unsupported unit type: {unit}. Supported unit types are: {self.supportedUnits}")

class Temperature(MeasurementBase):
    def __init__(self):
        self.type = MeasurementType.Temperature
        self.unit = UnitType.Celsius
        self.supportedUnits = [UnitType.Celsius, UnitType.Fahrenheit, UnitType.Kelvin]
        self.colour = Colour.ORANGE

    def convert_value(self, value: float, unit: UnitType = None) -> tuple:
        """Convert temperature from Celsius to the requested unit."""
        match unit:
            case None | UnitType.Celsius:
                return value, self.unit
            case UnitType.Fahrenheit:
                return value * 9/5 + 32, unit
            case UnitType.Kelvin:
                return value + 273.15, unit
            case _:
                self._throwUnsupportedUnitError(unit)

class RelativeHumidity(MeasurementBase):
    def __init__(self):
        self.type = MeasurementType.RelativeHumidity
        self.unit = UnitType.Percent
        self.supportedUnits = [UnitType.Percent]
        self.colour = Colour.BLUE

    def convert_value(self, value: float, unit: UnitType = None) -> tuple:
        """Convert relative humidity to the requested unit (no conversion needed)."""
        if unit is UnitType.Percent or unit is None :
            return value, self.unit
        else:
            self._throwUnsupportedUnitError(unit)

class Pressure(MeasurementBase):
    def __init__(self):
        self.type = MeasurementType.Pressure
        self.unit = UnitType.Hectopascal
        self.supportedUnits = [UnitType.Hectopascal, UnitType.Pascal, UnitType.MillimeterOfMercury,
                               UnitType.InchOfMercury, UnitType.Bar, UnitType.Atmosphere]
        self.colour = Colour.PURPLE
    def convert_value(self, value: float, unit: UnitType = None) -> tuple:
        """Convert pressure to the requested unit."""
        match unit:
            case None | UnitType.Hectopascal:
                return value, self.unit
            case UnitType.Pascal:
                return value * 100, unit
            case UnitType.MillimeterOfMercury:
                return value * 0.75006375541921, unit
            case UnitType.InchOfMercury:
                return value * 0.029529983071445, unit
            case UnitType.Bar:
                return value / 1000, unit
            case UnitType.Atmosphere:
                return value / 1013.25, unit
            case _:
                self._throwUnsupportedUnitError(unit)
