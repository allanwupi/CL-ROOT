from abc import ABC, abstractmethod
from game.game import Game
from board.clearing import Clearing
from ui.styles import Color
from components.pieces import Piece
from components.items import Item
from components.card import Card
from rules.modifiers import Modifier

class Faction(ABC):
    def __init__(self, name: str, supply: dict[Piece, int], color: Color, handsize: int):
        self.name: str = name
        self.abbr: str = ''.join([w[0] for w in name.split()])
        self.supply: dict[Piece, int] = supply
        self.color: Color = color
        self.handsize: int = handsize
        self.hand: list[Card] = []
        self.revealed: list[Card] = []
        self.items: list[Item] = []
        self.effects: set[Card] = set()  # Cannot have duplicate crafted improvements
        self.modifiers: dict[Modifier, int] = dict()
        self.vp: int = 0
        self.game: Game | None = None
    
    def __str__(self):
        return self.color.color(self.name)

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


class Environment(Faction):
    from random import shuffle
    def __init__(self, name: str):
        super().__init__(
            name=name,
            supply={},
            color=Color.NONE,
            handsize=0
        )
    
    def setup(self, game: Game, homelands: list[Clearing] = list()):
        pass
    
    def birdsong(self):
        pass
    
    def daylight(self):
        pass
    
    def evening(self):
        pass


VOID = Environment('No one')