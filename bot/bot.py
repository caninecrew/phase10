from player import Player

class BotPlayer(Player):
    """A bot player that automatically plays its turn."""
    
    def __init__(self, name: str):
        """Initialize the bot player with a name."""
        super().__init__(name)
    
    def play_turn(self, game):
        """Automatically play the bot's turn."""
        # Example logic: always try to lay down a set or run if possible
        if self.can_lay_down():
            self.lay_down_best_set_or_run()
        else:
            self.draw_card(game.deck)
        
        # If the bot has laid down, it can also try to hit on other players' sets
        if self.has_laid_down:
            self.try_hit_on_other_players(game)
        
        # End the turn
        game.end_turn()
    
    def lay_down_best_set_or_run(self):
        """Lay down the best set or run available in hand."""
        best_set = self.find_best_set()
        if best_set:
            self.lay_down(best_set)
        else:
            best_run = self.find_best_run()
            if best_run:
                self.lay_down(best_run)

    def try_hit_on_other_players(self, game):
        """Attempt to hit on other players' sets."""
        for player in game.players:
            if player != self and player.has_laid_down:
                for laid_down_set in player.laid_down_sets:
                    card_to_hit = self.find_card_to_hit(laid_down_set)
                    if card_to_hit:
                        self.hit(card_to_hit, laid_down_set)