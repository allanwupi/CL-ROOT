from board.clearing import Clearing
from factions.faction import NullFaction

class Board():
    def __init__(self, clearings: list[Clearing], ascii: str):
        self.clearings: list[Clearing] = clearings
        self.size: int = len(clearings)
        self.ascii: str = ascii
        self.environment: NullFaction = NullFaction()
        
    def slots(self):
        """Returns a dict with the building strings of clearing slots"""
    
    def __getitem__(self, key):
        return self.clearings[key]