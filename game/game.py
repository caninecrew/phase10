from deck.deck import Deck
from player.player import Player
import random


class Game:
    """Main game controller for Phase 10."""
    
    def __init__(self, players):
        """Initialize a new game with the given players."""
        self.players = players
        self.deck = Deck()
        self.current_player_index = 0
        self.round_number = 1
        self.game_over = False
        
    def start_new_round(self):
        """Start a new round of the game."""
        print(f"\nStarting Round {self.round_number}")
        
        # Reset all players for new round
        for player in self.players:
            player.reset_for_new_round()
        
        # Create and shuffle new deck
        self.deck = Deck()
        self.deck.shuffle()
        
        # Deal 10 cards to each player
        for _ in range(10):
            for player in self.players:
                card = self.deck.draw_card()
                if card:
                    player.draw_card(card)
        
        # Start discard pile with one card
        first_discard = self.deck.draw_card()
        if first_discard:
            self.deck.discard_pile.append(first_discard)
        
        # Reset turn order
        self.current_player_index = 0
    
    def get_current_player(self):
        """Get the current player whose turn it is."""
        return self.players[self.current_player_index]
    
    def end_turn(self):
        """End the current player's turn and move to next player."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def draw_from_deck(self, player):
        """Draw a card from the deck for the given player."""
        card = self.deck.draw_card()
        if card:
            player.draw_card(card)
            return card
        return None
    
    def take_from_discard(self, player):
        """Take the top card from the discard pile."""
        if self.deck.discard_pile:
            card = self.deck.discard_pile.pop()
            player.draw_card(card)
            return card
        return None
    
    def discard_card(self, player, card_index):
        """Discard a card from the player's hand."""
        card = player.discard_card(card_index)
        if card:
            self.deck.discard_pile.append(card)
            return card
        return None
    
    def hit_on_player_set(self, hitting_player, target_player, set_index, card):
        """Allow a player to hit a card on another player's laid down set."""
        if set_index < len(target_player.laid_down_sets):
            laid_set = target_player.laid_down_sets[set_index]
            if laid_set.can_add_card(card):
                # Remove card from hitting player's hand
                if card in hitting_player.hand.cards:
                    hitting_player.hand.cards.remove(card)
                    laid_set.add_card(card)
                    return True
        return False
    
    def is_round_over(self):
        """Check if the current round is over."""
        # Round is over when any player has no cards left
        for player in self.players:
            if len(player.hand.cards) == 0:
                return True
        return False
    
    def is_game_over(self):
        """Check if the entire game is over."""
        # Game is over when any player reaches phase 11
        for player in self.players:
            if player.current_phase > 10:
                return True
        return False
    
    def calculate_round_scores(self):
        """Calculate scores for all players at the end of a round."""
        for player in self.players:
            player.round_score = player.calculate_hand_score()
            player.total_score += player.round_score
        
        # Advance phases for players who laid down and went out
        self.advance_phases()
    
    def advance_phases(self):
        """Advance phases for eligible players."""
        for player in self.players:
            if player.has_laid_down_phase and len(player.hand.cards) == 0:
                player.current_phase += 1
                print(f"{player.name} advances to Phase {player.current_phase}!")
    
    def reset_for_next_round(self):
        """Reset game state for the next round."""
        self.round_number += 1
        for player in self.players:
            player.reset_for_new_round()
    
    def get_game_state(self):
        """Get a summary of the current game state."""
        state = {
            'round': self.round_number,
            'current_player': self.get_current_player().name,
            'deck_cards': len(self.deck.cards),
            'discard_pile': len(self.deck.discard_pile),
            'players': []
        }
        
        for player in self.players:
            player_state = {
                'name': player.name,
                'phase': player.current_phase,
                'hand_size': len(player.hand.cards),
                'has_laid_down': player.has_laid_down_phase,
                'total_score': player.total_score
            }
            state['players'].append(player_state)
        
        return state
    
    def play_turn(self, player):
        """Play a complete turn for the given player."""
        # This method can be used for automated play
        # Draw phase
        if self.deck.discard_pile and self._should_take_discard(player):
            self.take_from_discard(player)
        else:
            self.draw_from_deck(player)
        
        # Phase laying phase
        if not player.has_laid_down_phase:
            self._try_lay_phase(player)
        
        # Hitting phase
        if player.has_laid_down_phase:
            self._try_hit_on_sets(player)
        
        # Discard phase
        if player.hand.cards:
            # For now, discard the last card (can be made smarter)
            self.discard_card(player, len(player.hand.cards) - 1)
    
    def _should_take_discard(self, player):
        """Determine if player should take from discard pile."""
        if not self.deck.discard_pile:
            return False
        
        top_card = self.deck.discard_pile[-1]
        
        # Simple heuristic: take wild cards and cards that match hand
        if top_card.card_type == 'wild':
            return True
        
        # Check if card helps with sets or runs
        if top_card.card_type == 'number':
            for card in player.hand.cards:
                if card.card_type == 'number' and card.number == top_card.number:
                    return True  # Helps form a set
        
        return False
    
    def _try_lay_phase(self, player):
        """Try to lay down the player's current phase."""
        # Find potential sets and runs
        sets = player.hand.find_sets(3)
        runs = player.hand.find_runs(4)
        
        # Phase-specific logic
        if player.current_phase == 1:  # 2 sets of 3
            if len(sets) >= 2:
                player.lay_down(sets[:2])
        
        elif player.current_phase == 2:  # 1 set of 3 + 1 run of 4
            if len(sets) >= 1 and len(runs) >= 1:
                player.lay_down([sets[0], runs[0]])
        
        elif player.current_phase == 4:  # 1 run of 7
            long_runs = [run for run in runs if len(run) >= 7]
            if long_runs:
                player.lay_down([long_runs[0]])
    
    def _try_hit_on_sets(self, player):
        """Try to hit cards on other players' sets."""
        for other_player in self.players:
            if other_player != player and other_player.has_laid_down_phase:
                for set_index, laid_set in enumerate(other_player.laid_down_sets):
                    for card in player.hand.cards[:]:
                        if laid_set.can_add_card(card):
                            self.hit_on_player_set(player, other_player, set_index, card)
                            break  # Only hit one card per player per turn