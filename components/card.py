from dataclasses import dataclass
from board.suit import Suit
from ui.styles import Color
from components.items import Item
from rules.modifiers import Modifier


@dataclass(frozen=True)
class Card:
    name: str
    suit: Suit
    cost: tuple[Suit, ...] | None = None
    item: Item | None = None
    persistent: bool = False
    effect: Modifier | None = None
        
    def __str__(self):
        suit_color: Color = self.suit.color
        return suit_color.style(self.name)