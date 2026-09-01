from board.clearing import Clearing
from factions.faction import NullFaction
from components.data import _ENVIRONMENT

class Board():
    def __init__(self, clearings: list[Clearing], ascii: str):
        self.clearings: list[Clearing] = clearings
        self.size: int = len(clearings)
        self.ascii: str = ascii
        self.environment: NullFaction = _ENVIRONMENT
        
    def slots(self):
        """Returns a dict with the building strings of clearing slots"""
    
    def __len__(self) -> int:
        return self.size
    
    def __getitem__(self, key: int):
        return self.clearings[key]