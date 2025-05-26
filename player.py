from hand import Hand

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.current_phase = 1
        self.has_laid_down = False
        self.laid_down_sets = []

    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.add(card)
        return card

    def discard_card(self, deck, index):
        card = self.hand.play(index)
        if card:
            deck.discard(card)
        return card

    def lay_down(self, groups):
        """
        Attempt to lay down this phase with specified groups of cards.
        groups: list of lists of Card objects.
        """
        if self.has_laid_down:
            print(f"{self.name} has already laid down this round.")
            return False

        if self.validate_phase(groups):
            for group in groups:
                for card in group:
                    self.hand.remove(card)
                self.laid_down_sets.append(group)
            self.has_laid_down = True
            print(f"{self.name} laid down Phase {self.current_phase}!")
            return True

        print(f"{self.name} attempted to lay down an invalid phase.")
        return False

    def validate_phase(self, groups):
        """Simplified: only phase 1 = two sets of 3. Expand later."""
        if self.current_phase == 1:
            return self._validate_sets(groups, [3, 3])
        return False  # Placeholder for later phases

    def _validate_sets(self, groups, required_sizes):
        if len(groups) != len(required_sizes):
            return False
        for group, size in zip(groups, required_sizes):
            if len(group) != size:
                return False
            numbers = [c.number for c in group if c.card_type == 'number']
            if not numbers:
                return False
            num_set = set(numbers)
            wilds = sum(1 for c in group if c.card_type == 'wild')
            if len(num_set) > 1 and wilds == 0:
                return False
        return True

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")

    def show_laid_down(self):
        if not self.laid_down_sets:
            print(f"{self.name} has not laid down any cards.")
        else:
            for i, group in enumerate(self.laid_down_sets, 1):
                print(f"Group {i}: " + ', '.join(str(card) for card in group))
