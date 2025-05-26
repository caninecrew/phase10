from typing import List, Dict, Optional, Tuple
from card import Card
from deck import Deck
from player import Player
from board import GameBoard
from phase_validator import PhaseValidator
from hit_manager import HitManager

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
        self.scores: Dict[str, int] = {player.name: 0 for player in self.players}
        self._deal_initial_cards()

    def _deal_initial_cards(self) -> None:
        """Deal 10 cards to each player."""
        for _ in range(10):
            for player in self.players:
                player.draw_card(self.deck)

    def start_round(self) -> None:
        """Start a new round."""
        for player in self.players:
            player.has_laid_down = False
            player.laid_down_sets = []
        self.deck = Deck()
        self.round_end = False
        self._deal_initial_cards()
        first_card = self.deck.draw()
        self.deck.discard(first_card)

    def next_player(self) -> None:
        """Move to the next player."""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def get_current_player(self) -> Player:
        """Get the current player."""
        return self.players[self.current_player_idx]

    def validate_phase(self, player: Player, groups: List[Card]) -> bool:
        """Validate if the groups satisfy the requirements for the player's current phase."""
        return PhaseValidator.validate_phase(player.current_phase, groups)

    def play_turn(self, draw_from_discard: bool = False, groups_to_lay: Optional[List[Card]] = None, 
                 hit_on_groups: Optional[List[Tuple[int, int, Card]]] = None, discard_index: Optional[int] = None) -> bool:
        """Execute a player's turn."""
        player = self.get_current_player()

        # Draw phase
        if draw_from_discard:
            if not self.deck.discard_pile:
                return False
            card = self.deck.take_from_discard()
            player.hand.add(card)
        else:
            if not player.draw_card(self.deck):
                return False

        # Lay down phase
        if groups_to_lay and not player.has_laid_down:
            if not self.validate_phase(player, groups_to_lay):
                return False

            player.has_laid_down = True
            for group in groups_to_lay:
                for card in group:
                    player.hand.remove(card)
                player.laid_down_sets.append(group)

        # Hit on other players
        if hit_on_groups:
            for p_idx, set_idx, card in hit_on_groups:
                target_player = self.players[p_idx]
                if not HitManager.try_hit(player, target_player, set_idx, card):
                    return False

        # Discard phase
        if discard_index is not None:
            if not player.discard_card(self.deck, discard_index):
                return False

            if len(player.hand) == 0:
                self.round_end = True
                player.current_phase += 1
                if player.current_phase > 10:
                    self.game_end = True
                return True

        self.next_player()
        return True

    def calculate_round_scores(self):
        """Calculate scores for all players at the end of a round.
        Players score points for unplayed cards:
            - Number cards: face value
            - Skip and Wild cards: 25 points
        Winner scores 0, other players accumulate points."""
        if not self.round_end:
            return

        # Find the winning player (empty hand)
        winner = None
        for p in self.players:
            if len(p.hand) == 0:
                winner = p
                break

        if not winner:
            return

        # Calculate scores for unplayed cards
        for player in self.players:
            if player == winner:
                continue

            score = 0
            for card in player.hand.cards:
                if card.card_type == 'number':
                    score += card.number
                else:  # wild or skip
                    score += 25

            self.scores[player.name] += score

        return

    def get_game_state(self):
        """Get the current state of the game."""
        return {
            'current_player': self.get_current_player().name,
            'scores': self.scores.copy(),
            'round_end': self.round_end,
            'game_end': self.game_end,
            'players': [{
                'name': p.name,
                'phase': p.current_phase,
                'has_laid_down': p.has_laid_down,
                'hand_size': len(p.hand),
                'laid_down_sets': [[str(card) for card in set_] 
                                 for set_ in p.laid_down_sets]
            } for p in self.players],
            'deck_size': len(self.deck.cards),
            'top_discard': str(self.deck.discard_pile[-1]) if self.deck.discard_pile else None
        }

    def __str__(self):
        """Return a string representation of the game state."""
        state = self.get_game_state()
        output = []
        output.append(f"Current Player: {state['current_player']}")
        output.append("\nScores:")
        for name, score in state['scores'].items():
            output.append(f"{name}: {score}")
        output.append("\nPlayer Status:")
        for player in state['players']:
            output.append(f"\n{player['name']}:")
            output.append(f"  Phase: {player['phase']}")
            output.append(f"  Hand Size: {player['hand_size']}")
            output.append(f"  Laid Down: {player['has_laid_down']}")
            if player['laid_down_sets']:
                output.append("  Laid Down Sets:")
                for i, set_ in enumerate(player['laid_down_sets'], 1):
                    output.append(f"    Set {i}: {', '.join(set_)}")
        output.append(f"\nDeck Size: {state['deck_size']}")
        output.append(f"Top Discard: {state['top_discard']}")
        return '\n'.join(output)