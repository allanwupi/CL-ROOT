from enum import Enum


class Style(Enum):
    RESET = "\x1b[0m"
    DIM = "\x1b[2m"
    BOLD = "\x1b[1m"
    ITALIC = "\x1b[3m"
    NOITALIC = "\x1b[23m"
    NORMAL = "\x1b[22m"
    
    def __str__(self):
        return f"{self.value}{self.name}\x1b[0m"
    
    def style(self, text: str):
        return f"{self.value}{text}\x1b[0m"


class Color(Enum):
    # Terminal colors
    ERROR = "\x1b[31m"
    WARNING = "\x1b[33m"
    SUCCESS = "\x1b[32m"
    
    # Suit colors
    NONE = "\x1b[2m"
    FOX = "\x1b[38;5;167m"
    MOUSE = "\x1b[38;5;216m"
    RABBIT = "\x1b[38;5;228m"
    FROG = "\x1b[38;5;71m"
    BIRD = "\x1b[38;5;80m"
    
    # Faction colors
    ORANGE = "\x1b[38;5;208m"
    PINK = "\x1b[38;5;183m"
    
    # Turn phase colors
    BIRDSONG = "\x1b[38;5;179m"
    DAYLIGHT = "\x1b[38;5;117m"
    EVENING = "\x1b[38;5;244m"
    
    # Item colors
    BAG = "\x1b[38;5;107m"
    BOOT = "\x1b[38;5;131m"
    CROSSBOW = "\x1b[38;5;247m"
    HAMMER = "\x1b[38;5;103m"
    SWORD = "\x1b[38;5;7m"
    TEA = "\x1b[38;5;111m"
    COINS = "\x1b[38;5;222m"
    RUIN = "\x1b[38;5;243m"
    
    def __str__(self):
        return f"{self.value}{self.name}\x1b[0m"

    def style(self, text: str):
        return f"{self.value}{text}\x1b[0m"