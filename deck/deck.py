from card.card import Card
class Deck:
    def __init__(self):
        self.cards = []
        self.discard_pile = []
        self.build_deck()
        self.shuffle()
    
    def build_deck(self):
        colors = ['red', 'green', 'blue', 'yellow']
        for color in colors:
            for number in range(1,13):
                self.cards.append(Card('number', color, number))
                self.cards.append(Card('number', color, number))
        
        for _ in range(4):
            self.cards.append(Card('skip'))
        
        for _ in range(8):
            self.cards.append(Card('wild'))
        
    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            self.reshuffle_discard()
        return self.cards.pop() if self.cards else None
    
    def reshuffle_discard(self):
        if len(self.discard_pile) <= 1:
            return # Leave the last card in the discard pile
        top_card = self.discard_pile.pop()
        self.cards = self.discard_pile # Take all but the last card from discard pile
        self.discard_pile = [top_card] # Leave one on discard pile
        self.shuffle()

    def discard(self, card):
        self.discard_pile.append(card)

    def draw_card(self):
        """Draw a card from the deck. If the deck is empty, reshuffle the discard pile."""
        if not self.cards:
            if not self.discard_pile:
                raise ValueError("No cards left to draw.")
            self.cards = self.discard_pile
            self.discard_pile = []
            self.shuffle()
        return self.cards.pop()

    def take_from_discard(self):
        """Take the top card from the discard pile."""
        if self.discard_pile:
            return self.discard_pile.pop()
        return None

