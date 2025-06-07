from player.player import Player
import random

class BotPlayer(Player):
    """A bot player that automatically plays its turn."""
    
    def __init__(self, name: str):
        """Initialize the bot player with a name."""
        super().__init__(name)
    
    def play_turn(self, game):
        """Automatically play the bot's turn."""
        print(f"\n{self.name} is playing...")
        
        # Decision 1: Draw from deck or discard pile
        should_draw_discard = self._should_draw_from_discard(game)
        if should_draw_discard:
            print(f"{self.name} draws from discard pile")
            top_card = game.take_from_discard()
            if top_card:
                self.hand.add(top_card)
        else:
            print(f"{self.name} draws from deck")
            self.draw_card(game.deck)
        
        # Decision 2: Try to lay down phase if possible
        if not self.has_laid_down:
            self._try_lay_down_phase()
        
        # Decision 3: Try to hit on other players if already laid down
        if self.has_laid_down:
            self._try_hit_on_players(game)
        
        # Decision 4: Discard a card
        discard_index = self._choose_discard()
        print(f"{self.name} discards {self.hand[discard_index]}")
        self.discard_card(game.deck, discard_index)
        
        print(f"{self.name} has {len(self.hand)} cards remaining")

    def _should_draw_from_discard(self, game):
        """Decide whether to draw from discard pile."""
        top_discard = game.get_top_discard()
        if not top_discard:
            return False
        
        # Always take if it helps complete current phase
        if self._card_helps_phase(top_discard):
            return True
        
        # Take if it forms a set with cards in hand
        if self._card_forms_set(top_discard):
            return True
        
        # Take if it extends a run
        if self._card_extends_run(top_discard):
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
        
        if self._can_satisfy_phase(phase_req, sets, runs):
            groups = self._build_phase_groups(phase_req, sets, runs)
            if groups and self.lay_down(groups):
                print(f"{self.name} laid down Phase {self.current_phase}!")
                return True
        
        return False
    
    def _can_satisfy_phase(self, requirements, sets, runs):
        """Check if current hand can satisfy phase requirements."""
        # Simplified check - just see if we have enough sets/runs
        set_count = len(sets)
        run_count = len(runs)
        
        needed_sets = sum(1 for req_type, _ in requirements if req_type == 'set')
        needed_runs = sum(1 for req_type, _ in requirements if req_type == 'run')
        
        return set_count >= needed_sets and run_count >= needed_runs
    
    def _build_phase_groups(self, requirements, sets, runs):
        """Build groups of cards to satisfy phase requirements."""
        groups = []
        used_card_ids = set()
        
        for req_type, req_size in requirements:
            if req_type == 'set':
                # Find a set of the required size
                for set_ids in sets:
                    if len(set_ids) >= req_size and not any(id in used_card_ids for id in set_ids):
                        # Take only the required number of cards
                        selected_ids = set_ids[:req_size]
                        group = [card for card in self.hand.cards if card.id in selected_ids]
                        groups.append(group)
                        used_card_ids.update(selected_ids)
                        break
            elif req_type == 'run':
                # Find a run of the required size
                for run_ids in runs:
                    if len(run_ids) >= req_size and not any(id in used_card_ids for id in run_ids):
                        # Take only the required number of cards
                        selected_ids = run_ids[:req_size]
                        group = [card for card in self.hand.cards if card.id in selected_ids]
                        groups.append(group)
                        used_card_ids.update(selected_ids)
                        break
        
        return groups if len(groups) == len(requirements) else []
    
    def _try_hit_on_players(self, game):
        """Try to hit cards on other players' laid down sets."""
        for player in game.players:
            if player != self and player.has_laid_down:
                for set_idx, laid_set in enumerate(player.laid_down_sets):
                    # Try each card in hand
                    for card in self.hand.cards:
                        if self._can_hit_card(card, laid_set):
                            print(f"{self.name} hits {card} on {player.name}'s set")
                            # Simple hit logic - just add to the set
                            self.hand.remove(card)
                            player.laid_down_sets[set_idx].append(card)
                            return True
        return False
    
    def _can_hit_card(self, card, laid_set):
        """Check if a card can be hit on a laid down set."""
        if not laid_set:
            return False
        
        # For wild cards, can usually hit anywhere
        if card.card_type == 'wild':
            return True
        
        # For number cards, check if it matches the set pattern
        if card.card_type == 'number':
            # Check if it's a set (same numbers)
            first_number_card = next((c for c in laid_set if c.card_type == 'number'), None)
            if first_number_card and card.number == first_number_card.number:
                return True
            
            # Check if it extends a run
            numbers = sorted([c.number for c in laid_set if c.card_type == 'number'])
            if numbers:
                # Check if card extends the run at either end
                return card.number == numbers[0] - 1 or card.number == numbers[-1] + 1
        
        return False
    
    def _choose_discard(self):
        """Choose which card to discard."""
        if not self.hand.cards:
            return 0
        
        # Priority: discard highest value cards that don't help with phase
        scores = []
        for i, card in enumerate(self.hand.cards):
            score = self._calculate_discard_score(card)
            scores.append((score, i))
        
        # Sort by score (higher score = better to discard)
        scores.sort(reverse=True)
        return scores[0][1]
    
    def _calculate_discard_score(self, card):
        """Calculate how good it is to discard this card (higher = better to discard)."""
        score = 0
        
        # Higher value cards are generally better to discard
        if card.card_type == 'number':
            score += card.number
        elif card.card_type in ['wild', 'skip']:
            score -= 10  # Keep special cards
        
        # Cards that help with current phase are worse to discard
        if self._card_helps_phase(card):
            score -= 20
        
        # Cards that form sets/runs are worse to discard
        if self._card_forms_set(card) or self._card_extends_run(card):
            score -= 10
        
        return score