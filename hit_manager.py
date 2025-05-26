from phase_validator import PhaseValidator

class HitManager:
    @staticmethod
    def try_hit(source_player, target_player, set_idx, card):
        """Attempt to hit a card on another player's laid down set.
        
        Args:
            source_player (Player): Player attempting to hit
            target_player (Player): Player whose set is being hit on
            set_idx (int): Index of the set being hit on
            card (Card): Card being played
            
        Returns:
            bool: True if hit was successful, False otherwise
        """
        if set_idx >= len(target_player.laid_down_sets):
            return False
            
        target_set = target_player.laid_down_sets[set_idx]
        if card not in source_player.hand.cards:
            return False

        # Validate the hit
        test_set = target_set + [card]
        if not PhaseValidator._validate_set(test_set) and not PhaseValidator._validate_run(test_set):
            return False

        # Execute the hit
        target_set.append(card)
        source_player.hand.remove(card)
        return True
