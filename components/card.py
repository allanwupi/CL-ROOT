from dataclasses import dataclass
from board.suit import Suit
from ui.styles import Color
from components.items import Item
from rules.modifiers import Modifier

@dataclass
class Card:
    name: str
    suit: Suit
    cost: list[Suit] | None = None
    item: Item | None = None
    persistent: bool = False
    effect: Modifier | None = None
    
    def __repr__(self):
        return self.name
        
    def __str_(self):
        suit_color: Color = self.suit.color
        return suit_color.style(self.name)