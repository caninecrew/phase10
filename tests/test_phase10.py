import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from phase10.card import Card
from phase10.deck import Deck
from phase10.hand import Hand
from phase10.game import Game
from phase10.phase_validator import PhaseValidator
from phase10.hit_manager import HitManager
from phase10.board import GameBoard
from phase10.player import Player

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
        hand.add(Card('number', 'red', 5))       # ID: 0
        hand.add(Card('number', 'blue', 5))      # ID: 1
        hand.add(Card('number', 'green', 5))     # ID: 2
        sets = hand.find_sets(size=3)
        assert sets == [[0, 1, 2]], "Basic set of 3 test failed"
        
        # Test set of 4 generating all possible sets of 3
        hand.add(Card('number', 'yellow', 5))    # ID: 3
        sets = hand.find_sets(size=3)
        expected = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
        assert len(sets) == 4, "Set of 4 should generate 4 possible sets of 3"
        assert all(s in expected for s in sets), "All possible combinations should be present"
        
        # Test multiple sets of different numbers
        hand.add(Card('number', 'red', 7))       # ID: 4
        hand.add(Card('number', 'blue', 7))      # ID: 5
        hand.add(Card('number', 'green', 7))     # ID: 6
        sets = hand.find_sets(size=3)
        assert len(sets) == 5, "Should find sets from both 5s and 7s"
        assert [4, 5, 6] in sets, "Should find the set of 7s"
    
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