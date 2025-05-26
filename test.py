from deck import Deck
from card import Card
from hand import Hand

def test_sets():
    """Test various set combinations"""
    print("\n🎯 Testing set formations...")
    Card.reset_id_counter()  # Reset IDs for predictable testing
    hand = Hand()
    
    # Test basic set of 3
    print("\nTesting basic set of 3...")
    hand.add(Card('number', 'red', 5))    # ID: 0
    hand.add(Card('number', 'blue', 5))   # ID: 1
    hand.add(Card('number', 'green', 5))  # ID: 2
    sets = hand.find_sets(size=3)
    print(f"Found sets: {sets}")
    assert sets == [[0, 1, 2]], "Basic set of 3 test failed"
    
    # Test set of 4 split into sets of 3
    print("\nTesting set of 4...")
    hand.add(Card('number', 'yellow', 5)) # ID: 3
    sets = hand.find_sets(size=3)
    print(f"Found sets: {sets}")
    assert len(sets) == 1 and len(sets[0]) == 3, "Set of 4 should split into set of 3"
    
    # Test multiple sets
    print("\nTesting multiple sets...")
    hand.add(Card('number', 'red', 7))    # ID: 4
    hand.add(Card('number', 'blue', 7))   # ID: 5
    hand.add(Card('number', 'green', 7))  # ID: 6
    sets = hand.find_sets(size=3)
    print(f"Found sets: {sets}")
    assert len(sets) == 2, "Multiple sets test failed"
    
    # Test duplicate sets with same number
    print("\nTesting duplicate sets of same number...")
    Card.reset_id_counter()
    hand = Hand()
    # First set of three 5s
    hand.add(Card('number', 'red', 5))    # ID: 0
    hand.add(Card('number', 'blue', 5))   # ID: 1
    hand.add(Card('number', 'green', 5))  # ID: 2
    # Second set of three 5s
    hand.add(Card('number', 'yellow', 5)) # ID: 3
    hand.add(Card('number', 'red', 5))    # ID: 4
    hand.add(Card('number', 'blue', 5))   # ID: 5
    
    sets = hand.find_sets(size=3)
    print(f"Found sets: {sets}")
    assert len(sets) == 2, "Duplicate sets test failed"
    assert all(len(s) == 3 for s in sets), "Sets should have exactly 3 cards each"
    assert sets[0] != sets[1], "Sets should be different"

def test_runs():
    """Test various run combinations"""
    print("\n🏃 Testing run formations...")
    Card.reset_id_counter()  # Reset IDs for predictable testing
    hand = Hand()
    
    # Test basic run of 4
    print("\nTesting basic run of 4...")
    hand.add(Card('number', 'red', 3))    # ID: 0
    hand.add(Card('number', 'blue', 4))   # ID: 1
    hand.add(Card('number', 'green', 5))  # ID: 2
    hand.add(Card('number', 'yellow', 6)) # ID: 3
    runs = hand.find_runs(size=4)
    print(f"Found runs: {runs}")
    assert runs == [[0, 1, 2, 3]], "Basic run test failed"
    
    # Test run with duplicate numbers
    print("\nTesting run with duplicates...")
    Card.reset_id_counter()  # Reset IDs for new test
    hand = Hand()
    hand.add(Card('number', 'red', 3))    # ID: 0
    hand.add(Card('number', 'blue', 4))   # ID: 1
    hand.add(Card('number', 'red', 4))    # ID: 2
    hand.add(Card('number', 'green', 5))  # ID: 3
    hand.add(Card('number', 'yellow', 6)) # ID: 4
    runs = hand.find_runs(size=4)
    print(f"Found runs: {runs}")
    assert len(runs) >= 1, "Run with duplicates test failed"
    
    # Test overlapping runs
    print("\nTesting overlapping runs...")
    Card.reset_id_counter()  # Reset IDs for new test
    hand = Hand()
    hand.add(Card('number', 'red', 3))    # ID: 0
    hand.add(Card('number', 'blue', 4))   # ID: 1
    hand.add(Card('number', 'green', 5))  # ID: 2
    hand.add(Card('number', 'yellow', 6)) # ID: 3
    hand.add(Card('number', 'red', 7))    # ID: 4
    hand.add(Card('number', 'blue', 8))   # ID: 5

    runs = hand.find_runs(size=4)
    print(f"Found runs: {runs}")
    assert len(runs) == 3, "Should find 3 overlapping runs (3-6, 4-7, 5-8)"
    # Verify the runs are different
    assert len(set(tuple(run) for run in runs)) == 3, "All runs should be unique"
    # Verify each run is the correct size
    assert all(len(run) == 4 for run in runs), "All runs should have 4 cards"

