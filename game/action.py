from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from game.game import Game
from board.suit import Suit
from board.clearing import Clearing
from factions.faction import Faction
from components.pieces import Piece
from components.card import Card
from rules.rule_engine import RULE


@dataclass
class Action(ABC):
    owner: Faction
    clearing: Clearing
    piece: Piece
    numpieces: int
    
    @abstractmethod
    def execute(self, game: Game) -> None:
        pass


@dataclass
class Place(Action):
    owner: Faction
    clearing: Clearing
    piece: Piece
    numpieces: int
    at_piece: Piece | None
    suit: Suit = Suit.WILD
    require_rule: bool = False
    forced: bool = False
    
    def execute(self, game: Game) -> None:
        RULE.illegalplace(self)
        # TODO
        pass
        print(f"{str(self.owner)} built {str(self.piece)} in {str(self.clearing)}",end='')



@dataclass
class Remove(Action):
    owner: Faction # Removing your own faction pieces doesn't score VP (exception: Keepers in Iron)
    clearing: Clearing
    piece: Piece
    numpieces: int
    forced: bool = False
    
    def execute(self, game: Game) -> None:
        RULE.illegalremove(self)
        # TODO
        pass


@dataclass
class Move(Action):
    owner: Faction
    clearing: Clearing # The clearing of the move is the starting point
    piece: Piece
    numpieces: int
    destination: Clearing
    suit: Suit = Suit.WILD
    require_rule: bool = True
    forced: bool = False

    # A move is a compound action
    # Pieces are (1) removed from clearing; (2) placed in destination
    def execute(self, game: Game) -> None:
        RULE.illegalmove(self)
        game[self.clearing].presence[self.owner][str(self.piece)] -= self.numpieces
        game[self.destination].presence[self.owner][str(self.piece)] += self.numpieces


@dataclass
class Build(Place):
    owner: Faction
    piece: Piece
    numpieces: int = 1
    clearing: Clearing
    suit: Suit = Suit.WILD
    require_rule: bool = False
    forced: bool = False
    
    # Build action is a specific Place action requiring rule and a free building slot
    def execute(self, game: Game) -> None:
        RULE.illegalplace(self)
        # TODO
        pass


@dataclass
class Recruit(Place):
    owner: Faction
    clearing: Clearing
    piece: Piece
    numpieces: int
    at_piece: Piece | None
    suit: Suit = Suit.WILD
    require_rule: bool = False
    forced: bool = False
    
    # Recruit action is a Place action at a specified recruiting piece
    def execute(self, game: Game) -> None:
        RULE.illegalrecruit(self)
        # TODO
        pass


@dataclass
class Battle(Action):
    owner: Faction # Owner is the attacker (initiator of battle)
    clearing: Clearing
    piece: Piece # Only matters if this is the Warlord (not yet implemented)
    defender: Faction
    numpieces: int = field(init=False)
    suit: Suit = Suit.WILD
    forced: bool = False
    
    def __post_init__(self):
        object.__setattr__(
            self, 'numpieces',
            self.clearing[self.piece.owner][self.piece]
        )
    
    # A battle is a complex action which involves removing pieces
    def execute(self, game: Game) -> None:
        RULE.illegalbattle(self)        
        # TODO
        pass


@dataclass
class Craft(Action):
    initiator: Faction
    card: Card
    crafting_pieces: list[Piece]
    crafting_clearings: list[Clearing]
    forced: bool = False
    
    def execute(self, game: Game) -> None:
        RULE.illegalcraft(self)
        # TODO
        pass