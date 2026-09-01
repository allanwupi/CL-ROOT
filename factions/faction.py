from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

from components.card import Card
from components.items import Item
from components.pieces import Piece
from rules.modifiers import Modifier
from ui.styles import Color

if TYPE_CHECKING:
    from board.clearing import Clearing
    from game.game import Game


class TurnPhase(Enum):
    BIRDSONG = 'Birdsong'
    DAYLIGHT = 'Daylight'
    EVENING = 'Evening'
    
    def __str__(self):
        color: Color = Color.NONE
        match (self):
            case TurnPhase.BIRDSONG:
                color = Color.BIRDSONG
            case TurnPhase.DAYLIGHT:
                color = Color.DAYLIGHT
            case TurnPhase.EVENING:
                color = Color.EVENING
        return color.style(self.value)


class Faction(ABC):
    def __init__(self, name: str, supply: dict[Piece, int], color: Color, handsize: int):
        self.name: str = name # Faction names should be unique
        self.abbr: str = ''.join([w[0] for w in name.split()])
        self.supply: dict[Piece, int] = supply
        self.color: Color = color
        self.handsize: int = handsize
        self.hand: list[Card] = []
        self.revealed: list[Card] = []
        self.items: dict[Item, int] = {}
        self.effects: set[Card] = set() # Cannot have duplicate crafted improvements
        self.modifiers: dict[Modifier, int] = dict()
        self.vp: int = 0
        self.game: Game | None = None
    
    def __getitem__(self, key: Piece) -> int:
        return self.supply[key]
    
    def __setitem__(self, key: Piece, value: int) -> None:
        self.supply[key] = value 

    def __repr__(self):
        return f"Faction(name={self.name!r}, supply={self.supply})"
    
    def __str__(self):
        return self.color.style(self.name)
    
    def draw(self, numcards: int = 1) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised")
        drawn: list[Card] = self.game.deck.draw(numcards)
        if self.handsize > 0:
            self.hand.extend(drawn)
        else:
            self.revealed.extend(drawn)
    
    def discard(self, pile: list[Card], card: Card) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised")
        pile.remove(card)
        self.game.deck.discard([card])

    @abstractmethod
    def setup(self, game: Game, homelands: list[Clearing] = list()):
        """Set up faction pieces following advanced setup rules."""
        pass
    
    @abstractmethod
    def birdsong(self):
        """Execute the birdsong phase."""
        pass
    
    @abstractmethod
    def daylight(self):
        """Execute the daylight phase."""
        pass
    
    @abstractmethod
    def evening(self):
        """Execute the evening phase."""
        pass


# We provide NullFaction as a container for pieces which aren't actually faction pieces
# Namely: items, ruins, dominance cards, scrapped pieces/cards (out of play)
class NullFaction(Faction):
    from random import shuffle
    def __init__(self, name: str = "No one"):
        super().__init__(
            name=name,
            supply={},
            color=Color.NONE,
            handsize=999
        )
    
    def setup(self, game: Game, homelands: list[Clearing] = list()):
        pass
    
    def birdsong(self):
        pass
    
    def daylight(self):
        pass
    
    def evening(self):
        pass