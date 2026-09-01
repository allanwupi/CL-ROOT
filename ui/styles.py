from enum import Enum


class Style(Enum):
    RESET = "\x1b[0m"
    DIM = "\x1b[2m"
    BOLD = "\x1b[1m"
    ERROR = "\x1b[31m"
    
    def __str__(self):
        return self.value
    
    def style(self, text):
        return f"{str(self)}{text}{Style.RESET}"


class Color(Enum):
    # Suits
    NONE = Style.DIM
    FOX = "\x1b[38;5;167m"
    MOUSE = "\x1b[38;5;216m"
    RABBIT = "\x1b[38;5;228m"
    FROG = "\x1b[38;5;71m"
    BIRD = "\x1b[38;5;80m"
    
    # Factions
    ORANGE = "\x1b[38;5;208m"
    
    # Items
    BAG = "\x1b[38;5;107m"
    BOOT = "\x1b[38;5;131m"
    CROSSBOW = "\x1b[38;5;247m"
    HAMMER = "\x1b[38;5;103m"
    SWORD = "\x1b[38;5;7m"
    TEA = "\x1b[38;5;111m"
    COINS = "\x1b[38;5;222m"

    def color(self, text):
        return f"{str(self)}{text}{Style.RESET}"