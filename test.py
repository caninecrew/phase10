import pytest
from deck import Deck
from card import Card
from hand import Hand
from game import Game
from phase_validator import PhaseValidator
from hit_manager import HitManager
from board import GameBoard
from player import Player

@pytest.mark.sets
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

@pytest.mark.runs
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

@pytest.mark.edge_cases
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

@pytest.mark.game
def test_game():
    """Test Game functionality"""
    print("\n🎮 Testing game functionality...")
    
    # Test game initialization
    print("\nTesting game initialization...")
    player_names = ["Player 1", "Player 2", "Player 3"]
    game = Game(player_names)
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
    
    print("✅ Game functionality tests passed!")

@pytest.mark.phase_validator
def test_phase_validator():
    """Test PhaseValidator functionality"""
    print("\n🎯 Testing phase validator...")
    
    # Test set validation
    print("\nTesting set validation...")
    set_with_wild = [
        Card('number', 'red', 5),
        Card('number', 'blue', 5),
        Card('wild', None, None)
    ]
    assert PhaseValidator._validate_set(set_with_wild), "Should accept set with wild card"
    
    # Test run validation
    print("\nTesting run validation...")
    run_with_wild = [
        Card('number', 'red', 3),
        Card('wild', None, None),
        Card('number', 'blue', 5),
        Card('number', 'green', 6)
    ]
    assert PhaseValidator._validate_run(run_with_wild), "Should accept run with wild card"
    
    # Test color validation
    print("\nTesting color validation...")
    color_with_wild = [
        Card('number', 'red', 3),
        Card('number', 'red', 4),
        Card('wild', None, None),
        Card('number', 'red', 6)
    ]
    assert PhaseValidator._validate_color_set(color_with_wild), "Should accept color set with wild card"
    
    # Test phase requirements
    print("\nTesting phase requirements...")
    for phase_num in range(1, 11):
        assert phase_num in PhaseValidator.PHASE_REQUIREMENTS, f"Phase {phase_num} should be defined"
    
    print("✅ Phase validator tests passed!")

def test_hit_manager():
    """Test HitManager functionality"""
    print("\n🎯 Testing hit manager...")
    
    # Set up players and cards
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    
    # Create a laid down set for player 2
    set_cards = [
        Card('number', 'red', 5),
        Card('number', 'blue', 5),
        Card('number', 'green', 5)
    ]
    player2.laid_down_sets.append(set_cards)
    
    # Give player 1 a matching card
    hit_card = Card('number', 'yellow', 5)
    player1.hand.add(hit_card)
    
    # Test valid hit
    print("\nTesting valid hit...")
    success = HitManager.try_hit(player1, player2, 0, hit_card)
    assert success, "Should accept valid hit"
    assert len(player2.laid_down_sets[0]) == 4, "Target set should have one more card"
    assert hit_card not in player1.hand.cards, "Card should be removed from source player's hand"
    
    # Test invalid hit (wrong number)
    print("\nTesting invalid hit...")
    wrong_card = Card('number', 'red', 6)
    player1.hand.add(wrong_card)
    success = HitManager.try_hit(player1, player2, 0, wrong_card)
    assert not success, "Should reject invalid hit"
    assert wrong_card in player1.hand.cards, "Card should remain in source player's hand"
    
    print("✅ Hit manager tests passed!")

def test_game_board():
    """Test GameBoard functionality"""
    print("\n🎮 Testing game board...")
    
    board = GameBoard()
    
    # Test adding sets
    print("\nTesting adding sets...")
    player_name = "Player 1"
    set1 = [Card('number', 'red', 5), Card('number', 'blue', 5), Card('number', 'green', 5)]
    set2 = [Card('number', 'red', 7), Card('number', 'blue', 7), Card('number', 'green', 7)]
    
    board.add_phase_set(player_name, set1)
    board.add_phase_set(player_name, set2)
    
    # Test getting sets
    print("\nTesting getting sets...")
    player_sets = board.get_sets(player_name)
    assert len(player_sets) == 2, "Should have two sets"
    assert len(player_sets[0]) == 3, "First set should have 3 cards"
    assert len(player_sets[1]) == 3, "Second set should have 3 cards"
    
    # Test board display
    print("\nTesting board display...")
    display = board.show()
    assert player_name in display, "Board display should include player name"
    assert "Set 1" in display, "Board display should show set numbers"
    assert "Set 2" in display, "Board display should show set numbers"
    
    print("✅ Game board tests passed!")

def test_all():
    """Run all tests"""
    print("🎮 Starting comprehensive tests...")
    
    try:
        test_sets()
        test_runs()
        test_edge_cases()
        test_game()
        test_phase_validator()
        test_hit_manager()
        test_game_board()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_all()
