from deck import Deck
from card import Card

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

test_deck()
