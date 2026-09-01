from dataclasses import dataclass
from factions.faction import TurnPhase

@dataclass
class TurnManager:
    turn_number: int = 0
    player_count: int = 0
    current_player: int = -1
    current_phase: TurnPhase = TurnPhase.BIRDSONG
    
    def next(self) -> int:
        self.current_player = (self.current_player + 1) % self.player_count
        return self.current_player