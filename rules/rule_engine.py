from game.action import *

class RulesBreach(Exception):
    """Raised whenever a game rule is broken (e.g. rule, movement)"""

class RuleEngine:
    @staticmethod
    def illegalmove(move: Move) -> None:
        return
        raise RulesBreach("Illegal move")

    @staticmethod
    def illegalbattle(battle: Battle) -> None:
        return
        raise RulesBreach("Illegal battle")
    
    @staticmethod
    def illegalbuild(build: Build) -> None:
        return
        raise RulesBreach("Illegal build")