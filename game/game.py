from game.turn_manager import TurnManager
from rules.rule_engine import RULE
from board.board import Board
from board.clearing import Clearing
from factions.faction import Faction, TurnPhase
from components.pieces import Piece
from components.items import Item
from components.data import BAG, BOOT, CROSSBOW, HAMMER, SWORD, TEA, COINS
from components.deck import Deck


class GameOver(Exception):
    """Raised when the game is finished."""


class Game:
    ITEM_SUPPLY: dict[Item, int] = {
        BAG: 2,
        BOOT: 2,
        CROSSBOW: 1,
        HAMMER: 1,
        SWORD: 2,
        TEA: 2,
        COINS: 2
    }

    def __init__(self, board: Board, deck: Deck):
        self.board = board
        self.deck = deck
        self.board.environment.items = self.ITEM_SUPPLY
        self.factions: list[Faction] = []
        self.turn_manager: TurnManager = TurnManager()
        
    def __len__(self) -> int:
        return len(self.board)
    
    @property
    def items(self) -> dict[Item, int]:
        return self.board.environment.items
    
    def setup(self, faction: Faction) -> None:
        empty_supply: dict[Piece, int] = {key: 0 for key in faction.supply.keys()}
        for clearing in self.board.clearings:
            clearing.pieces[faction] = {}
            clearing.pieces[faction].update(empty_supply)
        self.factions.append(faction)
        faction.setup(self)
        self.turn_manager.player_count += 1
        
    def increment_score(self, faction: Faction, numpoints: int) -> None:
        if faction not in self.factions:
            print(f"{str(faction)} is not a player.")
            return
        if abs(numpoints > 0):
            print(f"{str(faction)} {'scores' if numpoints > 0 else 'loses'} {numpoints:d} VP.")
        faction.vp += numpoints
        if faction.vp >= 30:
            raise GameOver(f"{str(faction)} victory!")
        
    def play(self) -> None:
        faction: Faction = self.factions[self.turn_manager.next()]
        self.turn_manager.current_phase = TurnPhase.BIRDSONG
        faction.birdsong()
        self.turn_manager.current_phase = TurnPhase.DAYLIGHT
        faction.daylight()
        self.turn_manager.current_phase = TurnPhase.EVENING
        faction.evening()
        self.turn_manager.turn_number += 1
    
    def __getitem__(self, key: int) -> Clearing:
        return self.board.clearings[key]