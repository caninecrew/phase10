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
        # Check if target has laid down any sets
        if not target_player.has_laid_down or set_idx >= len(target_player.laid_down_sets):
            return False
            
        # Check if source player has the card
        if card not in source_player.hand.cards:
            return False
        
        target_set = target_player.laid_down_sets[set_idx].copy()
        target_set.append(card)
        
        # First try to validate as a set
        if PhaseValidator._validate_set(target_set):
            source_player.hand.remove(card)
            target_player.laid_down_sets[set_idx] = target_set
            return True
        
        # Then try to validate as a run
        if PhaseValidator._validate_run(target_set):
            source_player.hand.remove(card)
            target_player.laid_down_sets[set_idx] = target_set
            return True
        
        # If we can't hit on this set, return False
        return False
