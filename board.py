class GameBoard:
    """Tracks all players' laid-down sets during gameplay."""
    def __init__(self):
        self.player_sets = {}  # Dictionary mapping player names to their laid down sets

    def add_phase_set(self, player, group):
        """Add a laid down set for a player.
        
        Args:
            player (str): Player's name
            group (list): List of cards forming the set
        """
        if player not in self.player_sets:
            self.player_sets[player] = []
        self.player_sets[player].append(group)

    def get_sets(self, player):
        """Get all laid down sets for a player.
        
        Args:
            player (str): Player's name
            
        Returns:
            list: List of card groups laid down by the player
        """
        return self.player_sets.get(player, [])

    def show(self):
        """Display all laid down sets for all players."""
        output = []
        for player, sets in self.player_sets.items():
            output.append(f"\n{player}'s laid down sets:")
            for i, set_ in enumerate(sets, 1):
                output.append(f"  Set {i}: {', '.join(str(card) for card in set_)}")
        return '\n'.join(output)
