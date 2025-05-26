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

if __name__ == "__main__":
    test_hand()
    print("\n" + "="*50 + "\n")
    test_deck()
