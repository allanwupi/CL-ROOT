from __future__ import annotations

from game.action import Action, Battle, Recruit, Build, Craft, Move, Place, Remove
from game.turn_manager import TurnManager
from components.items import Item, Ruin
from components.pieces import Piece
from board.board import Board
from board.clearing import Clearing
from board.suit import Suit
from factions.faction import Faction, TurnPhase
from ui.styles import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import Game


# Terminal options
_PADDING: str = ' '*2
_TERMWIDTH: int = 80


class Renderer:    
    # Turn annoucements
    LEFT_DECORATOR: str = '-'*5 + '='*5 + '{'
    RIGHT_DECORATOR: str = '}' + '='*5 + '-'*5

    # Building slots
    FREE_SLOT: str = ' '
    BLOCKED_SLOT: str = f"{Color.RUIN.style('#')}"
    
    @classmethod
    def render_slot(cls, building: Piece | None, suit: Suit) -> str:
        if building is None:
            return (
                f"{suit.color.style('[')}"
                f"{cls.FREE_SLOT}"
                f"{suit.color.style(']')}"
            )
        elif isinstance(building, Ruin):
            return  (
                f"{suit.color.style('[')}"
                f"{cls.BLOCKED_SLOT}"
                f"{suit.color.style(']')}"
            )
        else:
            return f"{building.owner.color.style('['+building.name[0]+']')}"
    
    @classmethod
    def render_turn_phase(cls, game: Game) -> str:
        turn_manager: TurnManager = game.turn_manager
        turn: int = turn_manager.turn_number
        current_player: int = turn_manager.current_player
        phase: TurnPhase = turn_manager.current_phase
        result: str = ""
        if current_player == 0 and phase == TurnPhase.BIRDSONG:
            result += f"{cls.LEFT_DECORATOR}Turn {turn}{cls.RIGHT_DECORATOR}"
            result += f"{'-'*(_TERMWIDTH-len(result))}\n"
        result += f"{Style.BOLD.style(str(phase))}"
        return result
    
    @classmethod
    def render_action(cls, act: Action) -> str:
        if isinstance(act, Recruit):
            return f"{_PADDING}{str(act.owner)} recruits {act.numpieces:d}x {str(act.piece)} in {str(act._clearing)}. "
        if isinstance(act, Move):
            return (
                f"{str(act.owner)} moves {act.numpieces:d}x {str(act.piece)}"
                f" from {str(act._clearing)} to {str(act._destination)}. "
            )
        if isinstance(act, Battle):
            return f"{str(act.owner)} battles {str(act.defender)} in {str(act._clearing)}. Dice rolls: {act.rolls}. "
        if isinstance(act, Build):
            if act.numpieces > 1:
                return f"{str(act.owner)} builds {act.numpieces:d}x {str(act.piece)} in {str(act._clearing)}. "
            return f"{str(act.owner)} builds {str(act.piece)} in {str(act._clearing)}. "
        if isinstance(act, Place):
            return f"{_PADDING}{str(act.owner)} places {act.numpieces:d}x {str(act.piece)} in {str(act._clearing)}. "
        if isinstance(act, Remove):
            return f"{_PADDING}{str(act.owner)} removes {str(act.numpieces)}x {act.piece} in {str(act._clearing)}. "
        if isinstance(act, Craft):
            if act.card.item is not None:
                return f"{str(act.owner)} crafts {str(act.card.item)}. "
            return f"{str(act.owner)} crafts {str(act.card)}. "
        return Color.WARNING.style(f"Action {repr(act)} was not rendered.")

    @classmethod
    def render_item_supply(cls, supply: dict[Item, int], label: bool = False) -> str:
        result: str = "["
        if label: result = f"{_PADDING}Items   : "+result
        for key, count in supply.items():
            result += f'{count}x {str(key)}, '
        if len(supply) > 0:
            result = result[:-2]
        return result+']'
    
    @classmethod
    def render_faction_supply(cls, supply: dict[Piece, int], label: bool = False) -> str:
        result: str = ""
        if label: result = f'{_PADDING:s}Supply  : '+result
        for piece, count in supply.items():
            if count > 0:
                result += f'{count}x {str(piece)}, '
        if len(supply) > 0:
            result = result[:-2]
        return result
    
    @classmethod
    def render_faction_board(cls, faction: Faction) -> str:
        hand: str = f'{_PADDING}Hand    : ['
        for card in set(faction.hand):
            hand += f'{str(card)}, '
        if len(faction.hand) > 0:
            hand = hand[:-2]
        hand += ']'
        items: str = cls.render_item_supply(faction.items, label=True)
        faction_supply: str = cls.render_faction_supply(faction.supply, label=True)
        effects = f'{_PADDING}Crafted : ['
        for crafted_improvement in faction.effects:
            effects += f'{str(crafted_improvement)}, '
        if len(faction.effects) > 0:
            effects = effects[:-2]
        effects += ']'
        header: str = f"{cls.LEFT_DECORATOR}{faction.name} ({faction.vp}/30 VP){cls.RIGHT_DECORATOR}"
        header = faction.color.style(header + '-'*(_TERMWIDTH-len(header)))
        return '\n'.join((header, hand, effects, items, faction_supply))+'\n'

    @staticmethod
    def render_map(board: Board) -> str:
        # Note: hardcoded to work for Autumn board only!
        ascii: str = board.ascii
        colored_ascii: str = (
            ascii.replace('F', Color.FOX.value)
            .replace('M', Color.MOUSE.value)
            .replace('R', Color.RABBIT.value)
            .replace('N', Style.RESET.value)
        )
        slot_dict: dict[str, str] = {
            f"{clearing.name.lower()}_{i+1:d}": Renderer.render_slot(clearing.slots[i], clearing.suit)
            for clearing in board.clearings for i in range(0, len(clearing.slots)) 
        }
        return colored_ascii.format(**slot_dict)
    
    @classmethod
    def render_clearing(cls, game: Game, clearing: int | Clearing) -> str:
        if isinstance(clearing, int):
            _clearing: Clearing = game[clearing]
        else:
            _clearing: Clearing = clearing
        buildings: str = ""
        for slot in _clearing.slots:
            buildings += cls.render_slot(slot, _clearing.suit)
        clearing_ruler: Faction | None = _clearing.ruler
        ruler: Faction = (
            clearing_ruler
            if clearing_ruler is not None
            else game.board.environment
        )
        ruler_presence: int = (
            _clearing.faction_presence(clearing_ruler).rule
            if clearing_ruler is not None
            else 0
        )
        faction_presence: str = ""
        for present in _clearing.presence:
            faction: Faction = present.faction
            if present.numpieces > 0:
                faction_presence += (
                    f"{_PADDING}{faction.color.style(faction.name)} : "
                    f"{cls.render_faction_supply(_clearing.pieces[faction])}\n"
                )
        # faction_presence = faction_presence[:-1]
        result: str = (
            f"{_clearing.suit.color.value}{_clearing.number} {_clearing.name} {buildings}{Style.RESET.value}"
            f" ruled by {ruler.color.style(ruler.name)} (x{ruler_presence:d}) -> {_clearing.adjlist}\n"
            f"{faction_presence}"
        )
        return result[:-1]

    @classmethod
    def render_game(cls, game: Game) -> str:
        result: str = ""
        result += cls.render_item_supply(game.items)+"\n"
        result += cls.render_map(game.board)+"\n"
        result += (f'{Style.DIM.value}Turn {game.turn_manager.turn_number}: '
            f'{len(game.deck.draw_pile)}/{len(game.deck)} cards left in deck.{Style.RESET.value}\n'
        )
        for faction in game.factions:
            result += cls.render_faction_board(faction)
        return result