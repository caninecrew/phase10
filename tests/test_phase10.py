import pytest
from card import Card
from deck import Deck
from hand import Hand
from game import Game
from phase_validator import PhaseValidator
from hit_manager import HitManager
from board import GameBoard
from player import Player

class TestCard:
    def test_card_creation(self):
        Card.reset_id_counter()
        card = Card('number', 'red', 5)
        assert card.card_type == 'number'
        assert card.color == 'red'
        assert card.number == 5
        assert card.id == 0

class TestHand:
    def test_sets(self):
        Card.reset_id_counter()
        hand = Hand()
        
        # Test basic set of 3
        hand.add(Card('number', 'red', 5))
        hand.add(Card('number', 'blue', 5))
        hand.add(Card('number', 'green', 5))
        sets = hand.find_sets(size=3)
        assert sets == [[0, 1, 2]], "Basic set of 3 test failed"
        
        # Test set of 4 split into sets of 3
        hand.add(Card('number', 'yellow', 5))
        sets = hand.find_sets(size=3)
        assert len(sets) == 1 and len(sets[0]) == 3, "Set of 4 should split into set of 3"
    
    def test_runs(self):
        Card.reset_id_counter()
        hand = Hand()
        
        # Test basic run of 4
        hand.add(Card('number', 'red', 3))
        hand.add(Card('number', 'blue', 4))
        hand.add(Card('number', 'green', 5))
        hand.add(Card('number', 'yellow', 6))
        runs = hand.find_runs(size=4)
        assert runs == [[0, 1, 2, 3]], "Basic run test failed"

class TestGame:
    def test_game_initialization(self):
        player_names = ["Player 1", "Player 2", "Player 3"]
        game = Game(player_names)
        assert len(game.players) == 3, "Should create correct number of players"
        assert all(len(p.hand) == 10 for p in game.players), "Each player should have 10 cards"

class TestPhaseValidator:
    def test_set_validation(self):
        set_with_wild = [
            Card('number', 'red', 5),
            Card('number', 'blue', 5),
            Card('wild', None, None)
        ]
        assert PhaseValidator._validate_set(set_with_wild), "Should accept set with wild card"