from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from board.clearing import Clearing
from board.suit import Suit
from components.card import Card
from components.pieces import Piece, PieceType
from factions.faction import Faction, NullFaction

if TYPE_CHECKING:
    from game.game import Game


@dataclass(kw_only=True)
class Action(ABC):
    game: Game
    owner: Faction
    clearing: int
    piece: Piece
    numpieces: int
    suit: Suit = Suit.WILD
    _clearing: Clearing = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(
            self, '_clearing',
            self.game[self.clearing]
        )
    
    @abstractmethod
    def execute(self, suppress: bool = False) -> None:
        pass


@dataclass(kw_only=True)
class Place(Action):
    owner: Faction
    clearing: int
    piece: Piece
    numpieces: int
    at_piece: Piece | None
    suit: Suit = Suit.WILD
    ignores_rule: bool = True
    forced: bool = False
    
    def execute(self, suppress: bool = False) -> None:
        from rules.rule_engine import RuleEngine
        from ui.renderer import Renderer

        RuleEngine.illegalplace(self)
        # Take from faction supply, place onto board
        piece_owner: Faction = self.piece.owner
        piece_owner.supply[self.piece] -= self.numpieces
        self._clearing[piece_owner][self.piece] += self.numpieces
        if not suppress: print(Renderer.render_action(self),end='')


@dataclass(kw_only=True)
class Remove(Action):
    owner: Faction # Removing your own faction pieces doesn't score VP (exception: Keepers in Iron)
    clearing: int
    piece: Piece
    numpieces: int
    suit: Suit = Suit.WILD
    forced: bool = False
    
    def execute(self, suppress: bool = False) -> None:
        from rules.rule_engine import RuleEngine
        from ui.renderer import Renderer

        RuleEngine.illegalremove(self)
        # Take from board, return to faction supply. Score VP if remover is not owner of piece
        piece_owner: Faction = self.piece.owner
        self._clearing[piece_owner][self.piece] -= self.numpieces
        piece_owner.supply[self.piece] += self.numpieces
        if self.piece.piecetype == PieceType.BUILDING:
            self._clearing.destroy(self.piece)
        vp: int = (
            self.piece.points * self.numpieces
            if self.owner != piece_owner
            else 0
        )
        if not suppress: print(Renderer.render_action(self),end='')
        if vp:
            self.game.score_vp(self.owner, vp, suppress=True)
            print(f', scoring {vp:d} VP.')
        else:
            print('.')


@dataclass(kw_only=True)
class Move(Action):
    owner: Faction
    clearing: int # The clearing of the move is the starting point
    piece: Piece
    numpieces: int
    destination: int
    suit: Suit = Suit.WILD
    ignores_rule: bool = False
    forced: bool = False
    _destination: Clearing = field(init=False)
    _clearing: Clearing = field(init=False)
    
    def __post_init__(self):
        object.__setattr__(
            self, '_clearing',
            self.game[self.clearing]
        )
        object.__setattr__(
            self, '_destination',
            self.game[self.destination]
        )

    # A move is a compound action: pieces are (1) removed from clearing, (2) placed in destination
    def execute(self, suppress: bool = False) -> None:
        from rules.rule_engine import RuleEngine
        from ui.renderer import Renderer

        RuleEngine.illegalmove(self)
        self._clearing[self.owner][self.piece] -= self.numpieces
        self._destination[self.owner][self.piece] += self.numpieces
        if not suppress: print(Renderer.render_action(self),end='.\n')


@dataclass(kw_only=True)
class Build(Place):
    owner: Faction
    piece: Piece
    numpieces: int = 1
    clearing: int
    suit: Suit = Suit.WILD
    ignores_rule: bool = False
    forced: bool = False
    
    # Build action is a specialised Place action requiring rule and a free building slot
    def execute(self, suppress: bool = False) -> None:
        from rules.rule_engine import RuleEngine
        from ui.renderer import Renderer

        RuleEngine.illegalplace(self)
        # Take from faction supply, place onto board
        piece_owner: Faction = self.piece.owner
        piece_owner.supply[self.piece] -= self.numpieces
        self._clearing[piece_owner][self.piece] += self.numpieces
        self._clearing.build(self.piece)
        # Note that building does not score by default, this responsibility lies with the faction
        if not suppress: print(Renderer.render_action(self),end='')


