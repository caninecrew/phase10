from game.game import Game
from bot.bot import BotPlayer

def main():
    player_names = ["Human"]
    bot_count = 2  # Number of bots
    game = Game(player_names, bot_count)

    while not game.game_end:
        current_player = game.get_current_player()
        
        if isinstance(current_player, BotPlayer):
            print(f"{current_player.name}'s turn (Bot).")
            current_player.play_turn(game)
        else:
            print(f"{current_player.name}'s turn (Human).")
            print(f"Phase: {current_player.current_phase}")
            # Implement human player interaction here
            print("Your hand:", current_player.hand)
            action = input("Choose an action: (1) Draw from deck, (2) Draw from discard: ")
            if action == "1":
                current_player.draw_card(game.deck)
            elif action == "2":
                if game.deck.discard_pile:
                    card = game.deck.take_from_discard()
                    current_player.hand.add(card)
                else:
                    print("Discard pile is empty.")

            # Display the top card of the discard pile
            top_discard = game.get_top_discard()
            if top_discard:
                print(f"Top of discard pile: {top_discard}")
            else:
                print("Discard pile is empty.")

            # Placeholder for laying down sets/runs and hitting on other players
            discard_index = int(input("Choose a card index to discard: "))
            current_player.discard_card(game.deck, discard_index)

        game.next_player()

    print("Game over!")
    print("Final scores:", game.scores)

if __name__ == "__main__":
    main()
