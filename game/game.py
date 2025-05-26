from typing import List
from player.player import Player
from deck.deck import Deck
from board.board import GameBoard

class Game:
    def __init__(self, player_names: List[str]):
        """Initialize the game with a list of player names."""
        if len(player_names) < 2 or len(player_names) > 6:
            raise ValueError("Phase 10 requires 2-6 players")

        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.board = GameBoard()
        self.current_player_idx = 0
        self.round_end = False
        self.game_end = False

        # Initialize each player's hand with 10 cards
        for player in self.players:
            player.hand = [self.deck.draw_card() for _ in range(10)]

    def get_current_player(self):
        """Return the current player."""
        return self.players[self.current_player_idx]

    def next_player(self):
        """Move to the next player."""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def validate_phase(self, player, phase_sets):
        """Validate the phase sets for a player."""
        # Placeholder for phase validation logic
        return True

    def play_turn(self, draw_from_discard: bool, discard_index: int):
        """Simulate a player's turn."""
        # Placeholder for turn logic
        self.next_player()
        return True

    def calculate_round_scores(self):
        """Calculate scores for the round."""
        # Placeholder for score calculation logic
        pass