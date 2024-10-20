from enum import Enum

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
    GREY = ("Grey", "\033[38;5;245m")
    RESET = ("Reset", "\033[0m")

    def getName(self) -> str:
        return self.value[0]
    
    def getCode(self) -> str:
        import re
        return re.sub(r'\033\[(\d+)(;\d+)*m', '', self.value[1])

    def print(self, message: str) -> None:
        print(f"{self.value[1]}{message}{Colour.RESET.value[1]}")

class PrintUtil:

    def printMessage(self, message: str, colour: Colour) -> None:
        print(f"{colour.getCode()}{message}{Colour.RESET.getCode()}")

    def printTitle(self, title: str, colour: Colour) -> None:
        print("=" * 50)
        print(f"{colour.getCode()}{title}{Colour.RESET.getCode()}")
        print("=" * 50)

    def printWarning(self, message: str) -> None:
        self.printMessage(message, Colour.YELLOW)

    def printException(self, message: str) -> None:
        self.printMessage(message, Colour.ORANGE)

    def printError(self, message: str) -> None:
        self.printMessage(message, Colour.RED)

    def printSuccess(self, message: str) -> None:
        self.printMessage(message, Colour.GREEN)

    def printInfo(self, message: str) -> None:
        self.printMessage(message, Colour.BLUE)