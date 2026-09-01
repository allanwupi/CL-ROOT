from game.game import Game
from game.action import Action, Battle, Move, Build
from components.pieces import Piece
from components.items import Item, Ruin
from board.board import Board
from board.clearing import Clearing
from factions.faction import Faction
from styles import *


class Renderer:
    PADDING: str = ' '*2
    TERMINAL_WIDTH: int = 80
    LEFT_DECORATOR: str = '-'*5 + '='*5 + '{'
    RIGHT_DECORATOR: str = '}' + '='*5 + '-'*5
    SLOT_DECORATOR: tuple[str, str] = ('[', ']')
    
    @staticmethod
    def render_slot(building: Piece | None, braces: tuple[str, str] = SLOT_DECORATOR) -> str:
        slot: str = ''
        if building is None:
            slot = ' '
        elif isinstance(building, Ruin):
            slot = '#'
        else:
            slot = str(building).upper()[0]
        return braces[0]+slot+braces[1]
    
    @staticmethod
    def render_action(act: Action) -> str:
        if isinstance(act, Battle):
            return f"{str(act.owner)} battles {str(act.defender)} in {str(act.clearing)}"
        if isinstance(act, Move):
            return (
                f"{act.owner.color} moved {act.numpieces:d}x {str(act.piece)}"
                f"from {str(act.clearing)} to {str(act.destination)}"
            )
        if isinstance(act, Build):
            return f"{str(act.owner)} built {str(act.piece)} in {str(act.clearing)}"
        else:
            return Color.WARNING.style(f"Action {repr(act)} cannot be rendered.")

    @staticmethod
    def render_supply(supply: list[Piece]) -> str:
        return ""
    
    @staticmethod
    def render_board(board: Board) -> str:
        # Note: hardcoded to work for Autumn board only!
        ascii: str = board.ascii
        colored_ascii: str = (
            ascii.replace('F', Color.FOX.value)
            .replace('M', Color.MOUSE.value)
            .replace('R', Color.RABBIT.value)
            .replace('N', Style.RESET.value)
        )
        slot_dict: dict[str, str] = {
            f"{repr(clearing)}_{number+1:d}": Renderer.render_slot(clearing.slots[number])
            for number, clearing in enumerate(board.clearings)
        }
        return colored_ascii.format(**slot_dict)
    
    @staticmethod
    def render_game(game: Game) -> str:
        return ""
    
    @staticmethod
    def render_clearing(clearing: Clearing) -> str:
        return ""
    
    @staticmethod
    def render_faction(faction: Faction) -> str:
        return ""
    