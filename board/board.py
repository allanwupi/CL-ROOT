from board.clearing import Clearing
from board.suit import Suit
from board.location import Location
from factions.faction import Faction, NullFaction
from components.pieces import Piece
from components.data import _ENVIRONMENT

class Board():
    def __init__(self, clearings: list[Clearing], ascii: str):
        self.clearings: list[Clearing] = clearings
        self.size: int = len(clearings)
        self.ascii: str = ascii
        self.environment: NullFaction = _ENVIRONMENT
    
    # Helpful methods for finding clearings
    def get_clearing_index(self, clearing: Clearing | int) -> int:
        return (
            self.clearings.index(clearing)
            if isinstance(clearing, Clearing)
            else clearing
        )
    
    def get_obj_from_indices(self, clearings: list[int]) -> list[Clearing]:
        return [self.clearings[number] for number in clearings]
    
    def get_clearings(
        self, ruler: Faction | None = None, faction: Faction | None = None,
        suit: Suit = Suit.WILD, location: Location | None = None,
        not_picked: bool = False, return_indices: bool = True
    ) -> list:
        # Work with indices then convert back to clearings as final step if necessary
        filtered_by_suit: list[int] = [i for i in range(1, self.size) if self.clearings[i].suit in suit]
        filtered_by_presence: list[int] = (
            [i for i in filtered_by_suit if self.clearings[i].faction_presence(faction).numpieces > 0]
            if faction is not None
            else filtered_by_suit
        )
        filtered_by_ruler: list[int] = (
            [i for i in filtered_by_presence if self.clearings[i].ruler is not None and self.clearings[i].ruler == ruler]
            if ruler is not None
            else filtered_by_presence
        )
        filtered_by_location: list[int] = (
            [i for i in filtered_by_ruler if self.clearings[i].location == location]
            if location is not None
            else filtered_by_ruler
        )
        final: list[int] = (
            [i for i in filtered_by_location if not self.clearings[i].homeland]
            if not_picked
            else filtered_by_location
        )
        if return_indices:
            return final
        else:
            return [self.clearings[i] for i in final]
    
    def get_battles(self, attacker: Faction, suit: Suit = Suit.WILD) -> list[tuple[int, Faction]]:
        filtered_by_suit: list[int] = [i for i in range(1, self.size) if self.clearings[i].suit in suit]
        attacker_present: list[int] = [
            i for i in filtered_by_suit if self.clearings[i].faction_presence(attacker).battle > 0
        ]
        battles: list[tuple[int, Faction]] = [
            (i, faction) for i in attacker_present for faction in self.clearings[0].pieces.keys()
            if faction != attacker and self.clearings[i].faction_presence(faction).numpieces > 0
        ]
        return battles
    
    def check_adjacency(self, clearing: Clearing | int, destination: Clearing | int) -> bool:
        origin_number: int = self.get_clearing_index(clearing)
        destination_number: int = self.get_clearing_index(destination)
        return destination_number in self.clearings[origin_number].adjlist
    
    def get_adjacent_clearings(
        self, clearing: Clearing | int,
        return_indices: bool = True
    ) -> list:
        number: int = self.get_clearing_index(clearing)
        adjacent: list[int] = [i for i in self.clearings[number].adjlist]
        return adjacent if return_indices else self.get_obj_from_indices(adjacent)
    
    def count_pieces(self, clearing: int, piece: Piece) -> int:
        return self.clearings[clearing].pieces[piece.owner][piece]
    
    def count_enemies(self, clearing: int, faction: Faction, rule: bool = False) -> int:
        return sum(
            self.count_pieces(clearing, piece)
            for f in self[clearing].pieces.keys()
            for piece in self[clearing].pieces[f].keys()
            if f != faction and (not rule or piece.can_rule)
        )
    
    def __len__(self) -> int:
        return self.size
    
    def __getitem__(self, key: int):
        return self.clearings[key]