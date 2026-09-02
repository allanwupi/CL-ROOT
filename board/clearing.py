# from board.path import Path
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from board.location import Location
from board.suit import Suit
from components.pieces import Piece
from ui.styles import Color

if TYPE_CHECKING:
    from factions.faction import Faction


@dataclass(frozen=True)
class FactionPresence:
    faction: Faction
    numpieces: int
    rule: int
    battle: int


class Clearing:
    def __init__(self, number: int, name: str, suit: Suit, adjlist: list[int], slots: list[Piece | None]):
        self.number: int = number
        self.name: str = name
        self.suit: Suit = suit
        self.slots: list[Piece | None] = slots
        self.adjlist: list[int] = adjlist
        self.pieces: dict[Faction, dict[Piece, int]] = dict()
        self.location: Location = Location.from_number(self.number)
        print(self.number, self.location)
        self.homeland: bool = False # Chosen as homeland
    
    # Read-only, dynamically calculated fields for rule and presence
    @property
    def presence(self) -> list[FactionPresence]:
        faction_presence: list[FactionPresence] = []
        for faction in self.pieces.keys():
            numpieces: int = sum(count for count in self.pieces[faction].values())
            rule: int = sum(
                self.pieces[faction][piece]
                for piece in self.pieces[faction].keys() if piece.can_rule
            )
            battle: int = sum(
                self.pieces[faction][piece]
                for piece in self.pieces[faction].keys() if piece.can_battle
            )
            faction_presence.append(
                FactionPresence(faction, numpieces, rule, battle)
            )
        return faction_presence
    
    def faction_presence(self, key: Faction) -> FactionPresence:
        numpieces: int = sum(count for count in self.pieces[key].values())
        rule: int = sum(
                self.pieces[key][piece]
                for piece in self.pieces[key].keys() if piece.can_rule
            )
        battle: int = sum(
                self.pieces[key][piece]
                for piece in self.pieces[key].keys() if piece.can_battle
            )
        return(FactionPresence(key, numpieces, rule, battle))
    
    def has_piece(self, piece: Piece | None) -> bool:
        return (piece is None) or self.pieces[piece.owner][piece] > 0
    
    @property
    def ruler(self) -> Faction | None:
        factions_by_rule: list[FactionPresence] = sorted(
            self.presence,
            key=lambda x: x.rule, reverse=True
        )
        if len(factions_by_rule) == 0:
            return None # The higher-level board object will replace this with NullFaction
        elif len(factions_by_rule) > 1 and factions_by_rule[0].rule == factions_by_rule[1].rule:
            return None # On a tie, no one rules
        return factions_by_rule[0].faction

    @property
    def free(self) -> bool:
        return None in self.slots
    
    def build(self, building: Piece) -> None:
        first_free: int = self.slots.index(None)
        self.slots[first_free] = building
        
    def destroy(self, building: Piece) -> None:
        first_building: int = self.slots.index(building)
        self.slots[first_building] = None
    
    def __getitem__(self, key: Faction) -> dict[Piece, int]:
        return self.pieces[key]
    
    def __repr__(self):
        return self.name.lower()
        
    def __str__(self):
        suit_color: Color = self.suit.color
        return suit_color.style(self.name.title())