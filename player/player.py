from hand.hand import Hand
from laiddownset.laiddownset import LaidDownSet


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.current_phase = 1
        self.laid_down_sets = []
        self.has_laid_down_phase = False
        self.round_score = 0
        self.total_score = 0

    def draw_card(self, card):
        """Add a card to the player's hand."""
        self.hand.add_card(card)

    def discard_card(self, card_index):
        """Remove and return a card from the player's hand."""
        if 0 <= card_index < len(self.hand.cards):
            return self.hand.cards.pop(card_index)
        return None

    def lay_down(self, sets):
        """Lay down sets for the current phase."""
        if self.has_laid_down_phase:
            return False
        
        # Validate the sets meet phase requirements
        from phase_validator.phase_validator import PhaseValidator
        validator = PhaseValidator()
        
        if validator.is_valid_phase(self.current_phase, sets):
            # Remove cards from hand and create laid down sets
            for card_set in sets:
                # Remove cards from hand
                for card in card_set:
                    if card in self.hand.cards:
                        self.hand.cards.remove(card)
                
                # Create laid down set
                laid_down_set = LaidDownSet(card_set)
                self.laid_down_sets.append(laid_down_set)
            
            self.has_laid_down_phase = True
            return True
        
        return False

    def hit_on_set(self, card, set_index):
        """Add a card to an existing laid down set."""
        if set_index < len(self.laid_down_sets):
            set_to_hit = self.laid_down_sets[set_index]
            if set_to_hit.can_add_card(card):
                set_to_hit.add_card(card)
                # Remove card from hand
                if card in self.hand.cards:
                    self.hand.cards.remove(card)
                return True
        return False

    def calculate_hand_score(self):
        """Calculate the score of remaining cards in hand."""
        score = 0
        for card in self.hand.cards:
            if card.card_type == 'number':
                if card.number <= 9:
                    score += 5
                else:  # 10, 11, 12
                    score += 10
            elif card.card_type == 'skip':
                score += 15
            elif card.card_type == 'wild':
                score += 25
        return score

    def reset_for_new_round(self):
        """Reset player state for a new round."""
        self.hand = Hand()
        self.laid_down_sets = []
        self.has_laid_down_phase = False
        self.round_score = 0

    def advance_phase(self):
        """Advance to the next phase if current phase is complete."""
        if self.has_laid_down_phase and len(self.hand.cards) == 0:
            self.current_phase += 1
            return True
        return False

    def get_phase_requirements(self):
        """Get the requirements for the current phase."""
        phase_requirements = {
            1: "2 sets of 3",
            2: "1 set of 3 + 1 run of 4",
            3: "1 set of 4 + 1 run of 4",
            4: "1 run of 7",
            5: "1 run of 8",
            6: "1 run of 9",
            7: "2 sets of 4",
            8: "7 cards of one color",
            9: "1 set of 5 + 1 set of 2",
            10: "1 set of 5 + 1 set of 3"
        }
        return phase_requirements.get(self.current_phase, "Unknown phase")

    def __str__(self):
        return f"{self.name} (Phase {self.current_phase}, Score: {self.total_score})"