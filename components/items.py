from components.pieces import *
from ui.styles import Color
from factions.faction import VOID

class ItemType(Enum):
    BAG = 'Bag'
    BOOT = 'Boot'
    CROSSBOW = 'Crossbow'
    HAMMER = 'Hammer'
    SWORD = 'Sword'
    TEA = 'Tea'
    COINS = 'Coins'


@dataclass(frozen=True)
class Item(Piece):
    name: str
    itemtype: ItemType
    points: int
    suit: Suit
    crafting: bool
    movable: bool = False
    can_rule: bool = False
    can_battle: bool = False
    requires_slot: bool = False
    owner: Faction = VOID
    suit: Suit = Suit.WILD
    piecetype: PieceType = PieceType.ITEM
    
    _ITEM_COLOR_MAP: dict[ItemType, Color] = {
        ItemType.BAG: Color.BAG,
        ItemType.BOOT: Color.BOOT,
        ItemType.CROSSBOW: Color.CROSSBOW,
        ItemType.HAMMER: Color.HAMMER,
        ItemType.SWORD: Color.SWORD,
        ItemType.TEA: Color.TEA,
        ItemType.COINS: Color.COINS
    }
    def __str__(self):
        color: Color = self._ITEM_COLOR_MAP.get(self.itemtype, Color.NONE)
        return color.color(self.itemtype.value)


@dataclass(frozen=True)
class Ruin(Piece):
    name: str
    item: Item
    points: int = 1
    crafting: bool = False
    movable: bool = False
    can_rule: bool = False
    can_battle: bool = False
    owner: Faction = VOID
    suit: Suit = Suit.WILD
    piecetype: PieceType = PieceType.BUILDING