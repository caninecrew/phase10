class PhaseValidator:
    PHASE_REQUIREMENTS = {
        1: [('set', 3), ('set', 3)],               # Two sets of 3
        2: [('set', 3), ('run', 4)],               # One set of 3 + one run of 4
        3: [('set', 4), ('run', 4)],               # One set of 4 + one run of 4
        4: [('run', 7)],                           # Run of 7
        5: [('run', 8)],                           # Run of 8
        6: [('run', 9)],                           # Run of 9
        7: [('set', 4), ('set', 4)],               # Two sets of 4
        8: [('color', 7)],                         # 7 cards of one color
        9: [('set', 5), ('set', 2)],               # One set of 5 + one set of 2
        10: [('set', 5), ('set', 3)]               # One set of 5 + one set of 3
    }

    @classmethod
    def validate_phase(cls, phase_num, groups):
        """Validate if the groups satisfy the requirements for the given phase."""
        requirements = cls.PHASE_REQUIREMENTS[phase_num]
        
        if len(groups) != len(requirements):
            return False

        for group, (req_type, req_size) in zip(groups, requirements):
            if len(group) != req_size:
                return False

            if req_type == 'set':
                if not cls._validate_set(group):
                    return False
            elif req_type == 'run':
                if not cls._validate_run(group):
                    return False
            elif req_type == 'color':
                if not cls._validate_color(group):
                    return False

        return True

    @staticmethod
    def _validate_set(cards):
        """Validate that cards form a set (same number)."""
        number_cards = [c for c in cards if c.card_type == 'number']
        if not number_cards:
            return False
        
        wilds = sum(1 for c in cards if c.card_type == 'wild')
        different_numbers = len(set(c.number for c in number_cards))
        
        return different_numbers + wilds == 1

    @staticmethod
    def _validate_run(cards):
        """Validate that cards form a run (consecutive numbers)."""
        number_cards = [c for c in cards if c.card_type == 'number']
        wilds = [c for c in cards if c.card_type == 'wild']
        
        if not number_cards:
            return False

        numbers = sorted(c.number for c in number_cards)
        wild_count = len(wilds)
        gaps = 0

        for i in range(len(numbers) - 1):
            gaps += numbers[i + 1] - numbers[i] - 1

        return gaps <= wild_count

    @staticmethod
    def _validate_color(cards):
        """Validate that cards are all the same color."""
        number_cards = [c for c in cards if c.card_type == 'number']
        if not number_cards:
            return False
        
        wilds = sum(1 for c in cards if c.card_type == 'wild')
        different_colors = len(set(c.color for c in number_cards))
        
        return different_colors + wilds == 1
