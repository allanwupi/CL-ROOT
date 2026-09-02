from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

from board.clearing import Clearing
from board.suit import Suit
from factions.faction import Faction

# Suggested by Copilot

@dataclass(frozen=True)
class ClearingScore:
    clearing: int
    ruler: Faction | None
    allied_pieces: int
    allied_warriors: int
    enemy_pieces: int
    enemy_warriors: int
    free_slot: bool
    suit_match: bool


class ActionPlanner:
    def __init__(self, board):
        self.board = board

    # ---------- basic filters ----------
    def ordered_clearings(self, clearings: Iterable[int]) -> list[int]:
        return sorted(clearings, key=lambda n: n)

    def by_suit(self, clearings: Iterable[int], suit: Suit) -> list[int]:
        return [n for n in clearings if self.board[n].suit in suit]

    def by_rule(self, clearings: Iterable[int], faction: Faction) -> list[int]:
        return [
            n for n in clearings
            if self._has_strict_rule_advantage(self.board[n], faction)
        ]

    def by_free_slot(self, clearings: Iterable[int]) -> list[int]:
        return [n for n in clearings if self.board[n].free]

    # ---------- presence helpers ----------
    def presence(self, clearing: int, faction: Faction):
        return self.board[clearing].faction_presence(faction)

    def allied_presence(self, clearing: int, faction: Faction):
        p = self.board[clearing].faction_presence(faction)
        return p

    def enemy_presence(self, clearing: int, faction: Faction) -> int:
        total = 0
        for other in self.board[clearing].pieces:
            if other is faction:
                continue
            total += sum(self.board[clearing].pieces[other].values())
        return total

    def allied_piece_count(self, clearing: int, faction: Faction) -> int:
        if faction not in self.board[clearing].pieces:
            return 0
        return sum(self.board[clearing].pieces[faction].values())

    def allied_warrior_count(self, clearing: int, faction: Faction) -> int:
        if faction not in self.board[clearing].pieces:
            return 0
        total = 0
        for piece, count in self.board[clearing].pieces[faction].items():
            if piece.can_battle and piece.name.lower().startswith("warrior"):
                total += count
        return total

    def enemy_warrior_count(self, clearing: int, faction: Faction) -> int:
        total = 0
        for other in self.board[clearing].pieces:
            if other is faction:
                continue
            for piece, count in self.board[clearing].pieces[other].items():
                if piece.can_battle and piece.name.lower().startswith("warrior"):
                    total += count
        return total

    def _has_strict_rule_advantage(self, clearing: Clearing, faction: Faction) -> bool:
        if not clearing.pieces:
            return False

        my_rule = clearing.faction_presence(faction).rule
        for other in clearing.pieces:
            if other is faction:
                continue
            if clearing.faction_presence(other).rule >= my_rule:
                return False
        return True

    # ---------- action generation ----------
    def legal_moves(self, faction: Faction, ordered_suit: Suit) -> list[tuple[int, int, int]]:
        moves: list[tuple[int, int, int]] = []
        for origin in self.ordered_clearings(self.board.get_clearings(ruler=faction, return_indices=True)):
            if self.board[origin].suit not in ordered_suit:
                continue

            allied = self.allied_piece_count(origin, faction)
            if allied <= 0:
                continue

            for destination in self.board.get_adjacent_clearings(origin):
                if destination == origin:
                    continue

                if not self._move_legal(faction, origin, destination):
                    continue

                num = max(1, allied - 3)  # rough placeholder
                moves.append((origin, destination, num))
        return moves

    def _move_legal(self, faction: Faction, origin: int, destination: int) -> bool:
        origin_clearing = self.board[origin]
        destination_clearing = self.board[destination]

        # must be adjacent
        if destination not in origin_clearing.adjlist:
            return False

        # must either rule origin or destination, or both
        rule_origin = origin_clearing.ruler is faction
        rule_dest = destination_clearing.ruler is faction
        if not (rule_origin or rule_dest):
            return False

        # rough rule: not moving into place with no legal path or same suit restriction
        return True

    def legal_battles(self, faction: Faction, ordered_suit: Suit) -> list[int]:
        battles: list[int] = []
        for clearing in self.ordered_clearings(range(1, self.board.size)):
            if self.board[clearing].suit not in ordered_suit:
                continue

            if self.allied_warrior_count(clearing, faction) <= 0:
                continue

            if self.enemy_presence(clearing, faction) <= 0:
                continue

            battles.append(clearing)
        return battles

    def legal_builds(self, faction: Faction, ordered_suit: Suit) -> list[int]:
        builds: list[int] = []
        for clearing in self.ordered_clearings(range(1, self.board.size)):
            if self.board[clearing].suit not in ordered_suit:
                continue

            if not self.board[clearing].free:
                continue

            if self.board[clearing].ruler is not faction:
                continue

            # optionally require some allied warriors present
            if self.allied_warrior_count(clearing, faction) <= 0:
                continue

            builds.append(clearing)
        return builds