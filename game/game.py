from game.turn_manager import TurnManager
from board.board import Board
from factions.faction import Faction
from components.pieces import Piece
from components.items import Item
from components.deck import Deck


class GameOver(Exception):
    """Raised when the game is finished."""


class Game:
    def __init__(self, board: Board, deck: Deck, items: dict[Item, int]):
        self.board = board
        self.deck = deck
        self.board.environment.items = items # Item supply
        self.factions: list[Faction] = []
        self.turn_manager: TurnManager = TurnManager()
    
    def setup(self, faction: Faction):
        empty_supply: dict[Piece, int] = {key: 0 for key in faction.supply.keys()}
        for clearing in self.board.clearings:
            clearing.pieces[faction].update(empty_supply)
        self.factions.append(faction)
        faction.setup(self)
        
    def play(self):
        faction: Faction = self.factions[self.turn_manager.next()]
        faction.birdsong()
        faction.daylight()
        faction.evening()
        self.turn_manager.turn_number += 1
    
    def __getitem__(self, key):
        return self.board[key]