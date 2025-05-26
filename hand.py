class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return card
        return None
    
    def play(self, index):
        if 0 <= index < len(self.cards):
            return self.cards.pop(index)
        return None
    
    def sort(self):
        self.cards.sort(key=lambda c: (c.color or 'zzz', c.number or 99)) # Sort by color, then by number

    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index] # Get card at index
    
    def __str__(self):
        return ', '.join(str(card) for card in self.cards) if self.cards else "Empty Hand"
    
    def __repr__(self):
        return f"Hand({self.cards!r})"
    
    