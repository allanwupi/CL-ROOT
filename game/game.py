from game.turn_manager import TurnManager
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

    def __init__(self, board: Board, deck: Deck, pause_each_phase: bool = False):
        self.board = board
        self.deck = deck
        self.board.environment.items = self.ITEM_SUPPLY
        self.pause_each_phase = pause_each_phase
        self.factions: list[Faction] = []
        self.turn_manager: TurnManager = TurnManager()
        self.vp_history: list[list] = []
    
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
        self.vp_history.append([])
        self.turn_manager.player_count += 1
        
    def score_vp(self, faction: Faction, numpoints: int, suppress: bool = False) -> None:
        if faction not in self.factions:
            print(f"{str(faction)} is not a player.")
            return
        if abs(numpoints > 0) and not suppress:
            from ui.renderer import _PADDING
            # print(f"{_PADDING}{str(faction)} {'scores' if numpoints > 0 else 'loses'} {numpoints:d} VP.")
            print(f"{_PADDING}{'+' if numpoints > 0 else '-'}{numpoints:d} VP")
        faction.vp += numpoints
        if faction.vp >= 30:
            self.vp_history[self.turn_manager.current_player].append(faction.vp)
            raise GameOver(f"{str(faction)} victory!")
        
    def play(self) -> None:
        from ui.renderer import Renderer
        player: int = self.turn_manager.next()
        if player == 0:
            self.turn_manager.turn_number += 1
        faction: Faction = self.factions[player]
        self.turn_manager.current_phase = TurnPhase.BIRDSONG
        print(Renderer.render_turn_phase(self))
        faction.birdsong()
        if self.pause_each_phase: input()
        self.turn_manager.current_phase = TurnPhase.DAYLIGHT
        print(Renderer.render_turn_phase(self))
        faction.daylight()
        if self.pause_each_phase: input()
        self.turn_manager.current_phase = TurnPhase.EVENING
        print(Renderer.render_turn_phase(self))
        faction.evening()
        self.vp_history[player].append(faction.vp)
        print()
    
    def __getitem__(self, key: int) -> Clearing:
        return self.board.clearings[key]
    
    def __len__(self) -> int:
        return self.size
    
    def __getattr__(self, attribute):
        # Fetch missing attributes from the encapsulated board object
        return getattr(self.board, attribute)
    
    def __str__(self) -> str:
        from ui.renderer import Renderer
        return Renderer.render_game(self)