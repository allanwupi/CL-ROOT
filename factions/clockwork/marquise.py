from factions.faction import *
from components.pieces import PieceType
from board.suit import Suit

class MechanicalMarquise(Faction):
    def __init__(
        self,
        name: str,
        color: Color = Color.ORANGE,
        handsize: int = 0
    ):
        supply: dict[Piece, int] = {
            Piece(self, 'Warrior', PieceType.WARRIOR, 0, Suit.WILD, movable=True, crafting=False): 25,
            Piece(self, 'Keep', PieceType.TOKEN, 0, Suit.WILD, movable=False, crafting=False): 1,
            Piece(self, 'Wood', PieceType.TOKEN, 8, Suit.WILD, movable=False, crafting=False): 1,
            Piece(self, 'Sawmill', PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=False): 6,
            Piece(self, 'Workshop', PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=True): 6,
            Piece(self, 'Recruiter', PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=False): 6
        }
        super().__init__(name, supply, color, handsize)

    @abstractmethod
    def setup(self, game: Game, homelands: list[Clearing] = list()):
        """Set up faction pieces following advanced setup rules."""
        pass
    
    @abstractmethod
    def birdsong(self):
        """Execute the birdsong phase."""
        pass
    
    @abstractmethod
    def daylight(self):
        """Execute the daylight phase."""
        pass
    
    @abstractmethod
    def evening(self):
        """Execute the evening phase."""
        pass