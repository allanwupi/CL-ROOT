from board.clearing import Clearing

class Board():
    def __init__(self, clearings: list[Clearing], ascii: str):
        self.clearings: list[Clearing] = clearings
        self.size: int = len(clearings)
        self.ascii: str = ascii
    
    def __getitem__(self, key):
        return self.clearings[key]