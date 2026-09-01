from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from board.clearing import Clearing
from board.suit import Suit
from components.card import Card
from components.pieces import Piece
from factions.faction import Faction

if TYPE_CHECKING:
    from game.game import Game


@dataclass(kw_only=True)
class Action(ABC):
    game: Game
    owner: Faction
    clearing: int
    piece: Piece
    numpieces: int
    _clearing: Clearing = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(
            self, '_clearing',
            self.game[self.clearing]
        )
    
    @abstractmethod
    def execute(self, game: Game, suppress: bool = False) -> None:
        pass


@dataclass(kw_only=True)
class Place(Action):
    owner: Faction
    clearing: int
    piece: Piece
    numpieces: int
    at_piece: Piece | None
    suit: Suit = Suit.WILD
    ignore_rule: bool = True
    forced: bool = False
    
    def execute(self, game: Game, suppress: bool = False) -> None:
        from rules.rule_engine import RULE
        from ui.renderer import Renderer

        RULE.illegalplace(self)
        piece_owner: Faction = self.piece.owner
        piece_owner.supply[self.piece] -= self.numpieces
        self._clearing[piece_owner][self.piece] += self.numpieces
        if not suppress: print(Renderer.render_action(self))


@dataclass(kw_only=True)
class Remove(Action):
    owner: Faction # Removing your own faction pieces doesn't score VP (exception: Keepers in Iron)
    clearing: int
    piece: Piece
    numpieces: int
    forced: bool = False
    
    def execute(self, game: Game, suppress: bool = False) -> None:
        from rules.rule_engine import RULE
        from ui.renderer import Renderer

        RULE.illegalremove(self)
        piece_owner: Faction = self.piece.owner
        self._clearing[piece_owner][self.piece] -= self.numpieces
        piece_owner.supply[self.piece] += self.numpieces
        vp: int = (
            self.piece.points * self.numpieces
            if self.owner != piece_owner
            else 0
        )
        if not suppress:
            print(Renderer.render_action(self),end='')
            if vp:
                print(f", scoring {vp:d} VP.")
                game.score_vp(self.owner, vp)
            else:
                print()


@dataclass(kw_only=True)
class Move(Action):
    owner: Faction
    clearing: int # The clearing of the move is the starting point
    piece: Piece
    numpieces: int
    destination: int
    suit: Suit = Suit.WILD
    ignore_rule: bool = False
    forced: bool = False
    _destination: Clearing = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(
            self, '_destination',
            self.game[self.destination]
        )

    # A move is a compound action
    # Pieces are (1) removed from clearing; (2) placed in destination
    def execute(self, game: Game, suppress: bool = False) -> None:
        from rules.rule_engine import RULE
        from ui.renderer import Renderer

        RULE.illegalmove(self)
        self._clearing[self.owner][self.piece] -= self.numpieces
        self._destination[self.owner][self.piece] += self.numpieces
        if not suppress: print(Renderer.render_action(self))


@dataclass(kw_only=True)
class Build(Place):
    owner: Faction
    piece: Piece
    numpieces: int = 1
    clearing: int
    suit: Suit = Suit.WILD
    ignore_rule: bool = True
    forced: bool = False
    
    # Build action is a specific Place action requiring rule and a free building slot
    def execute(self, game: Game, suppress: bool = False) -> None:
        from rules.rule_engine import RULE
        from ui.renderer import Renderer

        RULE.illegalplace(self)
        # TODO
        pass
        if not suppress: print(Renderer.render_action(self))


@dataclass(kw_only=True)
class Recruit(Place):
    owner: Faction
    clearing: int
    piece: Piece
    numpieces: int
    at_piece: Piece | None
    suit: Suit = Suit.WILD
    ignore_rule: bool = True
    forced: bool = False
    
    # Recruit action is a Place action at a specified recruiting piece
    def execute(self, game: Game, suppress: bool = False) -> None:
        from rules.rule_engine import RULE
        from ui.renderer import Renderer

        RULE.illegalrecruit(self)
        # TODO
        pass
        if not suppress: print(Renderer.render_action(self))


@dataclass(kw_only=True)
class Battle(Action):
    owner: Faction # Owner is the attacker (initiator of battle)
    clearing: int
    piece: Piece # Only matters if this is the Warlord (not yet implemented)
    defender: Faction
    numpieces: int = field(init=False)
    suit: Suit = Suit.WILD
    forced: bool = False
    
    def __post_init__(self):
        object.__setattr__(
            self, 'numpieces',
            self._clearing[self.piece.owner][self.piece]
        )
    
    # A battle is a complex action which involves removing pieces
    def execute(self, game: Game, suppress: bool = False) -> None:
        from rules.rule_engine import RULE
        from ui.renderer import Renderer

        RULE.illegalbattle(self)        
        # TODO
        pass
        if not suppress: print(Renderer.render_action(self))


@dataclass(kw_only=True)
class Craft(Action):
    initiator: Faction
    card: Card
    crafting_pieces: list[Piece]
    crafting_clearings: list[Clearing]
    forced: bool = False
    
    def execute(self, game: Game, suppress: bool = False) -> None:
        from rules.rule_engine import RULE
        from ui.renderer import Renderer
        
        RULE.illegalcraft(self)
        # TODO
        pass
        if not suppress: print(Renderer.render_action(self))