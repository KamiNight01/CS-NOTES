# Board.py
#CS-261  Final
#Niraj

from typing import Optional

class Board:
    """
    class that represents the game board;check win conditions.
    Attributes:
        baord: A 2D list to store tokens on the board.
        width: Number of columns on the board.
        height: Number of rows on the board.
    """
    def __init__(self, width: int, height: int):
        """
           Initializes the board with empty slots represented by None.
        """
        self.columns = width
        self.rows = height
        self.board = [[None for _ in range(height)] for _ in range(width)]

    def addToken(self, color: int, columnNumber: int) -> int:
        """
        :param color: the int representing the color of the token.
        :param columnNumber: the column number of the token
        :return: the postion of the token on the board.
        """
        position = self.board[columnNumber].index(None)
        self.board[columnNumber][position] = color
        return position

    def isColumnFull(self, columnNumber: int) -> bool:
        """
        cehck if the column is full.
        :param columnNumber: the column number of the token to be checked
        :return:
        """
        return None not in self.board[columnNumber]

    def resetBoard(self) -> None:
        """
        Resets the board to their initial state.
        :return:
        """
        # Reset every position on the board to None
        self.board = [[None for _ in range(self.rows)] for _ in range(self.columns)]

    def returnBoard(self) -> list[list[Optional[int]]]:
        """
        Returns the boards current state
        :return:
        """
        return self.board

    def squareWin(self) -> Optional[int]:
        """
        Check if any player has achieved a 2x2 square victory.
        If a player wins, their identifier (int) is returned; otherwise, None is returned.
        :return: The int of the winning player, or None if no winner is found.
        """
        #   check the board to locate a possible 2x2 square
        for col in range(self.columns - 1):
            for row in range(self.rows - 1):
                # Ensure all cells in the 2x2 square are occupied by the same player
                current_player = self.board[col][row]
                if current_player is not None:
                    if (current_player == self.board[col + 1][row] and
                            current_player == self.board[col][row + 1] and
                            current_player == self.board[col + 1][row + 1]):
                        return current_player

        # No winning square found
        return None

    def lineWin(self) -> Optional[int]:
        """
        Check if any player has a 4 in a row win horizontally.
        check if any player has a 4 in a row win vertically.
        check if any player has a 4 in a column win diagonally.
        :return: the int of the winning player, or None if no winner is found.
        """
        # Check for vertical wins
        for col in range(self.columns):
            for row in range(self.rows - 3):
                if self.board[col][row] is not None:
                    if (self.board[col][row] == self.board[col][row + 1] ==
                            self.board[col][row + 2] == self.board[col][row + 3]):
                        return self.board[col][row]

        # Check for horizontal wins
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if self.board[col][row] is not None:
                    if (self.board[col][row] == self.board[col + 1][row] ==
                            self.board[col + 2][row] == self.board[col + 3][row]):
                        return self.board[col][row]

        # Check for diagonal wins (bottom-left to top-right)
        for col in range(self.columns - 3):
            for row in range(self.rows - 3):
                if self.board[col][row] is not None:
                    if (self.board[col][row] == self.board[col + 1][row + 1] ==
                            self.board[col + 2][row + 2] == self.board[col + 3][row + 3]):
                        return self.board[col][row]

        # Check for diagonal wins (top-left to bottom-right)
        for col in range(self.columns - 3):
            for row in range(3, self.rows):
                if self.board[col][row] is not None:
                    if (self.board[col][row] == self.board[col + 1][row - 1] ==
                            self.board[col + 2][row - 2] == self.board[col + 3][row - 3]):
                        return self.board[col][row]

        # Return None if no winner is found
        return None

