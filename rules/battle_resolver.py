from __future__ import annotations
from board.clearing import Clearing
from factions.faction import Faction
from components.pieces import Piece

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.action import Battle, Remove
    from game.game import Game

class BattleResolver:
    def __init__(self, game: Game, battle: Battle):
        self.game: Game = game
        self.attacker: Faction = battle.owner
        self.clearing: Clearing = battle._clearing
        self.number: int = battle.clearing
        self.defender: Faction = battle.defender
        self.rolls: tuple[int, int] = battle.rolls

    @staticmethod
    def _deal_hits(game: Game, faction: Faction, number: int, targets: list[tuple[Piece, int]], hits: int) -> None:
        for piece, count in targets:
            if (hits == 0):
                break
            hits_dealt: int = min(hits, count) # Cannot deal more hits than there are pieces
            Remove(game=game, owner=faction, clearing=number, piece=piece, numpieces=hits_dealt).execute()
            hits -= hits_dealt
            # Scoring of VP is handled by Remove
    
    def resolve(self, suppress: bool = False) -> None:
        allies_by_priority: list[tuple[Piece, int]] = sorted(
            [
                (piece, self.clearing[self.attacker][piece])
                for piece in self.attacker.supply.keys()
                if self.clearing[self.attacker][piece] > 0
            ],
            key=lambda x: (len(x[0]), int(x[0].piecetype))
        )
        targets_by_priority: list[tuple[Piece, int]] = sorted(
            [
                (target, self.clearing[self.defender][target])
                for target in self.defender.supply.keys()
                if self.clearing[self.defender][target] > 0
            ],
            key=lambda x: (len(x[0]), int(x[0].piecetype))
        )
        numattackers: int = sum(
            piece_count[1]
            for piece_count in allies_by_priority
            if piece_count[0].can_battle
        )
        numdefenders: int = sum(
            piece_count[1]
            for piece_count in targets_by_priority
            if piece_count[0].can_battle
        )
        attacker_hits: int = (
            min(max(self.rolls), numattackers)
            + int(numdefenders == 0) # +1 for defenseless target
        )
        defender_hits: int = min(min(self.rolls), numdefenders) # TODO: account for bonus hits
        if not suppress:
            from ui.renderer import _PADDING
            print(f"{_PADDING}Attacker {str(self.attacker)} deals {attacker_hits:d} {'hit' if attacker_hits==1 else 'hits'}; "
                f"defender {str(self.defender)} deals {defender_hits:d} {'hit' if defender_hits==1 else 'hits'}.")
        if attacker_hits > 0:
            self._deal_hits(self.game, self.attacker, self.number, targets_by_priority, attacker_hits)
        if defender_hits > 0:
            self._deal_hits(self.game, self.defender, self.number, allies_by_priority, defender_hits)
    
        
"""
    def deal_hits(self, faction: AbstractFaction, clearing: int, enemy: AbstractFaction, target_priority: list, hits: int) -> None:
        for piece in target_priority:
            if (hits == 0):
                break
            piecename = enemy.piece_names[piece]
            if piece not in self.clearings[clearing].presence[enemy.id]:
                continue
            building = '[' in piece
            hits_dealt: int = self.put(enemy, clearing, piece, -hits, building)
            hits -= hits_dealt
            if enemy.piece_values[piece] > 0:
                print(f'{self.PADDING}{faction.name} removes {hits_dealt}x {enemy.name} {piecename}, scoring {hits_dealt * enemy.piece_values[piece]} VP.')
            else:
                print(f'{self.PADDING}{faction.name} removes {hits_dealt}x {enemy.name} {piecename}.')
            self.score(faction, hits_dealt * enemy.piece_values[piece])
"""
