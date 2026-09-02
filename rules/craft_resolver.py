from __future__ import annotations

from board.suit import Suit
from components.pieces import Piece
from components.card import Card

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game
    from game.action import Craft

class CraftResolver:
    def __init__(self, game: Game, craft: Craft):
        self.game: Game = game
        self.craft: Craft = craft
    
    def resolve(self) -> bool:
        # TODO
        return True