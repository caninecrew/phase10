class Card:
    _id_counter = 0

    def __init__(self, card_type, color=None, number=None):
        self.card_type = card_type
        self.color = color
        self.number = number
        self.id = Card._id_counter
        Card._id_counter += 1

    def __str__(self):
        if self.card_type == 'number':
            return f"{self.color.capitalize()} {self.number} (ID: {self.id})"
        elif self.card_type == 'skip':
            return f"Skip (ID: {self.id})"
        elif self.card_type == 'wild':
            return f'Wild (ID: {self.id})'
        else:
            return f"Unknown Card (ID: {self.id})"
        
    def __repr__(self):
        return f"Card({self.card_type!r}, color={self.color!r}, number={self.number!r}, id={self.id})"

    
