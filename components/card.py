from dataclasses import dataclass
from board.suit import Suit
from components.items import Item
from rules.modifiers import Modifier

@dataclass
class Card:
    name: str
    suit: Suit
    cost: list[Suit]
    item: Item | None
    effect: Modifier