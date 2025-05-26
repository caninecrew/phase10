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
            for _ in range(8):
                self.cards.append(Card('skip', color))
            for _ in range(4):
                self.cards.append(Card('wild', color))

class Card:
    _id_counter = 0

    def __init__(self, card_type, color, number=None):
        self.card_type = card_type
        self.color = color
        self.number = number
        self.id = Card._id_counter
        Card._id_counter += 1

    def __str__(self):
        if self.card_type == 'number':
            return f"{self.color.capitalize()} {self.number} (ID: {self.id})"
        elif self.card_type == 'skip':
            return f"{self.color.capitalize()} Skip (ID: {self.id})"
        elif self.card_type == 'wild':
            return f'{self.color.capitalize()} Wild (ID: {self.id})'
        else:
            return f"Unknown Card (ID: {self.id})"
        
    def __repr__(self):
        return f"Card({self.card_type!r}, color={self.color!r}, number={self.number!r}, id={self.id})"

    
