from dataclasses import dataclass
from board.clearing import Clearing

@dataclass
class Path:
    origin: Clearing
    destination: Clearing
    closed: bool = False
    river: bool = False