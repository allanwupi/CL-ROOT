from components.pieces import *
from ui.styles import Color
from factions.faction import _ENVIRONMENT


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
    itemtype: ItemType
    points: int
    suit: Suit
    crafting: bool = False # Will need to change this for the vagabond but that's a future problem
    movable: bool = False
    can_rule: bool = False
    can_battle: bool = False
    requires_slot: bool = False
    owner: Faction = _ENVIRONMENT
    suit: Suit = Suit.WILD
    piecetype: PieceType = PieceType.ITEM
    name: str = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(
            self, 'name',
            self.itemtype.value
        )
    
    def __repr__(self):
        return self.name.title()
    
    def __str__(self):
        color: Color = Color.NONE
        match (self):
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
        return color.style(str(self))


BAG: Item = Item(itemtype=ItemType.BAG, points=1, suit=Suit.MOUSE)
BOOT: Item = Item(itemtype=ItemType.BOOT, points=1, suit=Suit.RABBIT)
CROSSBOW: Item = Item(itemtype=ItemType.CROSSBOW, points=1, suit=Suit.FOX)
HAMMER: Item = Item(itemtype=ItemType.HAMMER, points=2, suit=Suit.FOX)
SWORD: Item = Item(itemtype=ItemType.SWORD, points=2, suit=Suit.FOX)
TEA: Item = Item(itemtype=ItemType.TEA, points=2, suit=Suit.MOUSE)
COINS: Item = Item(itemtype=ItemType.COINS, points=3, suit=Suit.RABBIT)


@dataclass(frozen=True)
class Ruin(Piece):
    name: str
    item: Item
    points: int = 1
    crafting: bool = False
    movable: bool = False
    can_rule: bool = False
    can_battle: bool = False
    owner: Faction = _ENVIRONMENT
    suit: Suit = Suit.WILD
    piecetype: PieceType = PieceType.BUILDING