def test_edge_cases():
    """Test edge cases and invalid combinations"""
    print("\n❌ Testing edge cases...")
    hand = Hand()
    
    # Test empty hand
    print("\nTesting empty hand...")
    sets = hand.find_sets(size=3)
    runs = hand.find_runs(size=4)
    assert len(sets) == 0, "Empty hand sets test failed"
    assert len(runs) == 0, "Empty hand runs test failed"
    
    # Test hand with gaps
    print("\nTesting hand with gaps...")
    hand.add(Card('number', 'red', 1))    # ID: 0
    hand.add(Card('number', 'blue', 2))   # ID: 1
    hand.add(Card('number', 'green', 4))  # ID: 2
    hand.add(Card('number', 'yellow', 5)) # ID: 3
    runs = hand.find_runs(size=4)
    assert len(runs) == 0, "Gaps in run test failed"

def test_hand():
    """Main test function"""
    print("🎮 Starting comprehensive hand tests...")
    
    try:
        test_sets()
        test_runs()
        test_edge_cases()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}")

def test_deck():
    print("🔄 Creating a new deck...")
    deck = Deck()

    print(f"✅ Total cards in deck: {len(deck.cards)} (Expected: 108)")
    print(f"🃏 Top 5 cards: {deck.cards[:5]}")
    
    print("\n🎯 Drawing 5 cards:")
    hand = [deck.draw() for _ in range(5)]
    for card in hand:
        print("  ➤", card)

    print(f"\n✅ Cards remaining in draw pile: {len(deck.cards)} (Expected: 103)")

    print("\n🗑️ Discarding all cards in hand...")
    for card in hand:
        deck.discard(card)
    
    print(f"✅ Discard pile size: {len(deck.discard_pile)} (Expected: 5)")

    print("\n💥 Emptying draw pile...")
    while deck.cards:
        deck.draw()
    print("✅ Draw pile empty!")

    print("\n🔁 Triggering reshuffle from discard pile...")
    deck.reshuffle_discard()
    print(f"✅ New draw pile: {len(deck.cards)}")
    print(f"✅ Remaining discard pile (should be 1): {len(deck.discard_pile)}")
    print(f"🃏 Top card in discard pile: {deck.discard_pile[0] if deck.discard_pile else 'None'}")

