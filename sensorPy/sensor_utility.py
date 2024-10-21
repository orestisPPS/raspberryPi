from enum import Enum
import os
import time
from collections.abc import Iterable

class Colour(Enum):
    RED = ("Red", "\033[91m")
    GREEN = ("Green", "\033[92m")
    TOXIC_GREEN = ("Toxic Green", "\033[38;5;10m")
    YELLOW = ("Yellow", "\033[93m")
    BLUE = ("Blue", "\033[94m")
    MAGENTA = ("Magenta", "\033[95m")
    CYAN = ("Cyan", "\033[96m")
    WHITE = ("White", "\033[97m")
    ORANGE = ("Orange", "\033[38;5;208m")
    PURPLE = ("Purple", "\033[38;5;141m")
    GREY = ("Grey", "\033[38;5;240m")
    LIGHT_GREY = ("Light Grey", "\033[38;5;250m")
    DARK_GREY = ("Dark Grey", "\033[38;5;236m")
    BRIGHT_PINK = ("Bright Pink", "\033[38;5;200m")
    VIOLET = ("Violet", "\033[38;5;57m")
    SKY_BLUE = ("Sky Blue", "\033[38;5;123m")
    GOLD = ("Gold", "\033[38;5;214m")
    RESET = ("Reset", "\033[0m")

    def getName(self) -> str:
        return self.value[0]
    
    def getCode(self) -> str:
        return self.value[1]

    def print(self, message: str) -> None:
        print(f"{self.getCode()}{message}{Colour.RESET.getCode()}")

class SensorIO:
    @staticmethod
    def printMessage(message: str, colour: Colour = Colour.WHITE) -> None:
        print(f"{colour.getCode()}{message}{Colour.RESET.getCode()}")

    @staticmethod
    def printTitle(title: str, colour: Colour) -> None:
        print("=" * 50)
        print(f"{colour.getCode()}{title}{Colour.RESET.getCode()}")
        print("=" * 50)

    @staticmethod
    def printWarning(message: str) -> None:
        SensorIO.printMessage(message, Colour.YELLOW)

    @staticmethod
    def printException(message: str) -> None:
        SensorIO.printMessage(message, Colour.ORANGE)

    @staticmethod
    def printError(message: str) -> None:
        SensorIO.printMessage(message, Colour.RED)

    @staticmethod
    def printSuccess(message: str) -> None:
        SensorIO.printMessage(message, Colour.GREEN)

    @staticmethod
    def printInfo(message: str) -> None:
        SensorIO.printMessage(message, Colour.BLUE)

    @staticmethod
    def exportToCSV(sensorName: str, measurementNames: list, measurementData: list, units: list, path: str = None) -> None:
        print_util = SensorIO()
        
        if len(measurementNames) != len(measurementData) or len(measurementNames) != len(units):
            print_util.printError("ERROR: Argument length mismatch - Measurement names, data, and units must have the same length.")
            return
        if path is None:
            path = os.path.join(os.getcwd(), sensorName, "data")
        if not os.path.exists(path):
            os.makedirs(path)
            print_util.printMessage(f"Directory created successfully: {path}", Colour.DARK_GREY)
        
        day = time.strftime("%Y_%m_%d")
        dateTime = time.strftime("%H:%M:%S")
        file_path = os.path.join(path, f"{sensorName}_{day}.csv")
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                header = "timestamp," + ",".join([f"{name}[{unit}]" for name, unit in zip(measurementNames, units)]) + "\n"
                file.write(header)
            print_util.printMessage(f"New file created: {file_path}", Colour.DARK_GREY)       
        with open(file_path, 'a') as file:
            # Ensure data is iterable
            if not isinstance(measurementData, Iterable):
                measurementData = [measurementData]  # Wrap it in a list if it's not iterable
            # Flatten the data into a single line
            line = f"{dateTime}," + ",".join([f"{float(value):.2f}" for value in measurementData]) + "\n"
            file.write(line)
            print_util.printMessage(f"Data successfully appended to {file_path}.", Colour.DARK_GREY)
