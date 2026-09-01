from dataclasses import dataclass, field
from factions.faction import Faction
from board.suit import Suit
from enum import Enum


class PieceType(Enum):
    WARRIOR = 'Warrior'
    PAWN = 'Pawn'
    BUILDING = 'Building'
    TOKEN = 'Token'
    ITEM = 'Item'
    
    def __str__(self):
        return self.name
    

@dataclass(frozen=True)
class Piece:
    owner: Faction
    name: str
    piecetype: PieceType
    points: int
    suit: Suit
    movable: bool
    crafting: bool
    can_rule: bool = field(init=False)
    can_battle: bool = field(init=False)
    requires_slot: bool = field(init=False)
    
    def __post_init__(self):
        # Rule, move and building slot booleans are initialised based on piece type
        object.__setattr__(
            self, 'can_rule',
            self.piecetype in (PieceType.WARRIOR, PieceType.BUILDING)
        )
        object.__setattr__(
            self, 'can_battle',
            self.piecetype in (PieceType.WARRIOR, PieceType.PAWN)
        )
        object.__setattr__(
            self, 'requires_slot', self.piecetype == PieceType.BUILDING
        )
    
    def __str__(self):
        owner: Faction = self.owner
        if self.piecetype == PieceType.BUILDING:
            return owner.color.style('['+str(self.name)+']')
        return owner.color.style(str(self.name))