def test_laid_down_sets():
    """Test LaidDownSet functionality"""
    from laiddownset import LaidDownSet
    print("\n🎲 Testing laid down sets...")
    Card.reset_id_counter()
    
    # Test valid set creation
    print("\nTesting valid set creation...")
    set_cards = [
        Card('number', 'red', 5),
        Card('number', 'blue', 5),
        Card('number', 'green', 5)
    ]
    valid_set = LaidDownSet(set_cards, 'set')
    print(f"Created set: {valid_set}")
    assert len(valid_set) == 3, "Set should have 3 cards"
    
    # Test valid run creation
    print("\nTesting valid run creation...")
    run_cards = [
        Card('number', 'red', 3),
        Card('number', 'blue', 4),
        Card('number', 'green', 5),
        Card('number', 'yellow', 6)
    ]
    valid_run = LaidDownSet(run_cards, 'run')
    print(f"Created run: {valid_run}")
    assert len(valid_run) == 4, "Run should have 4 cards"
    
    # Test valid color set creation
    print("\nTesting valid color set creation...")
    color_cards = [
        Card('number', 'red', 3),
        Card('number', 'red', 5),
        Card('number', 'red', 7)
    ]
    valid_color = LaidDownSet(color_cards, 'color')
    print(f"Created color set: {valid_color}")
    assert len(valid_color) == 3, "Color set should have 3 cards"
    
    # Test invalid set creation
    print("\nTesting invalid set creation...")
    invalid_set_cards = [
        Card('number', 'red', 5),
        Card('number', 'blue', 6),
        Card('number', 'green', 5)
    ]
    try:
        invalid_set = LaidDownSet(invalid_set_cards, 'set')
        assert False, "Should raise ValueError for invalid set"
    except ValueError:
        print("✅ Correctly caught invalid set")
    
    # Test invalid run creation
    print("\nTesting invalid run creation...")
    invalid_run_cards = [
        Card('number', 'red', 3),
        Card('number', 'blue', 4),
        Card('number', 'green', 6),  # Gap in sequence
        Card('number', 'yellow', 7)
    ]
    try:
        invalid_run = LaidDownSet(invalid_run_cards, 'run')
        assert False, "Should raise ValueError for invalid run"
    except ValueError:
        print("✅ Correctly caught invalid run")
    
    # Test invalid color set creation
    print("\nTesting invalid color set creation...")
    invalid_color_cards = [
        Card('number', 'red', 3),
        Card('number', 'blue', 5),  # Different color
        Card('number', 'red', 7)
    ]
    try:
        invalid_color = LaidDownSet(invalid_color_cards, 'color')
        assert False, "Should raise ValueError for invalid color set"
    except ValueError:
        print("✅ Correctly caught invalid color set")
    
    # Test adding cards
    print("\nTesting adding cards...")
    set_cards = [
        Card('number', 'red', 5),
        Card('number', 'blue', 5)
    ]
    test_set = LaidDownSet(set_cards, 'set')
    test_set.add_card(Card('number', 'green', 5))
    assert len(test_set) == 3, "Set should have 3 cards after addition"
    
    # Test removing cards
    print("\nTesting removing cards...")
    removed = test_set.remove_card(set_cards[0])
    assert removed, "Card removal should return True"
    assert len(test_set) == 2, "Set should have 2 cards after removal"

def test_player():
    """Test Player functionality"""
    from player import Player
    print("\n👤 Testing player functionality...")
    Card.reset_id_counter()
    deck = Deck()
    
    # Test player creation
    print("\nTesting player creation...")
    player = Player("Test Player")
    assert player.name == "Test Player", "Player name not set correctly"
    assert player.current_phase == 1, "Initial phase should be 1"
    assert not player.has_laid_down, "Player should not start laid down"
    assert len(player.laid_down_sets) == 0, "Should start with no laid down sets"
    
    # Test drawing cards
    print("\nTesting drawing cards...")
    initial_hand_size = len(player.hand)
    player.draw_card(deck)
    assert len(player.hand) == initial_hand_size + 1, "Hand size should increase after drawing"
    
    # Test discarding cards
    print("\nTesting discarding cards...")
    player.draw_card(deck)  # Draw a card to ensure we have one
    initial_hand_size = len(player.hand)
    player.discard_card(deck, 0)  # Discard first card
    assert len(player.hand) == initial_hand_size - 1, "Hand size should decrease after discarding"
    assert len(deck.discard_pile) > 0, "Card should be in discard pile"
    
    # Test laying down valid phase 1 (two sets of 3)
    print("\nTesting laying down valid phase 1...")
    # Clear hand and add specific cards for phase 1
    player.hand.cards.clear()
    # First set of three 5s
    player.hand.add(Card('number', 'red', 5))
    player.hand.add(Card('number', 'blue', 5))
    player.hand.add(Card('number', 'green', 5))
    # Second set of three 7s
    player.hand.add(Card('number', 'red', 7))
    player.hand.add(Card('number', 'blue', 7))
    player.hand.add(Card('number', 'green', 7))
    
    # Create groups for laying down
    set1 = [c for c in player.hand.cards if c.number == 5]
    set2 = [c for c in player.hand.cards if c.number == 7]
    success = player.lay_down([set1, set2])
    assert success, "Valid phase 1 should be accepted"
    assert player.has_laid_down, "Player should be marked as laid down"
    assert len(player.laid_down_sets) == 2, "Should have 2 sets laid down"
    
    # Test laying down invalid phase
    print("\nTesting laying down invalid phase...")
    player = Player("Test Player 2")  # New player since previous one laid down
    # Add mixed cards that don't form valid sets
    player.hand.add(Card('number', 'red', 5))
    player.hand.add(Card('number', 'blue', 6))
    player.hand.add(Card('number', 'green', 7))
    player.hand.add(Card('number', 'red', 8))
    invalid_set = player.hand.cards
    success = player.lay_down([invalid_set])
    assert not success, "Invalid phase should be rejected"
    assert not player.has_laid_down, "Player should not be marked as laid down"
    assert len(player.laid_down_sets) == 0, "Should have no sets laid down"
    
    # Test laying down with wild cards
    print("\nTesting laying down with wild cards...")
    player = Player("Test Player 3")
    player.hand.add(Card('number', 'red', 5))
    player.hand.add(Card('number', 'blue', 5))
    player.hand.add(Card('wild', None, None))  # Wild card completing set
    player.hand.add(Card('number', 'red', 7))
    player.hand.add(Card('number', 'blue', 7))
    player.hand.add(Card('wild', None, None))  # Wild card completing set
    
    set1 = player.hand.cards[:3]  # First set with wild
    set2 = player.hand.cards[3:]  # Second set with wild
    success = player.lay_down([set1, set2])
    assert success, "Valid phase with wild cards should be accepted"
    assert player.has_laid_down, "Player should be marked as laid down"
    assert len(player.laid_down_sets) == 2, "Should have 2 sets laid down"

