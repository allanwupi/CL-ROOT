from abc import ABC, abstractmethod
from dataclasses import dataclass
from game.game import Game
from rules.rule_engine import RuleEngine
from board.clearing import Clearing
from factions.faction import Faction
from components.pieces import Piece
from ui.renderer import Renderer

@dataclass
class Action(ABC):
    @abstractmethod
    def execute(self, game: Game, suppress: bool = False):
        pass


@dataclass
class Battle(Action):
    attacker: Faction
    clearing: Clearing
    defender: Faction
    
    def execute(self, game: Game, suppress: bool = False):
        RuleEngine.illegalbattle(self)
        print(f"{str(self.attacker)} battles {str(self.defender)} in {str(self.clearing)}",end='')
        

@dataclass
class Move(Action):
    piece: Piece
    origin: Clearing
    destination: Clearing
    numpieces: int

    def execute(self, game: Game, suppress: bool = False):
        RuleEngine.illegalmove(self)
        owner: Faction = self.piece.owner
        game[self.origin].presence[owner][str(self.piece)] -= self.numpieces
        game[self.destination].presence[owner][str(self.piece)] += self.numpieces
        if suppress:
            return
        print(
              f"{owner.color} moved {self.numpieces:d}x {str(self.piece)}"
            f"from {str(self.origin)} to {str(self.destination)}",end=''
        )


@dataclass
class Build(Action):
    piece: Piece
    clearing: Clearing
    require_rule: bool = True
    
    def execute(self, game: Game, suppress: bool = False):
        RuleEngine.illegalbuild(self)
        owner: Faction = self.piece.owner
        print(f"{str(owner)} built {str(self.piece)} in {str(self.clearing)}",end='')