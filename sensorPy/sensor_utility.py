from enum import Enum
import os
import time

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
    def exportToCSV(sensorName: str, measurementNames: list,
                    measurementData: list, units: list, path: str = None) -> None:
        print_util = SensorIO()
        
        if len(measurementNames) != len(measurementData) or len(measurementNames) != len(units):
            print_util.printError("ERROR: Argument length mismatch - Measurement names, data, and units must have the same length.")
            return

        if path is None:
            path = os.path.join(os.getcwd(), sensorName, "data")
        
        if not os.path.exists(path):
            os.makedirs(path)
            print_util.printMessage(f"Directory created successfully: {path}", Colour.DARK_GREY)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_path = os.path.join(path, f"{time.strftime('%Y%m%d')}.csv")
        
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                header = ",".join([f"{name} [{unit}]" for name, unit in zip(measurementNames, units)]) + "\n"
                file.write(header)
                print_util.printMessage(f"New file created: {file_path}", Colour.DARK_GREY)
                for data in measurementData:
                    line = ",".join([value for value in data]) + "\n"
                    file.write(line)
                print_util.printMessage(f"Data successfully written to {file_path}.", Colour.DARK_GREY)
        else:
            with open(file_path, 'a') as file:
                for data in measurementData:
                    line = ",".join([str(value) for value in data]) + "\n"
                    file.write(line)
                print_util.printMessage(f"Data successfully appended to {file_path}.", Colour.DARK_GREY)

