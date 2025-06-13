from card.card import Card

class Hand:
    def __init__(self):
        """Initialize an empty hand."""
        self.cards = []

    def add(self, card):
        """Add a card to the hand."""
        if not isinstance(card, Card):
            raise ValueError("Only Card instances can be added to the hand.")
        self.cards.append(card)
    
    def add_card(self, card):
        """Add a card to the hand (alias for add method)."""
        return self.add(card)

    def remove(self, card):
        """Remove a specific card from the hand."""
        if card in self.cards:
            self.cards.remove(card)
            return card
        return None
    
    def play(self, index):
        """Play a card from the hand by index."""
        if 0 <= index < len(self.cards):
            return self.cards.pop(index)
        return None
    
    def sort(self):
        """Sort the hand by color and number."""
        self.cards.sort(key=lambda c: (c.color or 'zzz', c.number or 99))  # Sort by color, then by number

    def find_sets(self, size=3):
        """Find sets of cards in the hand of a given size.
        Returns a list of lists containing card IDs that form sets.
        Returns ALL possible combinations of 'size' cards for when there are 
        more than 'size' cards with the same number.

        Args:
            size (int, optional): The size of sets to find. Defaults to 3.

        Returns:
            list[list[int]]: A list of lists, where each inner list contains card IDs 
                             that form a valid set of the specified size.
        """
        from collections import defaultdict
        from itertools import combinations
        by_number = defaultdict(list)
        results = []
        
        # Group cards by number (excluding wild and skip cards)
        for card in self.cards:
            if card.card_type == 'number' and card.number is not None:
                by_number[card.number].append(card.id)
        
        # For each group of same-numbered cards
        for card_ids in by_number.values():
            if len(card_ids) >= size:
                # Get all possible combinations of size cards
                results.extend(list(combo) for combo in combinations(sorted(card_ids), size))
        
        return results
    
    def find_runs(self, size=4):
        """Find runs of cards in the hand of a given size.
        Returns a list of lists containing card IDs that form runs."""
        results = []
        # Sort cards by number
        numbered_cards = [(c.number, c.id) for c in self.cards if c.number is not None]
        numbered_cards.sort()
        
        # No runs possible if we have fewer cards than size
        if len(numbered_cards) < size:
            return []
        
        # Try to find runs starting from each card
        for i in range(len(numbered_cards) - size + 1):
            potential_run = numbered_cards[i:i + size]
            # Check if numbers are sequential
            is_run = True
            for j in range(1, len(potential_run)):
                if potential_run[j][0] != potential_run[j-1][0] + 1:
                    is_run = False
                    break
            
            if is_run:
                results.append([card_id for _, card_id in potential_run])
        
        return results

    def __len__(self):
        """Return the number of cards in the hand."""
        return len(self.cards)
    
    def __getitem__(self, index):
        """Get a card by index."""
        if index < 0 or index >= len(self.cards):
            raise IndexError("Index out of range.")
        return self.cards[index] # Get card at index
    
    def __str__(self):
        """Return a string representation of the hand."""
        return ', '.join(str(card) for card in self.cards) if self.cards else "Empty Hand"
    
    def __repr__(self):
        """Return a detailed string representation of the hand."""
        return f"Hand({self.cards!r})"

