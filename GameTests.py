# GameTests.py
# CS 261 Final
# Niraj

import unittest
from Game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        """Create a new game instance for testing."""
        self.game = Game(2)
        self.board = self.game.board

    def testNewGame(self):
        """Test resetting the game."""
        self.game.board.addToken(1, 0)
        self.game.newGame()
        for column in self.game.board.board:
            self.assertTrue(all(slot is None for slot in column))
        self.assertEqual(self.game.currentPlayer, 0)

    def testGameEnd(self):
        """Test the end of the game when a win condition is met."""
        # Verify initial game state
        self.assertTrue(self.game.gameActive)
        self.assertIsNone(self.game.winner)
        for i in range(7):
            self.game.playerTurn(i % 2)
        # Verify game state after a win condition
        self.assertFalse(self.game.gameActive)
        self.assertEqual(self.game.winner, 1)

    def testNextPlayer(self):
        """Test switching to the next player."""
        self.assertEqual(self.game.currentPlayer, 0)
        self.game.nextPlayer()
        self.assertEqual(self.game.currentPlayer, 1)

    def testRollDice(self):
        """Test rolling the dice for multiplayer."""
        diceValue = self.game.rollDice()
        self.assertTrue(1 <= diceValue <= 6)

    def testAddPiece(self):
        """Test adding a piece to the board."""
        self.game._addPiece(0)
        self.assertEqual(self.game.board.board[0][0], 0)

    def testPlayerTurn(self):
        """Test the flow of a player's turn."""
        self.game.playerTurn(0)
        self.assertEqual(self.game.board.board[0][0], 0)
        self.assertEqual(self.game.currentPlayer, 1)


    def testGameStartTwoPlayer(self):
        """Test game initialization with two players."""
        self.assertEqual(self.game.players, [0, 1])  # Ensure players are correctly set
        self.assertEqual(self.game.currentPlayer, 0)  # Verify the first player is active
        self.assertTrue(self.game.gameActive)  # Check if the game is active
        self.assertIsNone(self.game.winner)  # Confirm no winner at the start

    def testGameStartMultiPlayers(self):
        """Test game initialization with multiple players."""
        # Test with three players
        self.gameThreePlayer = Game(3)
        self.assertEqual(self.gameThreePlayer.players, [0, 1, 2])  # Verify three players
        self.assertEqual(self.gameThreePlayer.currentPlayer, 0)  # First player starts
        self.assertTrue(self.gameThreePlayer.multiPlayer)  # Confirm multiplayer mode