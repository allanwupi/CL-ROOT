from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING

from board.suit import Suit

if TYPE_CHECKING:
    from factions.faction import Faction


class PieceType(IntEnum):
    # Lower number is higher priority in battle
    # TODO
    # This should probably be a property per faction
    WARRIOR = 0
    ITEM = 0
    TOKEN = 1
    BUILDING = 2
    PAWN = 3
    
    def __str__(self):
        return self.name.title()
    

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
    
    def __len__(self):
        return len(self.name)
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        owner: Faction = self.owner
        if self.piecetype == PieceType.BUILDING:
            return owner.color.style('['+self.name+']')
        return owner.color.style(self.name)