@dataclass(kw_only=True)
class Recruit(Place):
    owner: Faction
    clearing: int
    piece: Piece
    numpieces: int
    at_piece: Piece | None
    suit: Suit = Suit.WILD
    ignores_rule: bool = True
    forced: bool = False
    
    # Recruit action is a Place action at a specified recruiting piece
    def execute(self, suppress: bool = False) -> None:
        from rules.rule_engine import RuleEngine
        from ui.renderer import Renderer

        RuleEngine.illegalrecruit(self)
        # Same as Place
        piece_owner: Faction = self.piece.owner
        piece_owner.supply[self.piece] -= self.numpieces
        self._clearing[piece_owner][self.piece] += self.numpieces
        if not suppress: print(Renderer.render_action(self))


@dataclass(kw_only=True)
class Battle(Action):
    game: Game
    owner: Faction # Owner is the attacker (initiator of battle)
    clearing: int
    piece: Piece # Only matters if this is the Warlord (not yet implemented)
    defender: Faction
    suit: Suit = Suit.WILD
    forced: bool = False
    numpieces: int = field(init=False)
    rolls: tuple[int, int] = field(init=False)
    _clearing: Clearing = field(init=False)
    
    def __post_init__(self):
        from random import randint
        object.__setattr__(
            self, '_clearing',
            self.game[self.clearing]
        )
        object.__setattr__(
            self, 'numpieces',
            self._clearing[self.piece.owner][self.piece]
        )
        object.__setattr__(
            self, 'rolls',
            (randint(0, 3), randint(0, 3))
        )
    
    # A battle is a complex action which involves removing pieces
    def execute(self, suppress: bool = False) -> None:
        from rules.rule_engine import RuleEngine
        from ui.renderer import Renderer
        from rules.battle_resolver import BattleResolver

        RuleEngine.illegalbattle(self)
        if not suppress: print(Renderer.render_action(self))
        # Responsibility of dealing battle damage is delegated to BattleResolver 
        BattleResolver(game=self.game, battle=self).resolve()        


@dataclass(kw_only=True)
class Craft(Action):
    owner: Faction
    supplier: NullFaction
    card: Card
    card_pile: list[Card]
    piece: Piece # Not used
    numpieces: int # Not used
    crafting_pieces: list[Piece]
    crafting_clearings: list[Clearing]
    suit: Suit = Suit.WILD
    override: int = -1
    forced: bool = False
    ignores_cost: bool = False
    
    def execute(self, suppress: bool = False) -> None:
        from rules.rule_engine import RuleEngine
        from ui.renderer import Renderer
        
        RuleEngine.illegalcraft(self)
        if not self.ignores_cost:
            from rules.rule_engine import RuleBreach
            from rules.craft_resolver import CraftResolver
            if not CraftResolver(game=self.game, craft=self).resolve():
                raise RuleBreach("Failed to select crafting pieces.")
        if not suppress: print(Renderer.render_action(self),end='')
        vp: int = 0
        if self.card.item is not None:
            vp = (
                self.override
                if self.override >= 0
                else self.card.item.points
            )
            self.owner.items[self.card.item] = self.owner.items.get(self.card.item, 0) + 1
            self.supplier.items[self.card.item] -= 1
        if self.card.persistent:
            self.owner.effects.add(self.card)
        if vp:
            self.game.score_vp(self.owner, vp, suppress=True)
            print(f', scoring {vp:d} VP.')
        else:
            print('.')
        self.owner.discard(self.card_pile, self.card)