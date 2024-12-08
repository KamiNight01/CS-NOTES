# BoardTests.py
# CS 261 Final
# Niraj

import unittest
from Board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        """Initialize a standard Connect 4 board for testing."""
        self.board = Board(7, 6)

    def testAddToken(self):
        """Test adding tokens to a column."""
        position = self.board.addToken(1, 0)
        self.assertEqual(position, 0)
        self.assertEqual(self.board.board[0][0], 1)

    def testIsColumnFull(self):
        """Test if a column is correctly marked as full."""
        for _ in range(6):
            self.board.addToken(1, 0)
        self.assertTrue(self.board.isColumnFull(0))
        self.assertFalse(self.board.isColumnFull(1))

    def testResetBoard(self):
        """Test if the board resets to its initial state."""
        self.board.addToken(1, 0)
        self.board.resetBoard()
        for column in self.board.board:
            self.assertTrue(all(slot is None for slot in column))

    def testReturnBoard(self):
        """Test returning the current board state."""
        self.board.addToken(1, 0)
        boardState = self.board.returnBoard()
        self.assertEqual(boardState[0][0], 1)

    def testSquareWin(self):
        """Test detecting a 2x2 square win."""
        self.board.addToken(1, 0)
        self.board.addToken(1, 1)
        self.board.addToken(1, 0)
        self.board.addToken(1, 1)
        self.assertEqual(self.board.squareWin(), 1)

    def testLineWin(self):
        """Test detecting vertical, horizontal, and diagonal line wins."""
        # Horizontal win
        for col in range(4):
            self.board.addToken(1, col)
        self.assertEqual(self.board.lineWin(), 1)

        # Reset for vertical win
        self.board.resetBoard()
        for _ in range(4):
            self.board.addToken(1, 0)
        self.assertEqual(self.board.lineWin(), 1)

        # Reset for diagonal win
        self.board.resetBoard()
        for i in range(4):
            for j in range(i):
                self.board.addToken(2, i)  # Fill with other tokens
            self.board.addToken(1, i)
        self.assertEqual(self.board.lineWin(), 1)


if __name__ == "__main__":
    unittest.main()
