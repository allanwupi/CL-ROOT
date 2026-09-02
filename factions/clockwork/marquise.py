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
        self.draw(self.revealed, 1)
        self.order = self.revealed[0]
        print(f"{self.name} reveals {str(self.order)}.")
        if (self.order.item and self.order.item.in_stock):
            self.craft(self.revealed, self.order, override = 1)
        elif (self.order.persistent and self.order not in self.effects):
            self.craft(self.revealed, self.order)
    
    def daylight(self):
        """Execute the daylight phase."""
        pass
    
    def evening(self):
        """Execute the evening phase."""
        while len(self.revealed) > 0:
            self.discard(self.revealed, self.revealed[-1])
        print(f"{self.name} discards {self.order}.")

"""
    # Birdsong
        print(f'\033[38;5;179m\033[1m~Birdsong~\033[0m')
        order: Card = self.draw()
        ordered_suit: Suit = order.suit
        print(f"{self.name} reveals {order.name}.")
        craftpoints = order.points
        if (order.item and order.item in self.game.item_supply):
            print(f"{self.name} crafts {order.item}, scoring 1 VP.")
            self.craft(order, override = 1)
        elif (order.persistent and order.name not in self.crafted_effects):
            print(f"{self.name} crafts {order.name}, scoring {order.points} VP.")
            self.craft(order)
        
        # Daylight
        print(f'\033[38;5;117m\033[1m~Daylight~\033[0m')
        print(f"{self.name} initiates a battle in each {'' if ordered_suit == Suit.BIRD else str(ordered_suit)+' '}clearing.")  # Only 1 enemy for now
        for (clearing, enemy) in self.get_battles(piece='M', suit=ordered_suit):
            self.battle(clearing, enemy)
        
        print(f"{self.name} recruits 4x {self.piece_names['M']} among ruled ordered clearings.")
        recruit_clearings = []
        if ordered_suit == Suit.BIRD:
            recruit_clearings = sorted(self.get_ruled_clearings(), key=id, reverse=True)[:2]
        else:
            recruit_clearings = sorted(self.get_ruled_clearings(suit=ordered_suit), key=id)
        failed_recruits: int = 0
        i: int = 0
        j: int = 0
        # print(recruit_clearings)
        troop: int = 4 if len(recruit_clearings) == 1 else (2 if len(recruit_clearings) == 2 else 1)
        recruit_clearings *= 2
        try:
            while i < 4:
                if self.supply['M'] < troop:
                    failed_recruits += troop
                    i += troop
                    j += 1
                    continue
                self.place(recruit_clearings[i], 'M', troop)
                print(f"{self.game.PADDING}{self.name} recruits {troop:d}x {self.piece_names['M']} at {self.game[recruit_clearings[j]].nickname:s}.")
                i += troop
                j += 1
        except IndexError:
            failed_recruits += (4-i)
        if failed_recruits:
            print(f"{self.name} scores {failed_recruits//2} VP for warriors that could not be recruited.")
            self.game.score(self, failed_recruits//2)
            
        warrior_count: int = 0
        warriors_to_move: int = 0
        for u in self.get_ruled_clearings(suit=ordered_suit):
            possible_destinations: list[int] = self.game.adjacent(u)
            possible_destinations.sort(key=lambda c: (self.game.count_enemies(self, c), -c), reverse=True)
            v: int = possible_destinations[0]
            warrior_count = self.game.count(self, u, piece='M')
            warriors_to_move = max(0, warrior_count-3)
            if self.rules(u) and self.game[u].free():
                # Need to find the rule threshold for the clearing, i.e. 1 + number of enemy warriors and buildings. If the number of warriors left behind is less than this threshold, we need to reduce the number of warriors moved.
                rule_threshold: int = 1 + self.game.count_enemies(self, u, rule=True)
                if warrior_count - warriors_to_move < rule_threshold:
                    warriors_to_move = max(0, warrior_count - rule_threshold)
            if warriors_to_move > 0:
                print(f"{self.name} moves {warriors_to_move:d}x {self.piece_names['M']} from {self.game[u].nickname:s} to {self.game[v].nickname:s}.")
                self.move(u, v, 'M', warriors_to_move)
                first_enemy = [f for f in self.game.presence(v) if f.id != self.id]
                if ordered_suit == Suit.BIRD and len(first_enemy) > 0:
                    self.battle(v, first_enemy[0])
        
        build_clearings: list[int] = sorted(
            self.get_ruled_clearings(),
            key=lambda c: (self.game[c].free(), self.game[c].count(self.id, piece='M'), self.game.size-c),
            reverse=True
        )
        
        building: str = ''
        if ordered_suit == Suit.FOX:
            building = '[S]'
        elif ordered_suit == Suit.RABBIT:
            building = '[W]'
        elif ordered_suit == Suit.MOUSE:
            building = '[R]'
        else:
            choices = ['[S]','[W]','[R]']
            building = sorted(choices, key=lambda p: self.supply[p], reverse=True)[0]
        if len(build_clearings) > 0:
            build_clearing = build_clearings[0]
            if self.game[build_clearing].free() and self.supply[building] > 0:
                vp: int = 7-self.supply[building]
                print(f"{self.name} builds {self.piece_names[building]} in {self.game[build_clearing].nickname}, scoring {vp:d} VP.")
                self.build(build_clearing, building)
                self.game.score(self, vp)
            
        # Evening
        print(f'\033[38;5;244m\033[1m~Evening~\033[0m')
        if order in self.hand:
            super().discard(order)
        print(f"{self.name} discards {order.name}.")
"""
