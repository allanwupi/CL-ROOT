from factions.faction import *
from game.action import Move, Build, Place, Battle, Recruit, Craft
from components.pieces import PieceType
from board.suit import Suit
from board.location import Location

class MechanicalMarquise(Faction):    
    def __init__(
        self,
        name: str,
        color: Color = Color.ORANGE,
    ):
        self._WARRIOR = Piece(self, "Warrior", PieceType.WARRIOR, 0, Suit.WILD, movable=True, crafting=False)
        self._KEEP = Piece(self, "Keep", PieceType.TOKEN, 0, Suit.WILD, movable=False, crafting=False)
        self._WOOD = Piece(self, "Wood", PieceType.TOKEN, 8, Suit.WILD, movable=False, crafting=False)
        self._SAWMILL = Piece(self, "Sawmill", PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=False)
        self._WORKSHOP = Piece(self, "Workshop", PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=True)
        self._RECRUITER = Piece(self, "Recruiter", PieceType.BUILDING, 0, Suit.WILD, movable=False, crafting=False)
        supply: dict[Piece, int] = {
            # self._WOOD: 8,
            self._WARRIOR: 25,
            self._KEEP: 1,
            self._SAWMILL: 6,
            self._WORKSHOP: 6,
            self._RECRUITER: 6
        }
        super().__init__(name, supply, color, handsize=0)
    
    def __repr__(self):
        return f"MechanicalMarquise(name={self.name!r}, supply={self.supply}, color={self.color.name})"
    
    def battle(self, u: int, defender: Faction) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        Battle(
            game=self.game, owner=self, clearing=u, piece=self._WARRIOR, defender=defender
        ).execute()
    
    def move(self, u: int, v: int, numpieces: int) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        Move(
            game=self.game, owner=self, clearing=u, destination=v, 
            piece=self._WARRIOR, numpieces=numpieces
        ).execute()
    
    def recruit(self, u: int, numpieces: int = 1) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        Recruit(
            game=self.game, owner=self, clearing=u, piece=self._WARRIOR, numpieces=numpieces,
            at_piece=None
        ).execute()
    
    def place(self, u: int, token: Piece, numpieces: int = 1) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        Place(
            game=self.game, owner=self, clearing=u, piece=token, numpieces=numpieces,
            at_piece=None
        ).execute()
    
    def build(self, u: int, building: Piece, noscore: bool = False) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        Build(
            game=self.game, owner=self, clearing=u, piece=building, at_piece=None
        ).execute()
        # Score points according to the number of buildings left on the track
        if noscore:
            return
        vp: int = 7-self.supply[building]
        self.game.score_vp(self, vp)
    
    def craft(self, card: Card) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        Craft(
            game=self.game, owner=self, clearing=0, piece=self._WORKSHOP, numpieces=0,
            supplier=self.game.board.environment, card=card, card_pile=self.revealed,
            crafting_pieces=[], crafting_clearings=[], override=1
        ).execute()

    def setup(self, game: Game) -> None:
        self.game = game
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        from rules.rule_engine import RuleBreach
        from random import shuffle, sample
        """Set up faction pieces following advanced setup rules."""
        for u in range(1, len(self.game)):
            self.recruit(u)
        corner_choices: list[int] = self.game.board.filter(location=Location.CORNER, not_picked=True, return_indices=True)
        if not corner_choices:
            raise RuleBreach(f"No available corner homelands remain for setup.")
        shuffle(corner_choices)
        u: int = 0
        while len(corner_choices) > 0:
            try:
                u = corner_choices.pop()
                print(u)
                adjacent_choices = [v for v in self.game.board[u].adjlist if not self.game.board[v].homeland]
                if len(adjacent_choices) < 2:
                    raise RuleBreach(f"Corner {u} has too few adjacent homelands available.")
                homeland = [u] + sample(adjacent_choices, k=2)
                buildings: list[Piece] = [self._SAWMILL, self._WORKSHOP, self._RECRUITER]
                shuffle(buildings)
                self.place(u=homeland[0], token=self._KEEP)
                for h in homeland:
                    self.recruit(h)
                    self.build(h, buildings.pop(), noscore=True)
                    self.game.board[h].homeland = True
                print(f"{self.name} set up in homeland clearings {homeland}.")
                return
            except RuleBreach as e:
                print(e)
                print(f"{self.name} setup failed for corner {u:d}. Trying again...")
        raise RuntimeError(f"Failed to find a valid setup for {self.name}.")
    
    def birdsong(self):
        """Execute the birdsong phase."""
        pass
    
    def daylight(self):
        """Execute the daylight phase."""
        pass
    
    def evening(self):
        """Execute the evening phase."""
        pass