def test_gameboard():
    """Test GameBoard functionality"""
    from gameboard import GameBoard
    print("\n🎮 Testing game board functionality...")
    
    # Test game initialization
    print("\nTesting game initialization...")
    player_names = ["Player 1", "Player 2", "Player 3"]
    game = GameBoard(player_names)
    assert len(game.players) == 3, "Should create correct number of players"
    assert all(len(p.hand) == 10 for p in game.players), "Each player should have 10 cards"
    
    # Test phase validation
    print("\nTesting phase validation...")
    player = game.get_current_player()
    # Create a valid phase 1 (two sets of 3)
    set1 = [Card('number', 'red', 5), Card('number', 'blue', 5), Card('number', 'green', 5)]
    set2 = [Card('number', 'red', 7), Card('number', 'blue', 7), Card('number', 'green', 7)]
    assert game.validate_phase(player, [set1, set2]), "Should accept valid phase 1"
    
    # Test invalid phase
    print("\nTesting invalid phase validation...")
    invalid_set = [Card('number', 'red', 5), Card('number', 'blue', 6), Card('number', 'green', 7)]
    assert not game.validate_phase(player, [invalid_set]), "Should reject invalid phase"
    
    # Test turn execution
    print("\nTesting turn execution...")
    initial_hand_size = len(player.hand)
    success = game.play_turn(draw_from_discard=False, discard_index=0)
    assert success, "Turn should execute successfully"
    assert len(player.hand) == initial_hand_size, "Hand size should remain same after draw and discard"
    assert game.get_current_player() != player, "Should move to next player"
    
    # Test round scoring
    print("\nTesting round scoring...")
    game.calculate_round_scores()
    assert all(score >= 0 for score in game.scores.values()), "Scores should be non-negative"
    
    # Test game state
    print("\nTesting game state retrieval...")
    state = game.get_game_state()
    assert 'current_player' in state, "Game state should include current player"
    assert 'scores' in state, "Game state should include scores"
    assert 'players' in state, "Game state should include player info"
    
    # Test wild card validation
    print("\nTesting wild card usage...")
    set_with_wild = [
        Card('number', 'red', 5),
        Card('number', 'blue', 5),
        Card('wild', None, None)
    ]
    assert game._validate_set(set_with_wild), "Should accept set with wild card"
    
    run_with_wild = [
        Card('number', 'red', 3),
        Card('wild', None, None),
        Card('number', 'blue', 5),
        Card('number', 'green', 6)
    ]
    assert game._validate_run(run_with_wild), "Should accept run with wild card"
    
    color_with_wild = [
        Card('number', 'red', 3),
        Card('number', 'red', 5),
        Card('wild', None, None)
    ]
    assert game._validate_color(color_with_wild), "Should accept color set with wild card"
    
    print("✅ GameBoard tests passed!")

# Add gameboard test to test_all function
def test_all():
    """Run all tests"""
    print("🎮 Starting comprehensive tests...")
    
    try:
        test_sets()
        test_runs()
        test_edge_cases()
        test_laid_down_sets()
        test_player()
        test_gameboard()  # Add gameboard test
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}")
        
if __name__ == "__main__":
    test_all()
    print("\n" + "="*50 + "\n")
    test_deck()
