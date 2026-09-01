from enum import Flag, auto
from ui.styles import *

class Suit(Flag):
    NONE = 0
    FOX = auto()
    MOUSE = auto()
    RABBIT = auto()
    FROG = auto()
    BIRD = FOX | MOUSE | RABBIT | FROG
    WILD = ~NONE
    
    def color(self) -> Color:
        match (self):
            case Suit.FOX:
                return Color.FOX
            case Suit.MOUSE:
                return Color.MOUSE
            case Suit.RABBIT:
                return Color.RABBIT
            case Suit.FROG:
                return Color.FROG
            case Suit.BIRD:
                return Color.BIRD
        return Color.NONE
    
    def __str__(self):
        suitname: str = str(self.name).title()
        return self.color().color(suitname)
