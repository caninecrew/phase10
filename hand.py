from card import Card
class Hand:
    def __init__(self):
        """Initialize an empty hand."""
        self.cards = []

    def add(self, card):
        """Add a card to the hand."""
        if not isinstance(card, Card):
            raise ValueError("Only Card instances can be added to the hand.")
        self.cards.append(card)

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
        self.cards.sort(key=lambda c: (c.color or 'zzz', c.number or 99)) # Sort by color, then by number

    def find_sets(self, size=3):
        """Find sets of cards in the hand of a given size.
        Returns a list of lists containing card IDs that form sets."""
        from collections import defaultdict
        sets = defaultdict(list)
        
        for card in self.cards:
            key = card.number  # Group by number only for sets
            sets[key].append(card.id)  # Store card ID instead of card object
        
        return [id_group for id_group in sets.values() if len(id_group) >= size]
    
    def find_runs(self, size=4):
        """Find runs of consecutive numbers in the hand regardless of color.
        Returns a list of lists containing card IDs that form runs."""
        from collections import defaultdict
        
        # Group cards by number to handle duplicates
        by_number = defaultdict(list)
        for card in self.cards:
            by_number[card.number].append(card.id)
            
        numbers = sorted(by_number.keys())
        runs = []
        
        # Look for consecutive sequences
        for i in range(len(numbers) - size + 1):
            potential_run = numbers[i:i + size]
            # Check if numbers are consecutive
            if all(potential_run[j+1] == potential_run[j] + 1 
                    for j in range(len(potential_run)-1)):
                # Take first card ID for each number in the run
                run_ids = [by_number[num][0] for num in potential_run]
                runs.append(run_ids)
            
        return runs

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
    
    