from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from board.suit import Suit
from components.pieces import Piece, PieceType
from ui.styles import Color

if TYPE_CHECKING:
    from factions.faction import NullFaction


class ItemType(Enum):
    BAG = 'Bag'
    BOOT = 'Boot'
    CROSSBOW = 'Crossbow'
    HAMMER = 'Hammer'
    SWORD = 'Sword'
    TEA = 'Tea'
    COINS = 'Coins'


@dataclass(frozen=True, kw_only=True)
class Item(Piece):
    owner: NullFaction
    itemtype: ItemType
    points: int
    suit: Suit
    crafting: bool = False # Will need to change this for the vagabond but that's a future problem
    movable: bool = False
    can_rule: bool = False
    can_battle: bool = False
    requires_slot: bool = False
    piecetype: PieceType = PieceType.ITEM
    name: str = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(
            self, 'name',
            self.itemtype.value
        )
    
    @property
    def color(self):
        color: Color = Color.NONE
        match (self.itemtype):
            case ItemType.BAG:
                color = Color.BAG
            case ItemType.BOOT:
                color = Color.BOOT
            case ItemType.CROSSBOW:
                color = Color.CROSSBOW
            case ItemType.HAMMER:
                color = Color.HAMMER
            case ItemType.SWORD:
                color = Color.SWORD
            case ItemType.TEA:
                color = Color.TEA
            case ItemType.COINS:
                color = Color.COINS
        return color
    
    @property
    def in_stock(self) -> bool:
        return self.owner.items[self] > 0
    
    def __str__(self):
        color: Color = self.color
        return color.style(self.name)


@dataclass(frozen=True, kw_only=True)
class Ruin(Piece):
    owner: NullFaction
    name: str
    item: Item
    points: int = 1
    crafting: bool = False
    movable: bool = False
    can_rule: bool = False
    can_battle: bool = False
    suit: Suit = Suit.WILD
    piecetype: PieceType = PieceType.BUILDING