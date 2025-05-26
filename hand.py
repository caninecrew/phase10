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
    
    