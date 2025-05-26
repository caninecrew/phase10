class LaidDownSet:
    def __init__(self, cards, set_type):
        """Initialize a laid down set of cards.
        
        Args:
            cards: List of Card objects
            set_type: Type of set ('set', 'run', or 'color')
        """
        self.cards = cards  # list of Card objects
        self.set_type = set_type  # e.g., 'set', 'run', 'color'
        self.validate()
    
    def validate(self):
        """Validate that the cards form a valid set of the specified type."""
        if not self.cards:
            raise ValueError("Cannot create an empty set")
            
        if self.set_type == 'set':
            return self._validate_set()
        elif self.set_type == 'run':
            return self._validate_run()
        elif self.set_type == 'color':
            return self._validate_color()
        else:
            raise ValueError(f"Invalid set type: {self.set_type}")
    
    def _validate_set(self):
        """Validate that all cards have the same number (except wilds)."""
        number_cards = [c for c in self.cards if c.card_type == 'number']
        if not number_cards:
            raise ValueError("Set must contain at least one number card")
            
        target_number = number_cards[0].number
        for card in number_cards:
            if card.number != target_number:
                raise ValueError("All cards in a set must have the same number")
                
        return True
    
    def _validate_run(self):
        """Validate that cards form a consecutive sequence."""
        number_cards = [c for c in self.cards if c.card_type == 'number']
        if not number_cards:
            raise ValueError("Run must contain at least one number card")
            
        numbers = sorted(card.number for card in number_cards)
        for i in range(len(numbers) - 1):
            if numbers[i] + 1 != numbers[i + 1]:
                raise ValueError("Cards in a run must be consecutive")
                
        return True
    
    def _validate_color(self):
        """Validate that all cards have the same color (except wilds)."""
        color_cards = [c for c in self.cards if c.card_type == 'number']
        if not color_cards:
            raise ValueError("Color set must contain at least one number card")
            
        target_color = color_cards[0].color
        for card in color_cards:
            if card.color != target_color:
                raise ValueError("All cards in a color set must have the same color")
                
        return True
    
    def add_card(self, card):
        """Add a card to the set if it maintains validity."""
        test_cards = self.cards + [card]
        test_set = LaidDownSet(test_cards, self.set_type)
        # If validation passes, add the card
        self.cards.append(card)
        return True
    
    def remove_card(self, card):
        """Remove a card from the set if it exists."""
        if card in self.cards:
            self.cards.remove(card)
            if self.cards:  # If there are still cards, validate
                self.validate()
            return True
        return False
    
    def __len__(self):
        """Return the number of cards in the set."""
        return len(self.cards)
    
    def __str__(self):
        """Return a string representation of the laid down set."""
        type_str = f"{self.set_type.capitalize()} of {len(self.cards)}: "
        cards_str = ', '.join(str(card) for card in self.cards)
        return type_str + cards_str
    
    def __repr__(self):
        """Return a detailed string representation of the laid down set."""
        return f"LaidDownSet(cards={self.cards!r}, set_type={self.set_type!r})"
