from game.action import *
from typing import Callable
from rules.craft_resolver import CraftResolver
    

def filter_moves(self, moves: list[Move], predicate: Callable[[Action], bool]) -> list[Move]:
    return [move for move in moves if predicate(move)]
    
def filter_clearings(clearings: list[Clearing], predicate: Callable[[Clearing], bool]) -> list[Clearing]:
    return [clearing for clearing in clearings if predicate(clearing)]
    
    
class RuleBreach(Exception):
    """Raised whenever a game rule is broken (e.g. rule, movement)"""


class RuleEngine:
    _SOURCES: list[str] = [
        "The Law of Root (updated Oct 8, 2025)",
        "Better Bot Project (playtest version 24 Aug, 2026)"
    ]
    FAIL: Callable[[Action], bool] = lambda x: False
    SUCCESS: Callable[[Action], bool] = lambda x: True
    OWNS_PIECE = lambda x: x.owner == x.piece.owner
    NON_ZERO_PIECES = lambda x: x.numpieces > 0
    SUFFICIENT_SUPPLY = lambda x: x.piece.owner[x.piece] >= x.numpieces
    SUFFICIENT_PIECES = lambda x: x._clearing[x.piece.owner][x.piece] >= x.numpieces
    RULES_CLEARING = lambda x: x.owner == x._clearing.ruler
    ENEMY_HAS_PIECES = lambda x: isinstance(x, Battle) and x._clearing.faction_presence(x.defender).numpieces > 0
    ITEM_IN_STOCK = lambda x: isinstance(x, Craft) and (x.card.item is None or x.card.item.in_stock)
    RULES_DESTINATION = lambda x: isinstance(x, Move) and x.owner == x._destination.ruler
    MATCHING_CLEARING = lambda x: isinstance(x, Move | Battle | Remove | Place) and x._clearing.suit in x.suit
    ADJACENT_CLEARINGS = lambda x: isinstance(x, Move) and x.destination in x._clearing.adjlist
    CLEARING_HAS_PIECE = lambda x: isinstance(x, Place) and x._clearing.has_piece(x.at_piece)
    NO_DUPLICATE_CARDS = lambda x: isinstance(x, Craft) and x.card not in x.owner.effects
    BUILDING_SLOT_FREE = lambda x: isinstance(x, Build) and x._clearing.free
    ADDED_PREDICATES: dict[str, Callable[[Action], bool]] = {}

    def __init__(self, name: str, predicates: dict[str, Callable[[Action], bool]]):
        self.name = name
        self.sources = self._SOURCES
        self.ADDED_PREDICATES.update(predicates)
    
    @classmethod
    def check(cls, act: Action, predicate: str | Callable[[Action], bool]) -> bool:
        if isinstance(predicate, str):
            _predicate: Callable[[Action], bool] | None = cls.ADDED_PREDICATES.get(predicate)
            if _predicate is None:
                _predicate = getattr(cls, predicate, None)
            if _predicate is None:
                return False
            return _predicate(act)
        return predicate(act)
    
    @classmethod
    def illegalplace(cls, place: Place) -> None:
        if not cls.check(place, cls.NON_ZERO_PIECES):
            raise RuleBreach("Must place at least one piece.")
        if not cls.check(place, cls.CLEARING_HAS_PIECE):
            raise RuleBreach("Must place at a clearing containing a piece.")
        if not place.forced and not cls.check(place, cls.OWNS_PIECE):   
            raise RuleBreach("Can only place another faction's piece if the action is Forced.")
        if not place.ignores_rule and not cls.check(place, cls.RULES_CLEARING):
            raise RuleBreach("Must rule the clearing to place.")
        if not cls.check(place, cls.MATCHING_CLEARING):
            raise RuleBreach("Can only place that piece in a matching clearing.")
        if not cls.check(place, cls.SUFFICIENT_SUPPLY):   
            raise RuleBreach("Supply does not have enough pieces. Pieces are limited by the contents of the game.")

    @classmethod
    def illegalremove(cls, remove: Remove) -> None:
        if not cls.check(remove, cls.NON_ZERO_PIECES):
            raise RuleBreach("Must remove at least one piece.")
        if not cls.check(remove, cls.MATCHING_CLEARING):
            raise RuleBreach("Must remove pieces from a matching clearing.")
        if not cls.check(remove, cls.SUFFICIENT_PIECES):   
            raise RuleBreach("Clearing does not have enough pieces. Pieces are limited by the contents of the game.")
    
    @classmethod
    def illegalmove(cls, move: Move) -> None:
        if not move.forced and not cls.check(move, cls.OWNS_PIECE):   
            raise RuleBreach("Can only move another faction's piece if the action is Forced.")
        if not cls.check(move, cls.MATCHING_CLEARING):
            raise RuleBreach("Can only take a move from a matching clearing.")
        if not cls.check(move, cls.NON_ZERO_PIECES):
            raise RuleBreach("Must move at least one piece.")
        if not move.piece.movable:
            raise RuleBreach("That piece cannot be moved.")
        if not cls.check(move, cls.SUFFICIENT_PIECES):   
            raise RuleBreach("Supply does not have enough pieces. Pieces are limited by the contents of the game.")
        if (not move.ignores_rule
            and not cls.check(move, cls.RULES_CLEARING)
            and not cls.check(move, cls.RULES_DESTINATION)
        ):
            raise RuleBreach("To take a move, you must rule the origin clearing, destination clearing, or both.")
        if not cls.check(move, cls.ADJACENT_CLEARINGS):
            raise RuleBreach("Clearings are not connected. A clearing is adjacent to all other clearings linked to it by a path.")

    @classmethod
    def illegalbattle(cls, battle: Battle) -> None:
        if not cls.check(battle, cls.OWNS_PIECE):   
            raise RuleBreach("Can only battle with another faction's piece if the action is Forced.")
        if not cls.check(battle, cls.NON_ZERO_PIECES):
            raise RuleBreach("You must have at least one warrior/pawn there to battle.")
        if not cls.check(battle, cls.SUFFICIENT_PIECES):   
            raise RuleBreach("Clearing does not have enough pieces. Pieces are limited by the contents of the game.")
        if not cls.check(battle, cls.ENEMY_HAS_PIECES):   
            raise RuleBreach("There are no enemy pieces in that clearing.")
        if not battle.piece.can_battle:
            raise RuleBreach("Only warriors/pawns can initiate battle.")
        if not cls.check(battle, cls.MATCHING_CLEARING):
            raise RuleBreach("Battle must take place in a matching clearing.")
    
    @classmethod
    def illegalrecruit(cls, recruit: Recruit) -> None:
        if not cls.check(recruit, cls.OWNS_PIECE):
            raise RuleBreach("Cannot recruit another faction's pieces.")
        if not cls.check(recruit, cls.CLEARING_HAS_PIECE):
            raise RuleBreach("Clearing does not have a recruiting piece.")
        if not cls.check(recruit, cls.NON_ZERO_PIECES):
            raise RuleBreach("Must recruit at least one piece.")
        if not cls.check(recruit, cls.MATCHING_CLEARING):
            raise RuleBreach("Can only recruit that piece in a matching clearing.")
        if not cls.check(recruit, cls.SUFFICIENT_SUPPLY):   
            raise RuleBreach("Supply does not have enough pieces. Pieces are limited by the contents of the game.")
    
    @classmethod
    def illegalbuild(cls, build: Build) -> None:
        if not build.ignores_rule and not cls.check(build, cls.RULES_CLEARING):
            raise RuleBreach("Must rule the clearing to build.")
        if not cls.check(build, cls.OWNS_PIECE):   
            raise RuleBreach("Cannot build another faction's pieces.")
        if not cls.check(build, cls.BUILDING_SLOT_FREE):
            raise RuleBreach("Clearing does not have a free building slot.")
        if not cls.check(build, cls.NON_ZERO_PIECES):
            raise RuleBreach("Must build at least one piece.")
        if not cls.check(build, cls.MATCHING_CLEARING):
            raise RuleBreach("Can only build in a matching clearing.")
        if not cls.check(build, cls.SUFFICIENT_SUPPLY):   
            raise RuleBreach("Supply does not have enough buildings. Pieces are limited by the contents of the game.")
    
    @classmethod
    def illegalcraft(cls, craft: Craft) -> None:
        if not cls.check(craft, cls.ITEM_IN_STOCK):
            raise RuleBreach("That card cannot be crafted. The item is not in the item supply.")
        if not cls.check(craft, cls.NO_DUPLICATE_CARDS):
            raise RuleBreach("No duplicates. You cannot craft a persistent effect if you have an identical one in your play area.")
        #TODO