from factions.faction import *
from game.action import Action, Move, Build, Battle, Recruit
from components.pieces import PieceType
from board.suit import Suit

class MechanicalMarquise(Faction):
    def __init__(
        self,
        name: str,
        color: Color = Color.ORANGE,
    ):
        supply: dict[Piece, int] = {
            Piece(self, 'Warrior', PieceType.WARRIOR, 0, Suit.WILD, movable=True, crafting=False): 25,
            Piece(self, 'Keep', PieceType.TOKEN, 0, Suit.WILD, movable=False, crafting=False): 1,
            # Piece(self, 'Wood', PieceType.TOKEN, 8, Suit.WILD, movable=False, crafting=False): 8,
            Piece(self, 'Sawmill', PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=False): 6,
            Piece(self, 'Workshop', PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=True): 6,
            Piece(self, 'Recruiter', PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=False): 6
        }
        super().__init__(name, supply, color, handsize=0)
    
    def __repr__(self):
        return f"MechanicalMarquise(name={self.name!r}, supply={self.supply}, color={self.color.name})"
    
    def craft(self, card: Card) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised")
        if card.item is not None:
            self.game.score_vp(self, 1)
            self.items[card.item] = self.items.get(card.item, 0) + 1
            self.game.items[card.item] -= 1
        if card.persistent:
            self.effects.add(card)
        self.game.deck.discard(self.hand, card)

    def setup(self, game: Game, homelands: list[Clearing] = list()):
        """Set up faction pieces following advanced setup rules."""
        pass
    
    def birdsong(self):
        """Execute the birdsong phase."""
        pass
    
    def daylight(self):
        """Execute the daylight phase."""
        pass
    
    def evening(self):
        """Execute the evening phase."""
        pass