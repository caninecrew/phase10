from player.player import Player
import random


class BotPlayer(Player):
    """A bot player that automatically plays its turn."""
    
    def __init__(self, name: str):
        """Initialize the bot player with a name."""
        super().__init__(name)
    
    def play_turn(self, game):
        """Automatically play the bot's turn."""
        # Decision 1: Draw from deck or discard pile
        should_draw_discard = self._should_draw_from_discard(game)
        if should_draw_discard and game.deck.discard_pile:
            card = game.take_from_discard(self)
        else:
            card = game.draw_from_deck(self)
        
        # Decision 2: Try to lay down phase if possible
        if not self.has_laid_down_phase:
            self._try_lay_down_phase()
        
        # Decision 3: Try to hit on other players if already laid down
        if self.has_laid_down_phase:
            self._try_hit_on_players(game)
        
        # Decision 4: Discard the least useful card
        self._discard_worst_card(game)
    
    def _should_draw_from_discard(self, game):
        """Determine if bot should draw from discard pile."""
        if not game.deck.discard_pile:
            return False
        
        top_discard = game.deck.discard_pile[-1]
        
        # Always take wild cards and skip cards
        if top_discard.card_type in ['wild', 'skip']:
            return True
        
        # Take if it helps with current phase
        if self._card_helps_phase(top_discard):
            return True
        
        return False
    
    def _card_helps_phase(self, card):
        """Check if card helps complete current phase."""
        # For simplicity, check if card forms sets or runs with hand
        return self._card_forms_set(card) or self._card_extends_run(card)
    
    def _card_forms_set(self, card):
        """Check if card forms a set with cards in hand."""
        if card.card_type != 'number':
            return True  # Wild cards are always useful
        
        same_number_count = sum(1 for c in self.hand.cards 
                               if c.card_type == 'number' and c.number == card.number)
        return same_number_count >= 2  # Would make a set of 3
    
    def _card_extends_run(self, card):
        """Check if card extends a run."""
        if card.card_type != 'number':
            return True  # Wild cards are always useful
        
        numbers = [c.number for c in self.hand.cards if c.card_type == 'number']
        numbers.append(card.number)
        numbers.sort()
        
        # Check for consecutive sequences
        consecutive_count = 1
        max_consecutive = 1
        
        for i in range(1, len(numbers)):
            if numbers[i] == numbers[i-1] + 1:
                consecutive_count += 1
                max_consecutive = max(max_consecutive, consecutive_count)
            else:
                consecutive_count = 1
        
        return max_consecutive >= 3  # Forms a run of at least 3
    
    def _try_lay_down_phase(self):
        """Try to lay down the current phase."""
        from phase_validator.phase_validator import PhaseValidator
        
        # Find all possible sets and runs
        sets = self.hand.find_sets(3)
        runs = self.hand.find_runs(4)
        
        # Try different combinations based on current phase
        phase_req = PhaseValidator.PHASE_REQUIREMENTS.get(self.current_phase, [])
        
        # Simple strategy: try to lay down if we have enough groups
        if self.current_phase == 1:  # 2 sets of 3
            if len(sets) >= 2:
                selected_sets = sets[:2]
                success = self.lay_down(selected_sets)
                if success:
                    return True
        
        elif self.current_phase == 2:  # 1 set of 3 + 1 run of 4
            if len(sets) >= 1 and len(runs) >= 1:
                selected_groups = [sets[0], runs[0]]
                success = self.lay_down(selected_groups)
                if success:
                    return True
        
        elif self.current_phase == 4:  # 1 run of 7
            long_runs = [run for run in runs if len(run) >= 7]
            if long_runs:
                success = self.lay_down([long_runs[0]])
                if success:
                    return True
        
        return False
    
    def _try_hit_on_players(self, game):
        """Try to hit cards on other players' laid down sets."""
        for other_player in game.players:
            if other_player != self and other_player.has_laid_down_phase:
                for set_index, laid_set in enumerate(other_player.laid_down_sets):
                    # Try each card in hand
                    for card in self.hand.cards[:]:  # Copy list to avoid modification during iteration
                        if laid_set.can_add_card(card):
                            success = game.hit_on_player_set(self, other_player, set_index, card)
                            if success:
                                break  # Only hit one card per turn
    
    def _discard_worst_card(self, game):
        """Discard the least useful card."""
        if not self.hand.cards:
            return
        
        # Score each card and discard the worst one
        card_scores = []
        for i, card in enumerate(self.hand.cards):
            score = self._score_card_usefulness(card)
            card_scores.append((score, i, card))
        
        # Sort by score (lower is worse)
        card_scores.sort()
        
        # Discard the worst card
        worst_score, worst_index, worst_card = card_scores[0]
        game.discard_card(self, worst_index)
    
    def _score_card_usefulness(self, card):
        """Score how useful a card is (higher = more useful)."""
        score = 0
        
        # Wild cards are always valuable
        if card.card_type == 'wild':
            return 100
        
        # Skip cards have medium value
        if card.card_type == 'skip':
            return 50
        
        # Number cards - check if they help with sets or runs
        if card.card_type == 'number':
            # Check if forms sets
            same_number_count = sum(1 for c in self.hand.cards 
                                   if c != card and c.card_type == 'number' and c.number == card.number)
            score += same_number_count * 10  # More matching cards = higher score
            
            # Check if extends runs
            numbers = [c.number for c in self.hand.cards if c != card and c.card_type == 'number']
            numbers.sort()
            
            # Check how well this card fits into sequences
            adjacent_count = 0
            for num in numbers:
                if abs(num - card.number) == 1:
                    adjacent_count += 1
            
            score += adjacent_count * 5
            
            # Lower numbered cards are generally easier to use
            if card.number <= 6:
                score += 5
        
        return score
