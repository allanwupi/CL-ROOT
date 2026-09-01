# from board.path import Path
from board.suit import Suit
from board.location import Location
from ui.styles import Color

class Clearing:
    BLOCKED_SLOT: str = '[#]'
    FREE_SLOT: str = '[ ]'
    
    def __init__(self, number: int, name: str, suit: Suit, adjlist: list[int], slots: list[str]):
        self.number: int = number
        self.name: str = name
        self.suit: Suit = suit
        self.slots: list[str] = slots
        self.adjlist: list[int] = adjlist
        self.presence: dict[str, str] = dict()
        self.location: Location = Location.from_number(self.number)
        self.chosen: bool = False # Chosen as homeland
    
    def __str_(self):
        suit_color: Color = self.suit.color()
        return suit_color.color(self.name.title())