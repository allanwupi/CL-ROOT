from game.action import *
from typing import Callable
    

class RulesBreach(Exception):
    """Raised whenever a game rule is broken (e.g. rule, movement)"""


class RuleEngine:
    _SOURCES: list[str] = [
        "The Law of Root (updated Oct 8, 2025)",
        "Better Bot Project (playtest version 24 Aug, 2026)"
    ]

    _BASE_PREDICATES: dict[str, Callable[[Action], bool]] = {
        "PASS": lambda x: True,
        "FAIL": lambda x: False,
        # Check that the owner of the Action is the same as the Piece
        "OWNS_PIECE": lambda x: x.owner == x.piece.owner,
        "SUFFICIENT_PIECES": lambda x: x._clearing[x.piece.owner][x.piece] >= x.numpieces,
        "SUFFICIENT_SUPPLY": lambda x: x.piece.owner[x.piece] >= x.numpieces,
        "IGNORE_RULE": lambda x: isinstance(x, Build | Move) and x.ignore_rule,
        "RULES_CLEARING": lambda x: x.owner == x._clearing.ruler,
        "RULES_DESTINATION": lambda x: isinstance(x, Move) and x.owner == x._destination.ruler,
        "FREE_SLOT": lambda x: isinstance(x, Build) and x._clearing.free
    }

    def __init__(self, name: str, predicates: dict[str, Callable[[Action], bool]]):
        self.name = name
        self.sources = self._SOURCES
        self.predicates = predicates
        self.predicates.update(self._BASE_PREDICATES)
    
    def filter(self, moves: list[Move], predicate: str | Callable[[Move], bool]) -> list[Move]:
        rule: Callable[[Move], bool] = (
            self.predicates[predicate]
            if isinstance(predicate, str)
            else predicate
        )
        return [move for move in moves if rule(move)]
    
    def illegalplace(self, place: Place) -> None:
        return
        raise RUlesBreach("Illegal place")

    def illegalremove(self, remove: Remove) -> None:
        return
        raise RUlesBreach("Illegal remove")
    
    def illegalmove(self, move: Move) -> None:
        return
        raise RulesBreach("Illegal move")

    def illegalbattle(self, battle: Battle) -> None:
        return
        raise RulesBreach("Illegal battle")
    
    def illegalrecruit(self, recruit: Recruit) -> None:
        return
        raise RulesBreach("Illegal recruit")
    
    def illegalbuild(self, build: Build) -> None:
        return
        raise RulesBreach("Illegal build")
    
    def illegalcraft(self, craft: Craft) -> None:
        return
        raise RulesBreach("Illegal craft")


RULE = RuleEngine(name="Law of Root + Better Bots", predicates={})