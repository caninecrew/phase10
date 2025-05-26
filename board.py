from card import Card
from laiddownset import LaidDownSet
from typing import List

class GameBoard:
    """Tracks all players' laid-down sets during gameplay."""
    def __init__(self):
        """Initialize an empty game board."""
        self.player_sets = {}  # Dictionary mapping player names to their laid down sets
        
    def add_phase_set(self, player_name: str, cards: List[Card], set_type: str = 'set') -> None:
        """Add a laid down set for a player."""
        if player_name not in self.player_sets:
            self.player_sets[player_name] = []
        laid_down_set = LaidDownSet(cards, set_type)
        self.player_sets[player_name].append(laid_down_set)
        
    def get_sets(self, player_name: str) -> List[LaidDownSet]:
        """Get all laid down sets for a player."""
        return self.player_sets.get(player_name, [])
        
    def show(self) -> str:
        """Display all laid down sets for all players."""
        output = []
        for player, sets in self.player_sets.items():
            output.append(f"\n{player}'s laid down sets:")
            for i, laid_down_set in enumerate(sets, 1):
                cards_str = ', '.join(str(card) for card in laid_down_set.cards)
                output.append(f"  Set {i} ({laid_down_set.set_type}): {cards_str}")
        return '\n'.join(output)
