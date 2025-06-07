#!/usr/bin/env python3
"""
Single Player Mode for Phase 10 Card Game
Human player vs 3 bot players
"""

from game.game import Game
from player.player import Player
from bot.bot import BotPlayer


class SinglePlayerGame:
    def __init__(self):
        self.game = None
        self.human_player = None
        
    def start_game(self):
        """Start a new single player game."""
        print("=" * 60)
        print("Welcome to Phase 10 - Single Player Mode!")
        print("=" * 60)
        
        # Get player name
        player_name = input("Enter your name: ").strip()
        if not player_name:
            player_name = "Player"
            
        # Create players
        self.human_player = Player(player_name)
        bot1 = BotPlayer("Bot Alice")
        bot2 = BotPlayer("Bot Bob") 
        bot3 = BotPlayer("Bot Charlie")
        
        players = [self.human_player, bot1, bot2, bot3]
        
        # Create and start game
        self.game = Game(players)
        
        print(f"\nStarting game with {len(players)} players:")
        for i, player in enumerate(players, 1):
            print(f"  {i}. {player.name}")
        
        self.play_game()
    
    def play_game(self):
        """Main game loop."""
        round_num = 1
        
        while not self.game.is_game_over():
            print(f"\n{'='*60}")
            print(f"ROUND {round_num}")
            print(f"{'='*60}")
            
            # Show current phases
            self.show_player_phases()
            
            # Play the round
            self.play_round()
            
            # Check if game is over
            if self.game.is_game_over():
                break
                
            round_num += 1
            
        self.show_final_results()
    
    def play_round(self):
        """Play a single round."""
        self.game.start_new_round()
        
        while not self.game.is_round_over():
            current_player = self.game.get_current_player()
            
            print(f"\n{'-'*40}")
            print(f"{current_player.name}'s turn")
            print(f"{'-'*40}")
            
            if current_player == self.human_player:
                self.play_human_turn()
            else:
                self.play_bot_turn(current_player)
                
            if self.game.is_round_over():
                break
                
            self.game.end_turn()
        
        # Round is over, show results
        self.show_round_results()
    
    def play_human_turn(self):
        """Handle human player's turn."""
        player = self.human_player
        
        # Show game state
        self.show_game_state()
        
        # Show hand before drawing
        self.show_hand(player)
        
        # Draw phase
        self.handle_draw_phase(player)
        
        # Show updated hand
        self.show_hand(player)
        
        # Phase laying and hitting phase
        self.handle_phase_and_hitting(player)
        
        # Discard phase
        self.handle_discard_phase(player)
    
    def handle_draw_phase(self, player):
        """Handle the draw phase for human player."""
        print(f"\nTop discard: {self.game.deck.discard_pile[-1] if self.game.deck.discard_pile else 'None'}")
        
        while True:
            choice = input("Draw from (d)eck or (p)ile? ").lower().strip()
            if choice in ['d', 'deck']:
                self.game.draw_from_deck(player)
                print("Drew from deck.")
                break
            elif choice in ['p', 'pile'] and self.game.deck.discard_pile:
                self.game.take_from_discard(player)
                print(f"Took {self.game.deck.discard_pile[-1]} from discard pile.")
                break
            elif choice in ['p', 'pile']:
                print("Discard pile is empty!")
            else:
                print("Invalid choice. Enter 'd' for deck or 'p' for pile.")
    
    def handle_phase_and_hitting(self, player):
        """Handle phase laying and hitting for human player."""
        if not player.has_laid_down_phase:
            if self.try_lay_down_phase(player):
                print("✓ Phase successfully laid down!")
                player.has_laid_down_phase = True
        
        # Try hitting on other players' sets
        self.try_hitting_on_sets(player)
    
    def try_lay_down_phase(self, player):
        """Try to lay down the current phase."""
        print(f"\nCurrent phase requirement: {player.get_phase_requirements()}")
        
        while True:
            choice = input("Try to lay down phase? (y/n): ").lower().strip()
            if choice in ['n', 'no']:
                return False
            elif choice in ['y', 'yes']:
                break
            else:
                print("Please enter 'y' or 'n'")
        
        # Show available sets and runs
        sets = player.hand.find_sets(3)
        runs = player.hand.find_runs(4)
        
        if not sets and not runs:
            print("No valid sets or runs found in your hand.")
            return False
        
        print("\nAvailable card groups:")
        all_groups = []
        
        if sets:
            print("Sets:")
            for i, card_set in enumerate(sets):
                print(f"  {len(all_groups) + 1}. Set: {', '.join(str(card) for card in card_set)}")
                all_groups.append(card_set)
        
        if runs:
            print("Runs:")
            for i, run in enumerate(runs):
                print(f"  {len(all_groups) + 1}. Run: {', '.join(str(card) for card in run)}")
                all_groups.append(run)
        
        # Let player select groups for their phase
        selected_groups = self.select_groups_for_phase(all_groups, player.current_phase)
        
        if selected_groups:
            success = player.lay_down(selected_groups)
            if success:
                return True
            else:
                print("Selected groups don't meet phase requirements.")
        
        return False
    
    def select_groups_for_phase(self, all_groups, phase):
        """Let player select card groups for their phase."""
        phase_requirements = {
            1: 2,  # 2 sets of 3
            2: 2,  # 1 set of 3 + 1 run of 4
            3: 2,  # 1 set of 4 + 1 run of 4
            4: 1,  # 1 run of 7
            5: 1,  # 1 run of 8
            6: 1,  # 1 run of 9
            7: 2,  # 2 sets of 4
            8: 1,  # 7 cards of one color
            9: 2,  # 1 set of 5 + 1 set of 2
            10: 2  # 1 set of 5 + 1 set of 3
        }
        
        required_groups = phase_requirements.get(phase, 1)
        selected = []
        
        print(f"\nSelect {required_groups} group(s) for Phase {phase}:")
        
        for _ in range(required_groups):
            if not all_groups:
                break
                
            while True:
                try:
                    choice = input(f"Select group {len(selected) + 1} (1-{len(all_groups)}, or 0 to cancel): ")
                    if choice == '0':
                        return []
                    
                    choice = int(choice) - 1
                    if 0 <= choice < len(all_groups):
                        selected.append(all_groups.pop(choice))
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(all_groups)}")
                except ValueError:
                    print("Please enter a valid number")
            
            # Show remaining groups
            if all_groups and len(selected) < required_groups:
                print("Remaining groups:")
                for i, group in enumerate(all_groups):
                    group_type = "Set" if len(set(card.number for card in group if card.card_type == 'number')) == 1 else "Run"
                    print(f"  {i + 1}. {group_type}: {', '.join(str(card) for card in group)}")
        
        return selected
    
    def try_hitting_on_sets(self, player):
        """Try hitting cards on other players' laid down sets."""
        # Find all laid down sets from other players
        available_sets = []
        for other_player in self.game.players:
            if other_player != player and other_player.has_laid_down_phase:
                for i, laid_set in enumerate(other_player.laid_down_sets):
                    available_sets.append((other_player, i, laid_set))
        
        if not available_sets:
            return
        
        while True:
            choice = input("Try to hit on other players' sets? (y/n): ").lower().strip()
            if choice in ['n', 'no']:
                break
            elif choice in ['y', 'yes']:
                self.select_and_hit_sets(player, available_sets)
                break
            else:
                print("Please enter 'y' or 'n'")
    
    def select_and_hit_sets(self, player, available_sets):
        """Let player select cards to hit on sets."""
        print("\nAvailable sets to hit on:")
        for i, (owner, set_idx, laid_set) in enumerate(available_sets):
            print(f"  {i + 1}. {owner.name}'s set: {', '.join(str(card) for card in laid_set.cards)}")
        
        self.show_hand(player)
        
        while True:
            try:
                set_choice = input(f"Select set to hit on (1-{len(available_sets)}, 0 to cancel): ")
                if set_choice == '0':
                    break
                
                set_choice = int(set_choice) - 1
                if 0 <= set_choice < len(available_sets):
                    owner, set_idx, laid_set = available_sets[set_choice]
                    
                    card_choice = input(f"Select card from hand (1-{len(player.hand.cards)}, 0 to cancel): ")
                    if card_choice == '0':
                        break
                    
                    card_choice = int(card_choice) - 1
                    if 0 <= card_choice < len(player.hand.cards):
                        card = player.hand.cards[card_choice]
                        
                        if self.game.hit_on_player_set(player, owner, set_idx, card):
                            print(f"✓ Successfully hit {card} on {owner.name}'s set!")
                        else:
                            print(f"✗ Cannot hit {card} on that set.")
                    else:
                        print("Invalid card selection")
                else:
                    print("Invalid set selection")
            except ValueError:
                print("Please enter a valid number")
    
    def handle_discard_phase(self, player):
        """Handle the discard phase for human player."""
        if len(player.hand.cards) == 0:
            print("Hand is empty - you win this round!")
            return
        
        print("\nSelect a card to discard:")
        self.show_hand(player)
        
        while True:
            try:
                choice = input(f"Select card to discard (1-{len(player.hand.cards)}): ")
                choice = int(choice) - 1
                
                if 0 <= choice < len(player.hand.cards):
                    card = player.hand.cards[choice]
                    self.game.discard_card(player, choice)
                    print(f"Discarded: {card}")
                    break
                else:
                    print(f"Please enter a number between 1 and {len(player.hand.cards)}")
            except ValueError:
                print("Please enter a valid number")
    
    def play_bot_turn(self, bot_player):
        """Handle bot player's turn."""
        print(f"{bot_player.name} is thinking...")
        
        # Bot plays automatically
        bot_player.play_turn(self.game)
        
        # Show what the bot did
        print(f"{bot_player.name} completed their turn.")
        print(f"Cards in hand: {len(bot_player.hand.cards)}")
        
        if bot_player.has_laid_down_phase:
            print(f"✓ {bot_player.name} has laid down Phase {bot_player.current_phase}")
    
    def show_game_state(self):
        """Show current game state."""
        print(f"\nGame State:")
        print(f"Deck: {len(self.game.deck.cards)} cards")
        print(f"Discard pile: {len(self.game.deck.discard_pile)} cards")
        if self.game.deck.discard_pile:
            print(f"Top discard: {self.game.deck.discard_pile[-1]}")
        
        print(f"\nOther players:")
        for player in self.game.players:
            if player != self.human_player:
                status = "✓ Laid down" if player.has_laid_down_phase else "Working on phase"
                print(f"  {player.name}: Phase {player.current_phase}, {len(player.hand.cards)} cards, {status}")
    
    def show_hand(self, player):
        """Show player's hand."""
        print(f"\nYour hand ({len(player.hand.cards)} cards):")
        for i, card in enumerate(player.hand.cards, 1):
            print(f"  {i}. {card}")
    
    def show_player_phases(self):
        """Show all players' current phases."""
        print("\nCurrent Phases:")
        for player in self.game.players:
            phase_req = player.get_phase_requirements()
            print(f"  {player.name}: Phase {player.current_phase} ({phase_req})")
    
    def show_round_results(self):
        """Show results at the end of a round."""
        print(f"\n{'='*60}")
        print("ROUND RESULTS")
        print(f"{'='*60}")
        
        # Calculate and show scores
        self.game.calculate_round_scores()
        
        for player in self.game.players:
            status = "✓ Advanced" if player.has_laid_down_phase and len(player.hand.cards) == 0 else "No advancement"
            print(f"{player.name}:")
            print(f"  Round Score: {player.round_score}")
            print(f"  Total Score: {player.total_score}")
            print(f"  Next Phase: {player.current_phase} ({status})")
            print()
        
        input("Press Enter to continue...")
    
    def show_final_results(self):
        """Show final game results."""
        print(f"\n{'='*60}")
        print("GAME OVER!")
        print(f"{'='*60}")
        
        # Sort players by score (lower is better)
        sorted_players = sorted(self.game.players, key=lambda p: p.total_score)
        
        print("Final Standings:")
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player.name}")
            print(f"   Phase Reached: {player.current_phase}")
            print(f"   Total Score: {player.total_score}")
            print()
        
        winner = sorted_players[0]
        if winner == self.human_player:
            print("🎉 Congratulations! You won! 🎉")
        else:
            print(f"🤖 {winner.name} wins this time!")
        
        print(f"\nThank you for playing Phase 10!")


def main():
    """Main function to start the single player game."""
    try:
        game = SinglePlayerGame()
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your game files and try again.")


if __name__ == "__main__":
    main()