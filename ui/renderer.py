from game.game import Game
from components.pieces import Piece
from components.items import Item
from board.board import Board
from board.clearing import Clearing
from factions.faction import Faction
from styles import *


class Renderer:
    PADDING: str = ' '*2
    TERMINAL_WIDTH: int = 80
    LEFT_DECORATOR: str = '-'*5 + '='*5 + '{'
    RIGHT_DECORATOR: str = '}' + '='*5 + '-'*5
    
    @staticmethod
    def render_supply(supply: list[Piece]) -> str:
        return ""
    
    @staticmethod
    def render_board(board: Board) -> str:
        ascii: str = board.ascii
        colored_ascii: str = (
            ascii.replace('F', Color.FOX.value)
            .replace('M', Color.MOUSE.value)
            .replace('R', Color.RABBIT.value)
            .replace('N', Style.RESET.value)
        )
            
        return ""
    
    @staticmethod
    def render_game(game: Game) -> str:
        return ""
    
    @staticmethod
    def render_clearing(clearing: Clearing) -> str:
        return ""
    
    @staticmethod
    def render_faction(faction: Faction) -> str:
        return ""
    