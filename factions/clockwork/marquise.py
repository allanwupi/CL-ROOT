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
        self.order: Card = Card("PLACEHOLDER", Suit.NONE)
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
    
    def __str__(self):
        return f"{self.color.style(self.name)}"
    
    def __getattr__(self, attribute):
        # Fetch missing attributes from the encapsulated board object
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        return getattr(self.game.board, attribute)
    
    def score(self, vp: int) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        self.game.score_vp(self, vp)
        
    def rules(self, u: int) -> bool:
        return self.clearings[u].ruler == self
    
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
    
    def craft(self, card_pile: list[Card], card: Card, override: int = 1) -> None:
        if self.game is None:
            raise AttributeError("Game was not initialised!")
        Craft(
            game=self.game, owner=self, clearing=0, piece=self._WORKSHOP, numpieces=0,
            supplier=self.game.board.environment, card=card, card_pile=card_pile,
            crafting_pieces=[], crafting_clearings=[], override=override
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
        corner_choices: list[int] = self.get_clearings(location=Location.CORNER, not_picked=True, return_indices=True)
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
        self.draw(self.revealed, 1)
        self.order = self.revealed[0]
        print(f"{str(self)} reveals {str(self.order)}.")
        if (self.order.item and self.order.item.in_stock):
            self.craft(self.revealed, self.order, override = 1)
        elif (self.order.persistent and self.order not in self.effects):
            self.craft(self.revealed, self.order)
    
    def daylight(self):
        """Execute the daylight phase."""
        # BATTLE
        print(f"{self.name} initiates a battle in each {'' if self.order.suit == Suit.BIRD else str(self.order.suit)+' '}clearing.")  # Only 1 enemy for now
        for (clearing, enemy) in self.get_battles(self, suit=self.order.suit):
            self.battle(clearing, enemy)
        print(f"{self.name} recruits 4x {self._WARRIOR} among ruled ordered clearings.")
        # RECRUIT
        recruit_clearings: list[int] = []
        if self.order.suit == Suit.BIRD:
            recruit_clearings = sorted(self.get_clearings(ruler=self), key=id, reverse=True)[:2]
        else:
            recruit_clearings = sorted(self.get_clearings(ruler=self, suit=self.order.suit), key=id)
        failed_recruits: int = 0
        i: int = 0
        j: int = 0
        troop: int = 4 if len(recruit_clearings) == 1 else (2 if len(recruit_clearings) == 2 else 1)
        recruit_clearings *= 2
        try:
            while i < 4:
                if self.supply[self._WARRIOR] < troop:
                    failed_recruits += troop
                    i += troop
                    j += 1
                    continue
                self.recruit(recruit_clearings[i], troop)
                i += troop
                j += 1
        except IndexError:
            failed_recruits += (4-i)
        if failed_recruits:
            print(f"{self.name} scores {failed_recruits//2} VP for warriors that could not be recruited.")
            self.score(failed_recruits//2)  
        # MOVE
        warrior_count: int = 0
        warriors_to_move: int = 0
        for u in self.get_clearings(suit=self.order.suit):
            print('move',u)
            possible_destinations: list[int] = self.get_adjacent_clearings(u)
            possible_destinations.sort(key=lambda c: (self.count_enemies(c, self), -c), reverse=True)
            v: int = possible_destinations[0]
            warrior_count = self.count_pieces(u, self._WARRIOR)
            warriors_to_move = max(0, warrior_count-3)
            if self == self.clearings[u].ruler and self.clearings[u].free:
                # Need to find the rule threshold for the clearing, i.e. 1 + number of enemy warriors and buildings. If the number of warriors left behind is less than this threshold, we need to reduce the number of warriors moved.
                rule_threshold: int = 1 + self.count_enemies(u, self, rule=True)
                if warrior_count - warriors_to_move < rule_threshold:
                    warriors_to_move = max(0, warrior_count - rule_threshold)
            if warriors_to_move > 0 and (self.rules(u) or self.rules(v)):
                self.move(u, v, warriors_to_move)
                first_enemy: list[Faction] = [f for f in self.clearings[v].pieces.keys() if f != self]
                if self.order.suit == Suit.BIRD and self.clearings[v].faction_presence(first_enemy).numpieces > 0:
                    self.battle(v, first_enemy[0])
        
        build_clearings: list[int] = sorted(
            self.get_clearings(ruler=self, suit=self.order.suit),
            key=lambda c: (self.clearings[c].free, self.count_pieces(c, piece=self._WARRIOR), -c),
            reverse=True
        )
        print(build_clearings)
        for c in build_clearings:
            print(c, self.rules(c))
        
        building: Piece = self._SAWMILL
        match self.order.suit:
            case Suit.FOX:
                building = self._SAWMILL
            case Suit.RABBIT:
                building = self._WORKSHOP
            case Suit.MOUSE:
                building = self._RECRUITER
            case _:
                choices: list[Piece] = [self._SAWMILL, self._WORKSHOP, self._RECRUITER]
                building = sorted(choices, key=lambda p: self.supply[p], reverse=True)[0]
        if len(build_clearings) > 0:
            build_location: int = build_clearings[0]
            if self.clearings[build_location].free and self.supply[building] > 0:
                self.build(build_location, building)
    
    
    def evening(self):
        """Execute the evening phase."""
        while len(self.revealed) > 0:
            self.discard(self.revealed, self.revealed[-1])
        print(f"{str(self)} discards {self.order}.")