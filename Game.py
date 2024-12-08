# Game.py
#CS-261  Final
#Niraj

from Board import *
import random
class Game:
    """
    A class to manage the logic and flow of the Connect 4 War game.

    Attributes:
        colors (list[int]): A class-level list representing all possible integer representations of player colors.
        players (list[int]): The list of players currently in the game, assigned from the `colors` list.
        currentPlayer (int): The player currently taking their turn, represented by an integer.
        multiPlayer (bool): Indicates whether the game involves more than two players.
        board (Board): The game board instance used for managing the Connect 4 grid.
        winner (Optional[int]): The identifier of the winning player, or None if no winner yet.
        isDraw (bool): Indicates if the game has ended in a draw.
        gameActive (bool): A flag indicating if the game is still ongoing.
    """
    colors = [0, 1, 2, 3, 4, 5]

    def __init__(self, numPlayers: int) -> None:
        """
        Initialize a new game instance.

        :param numPlayers: The number of players in the game (must be between 2 and 6).
        """
        #intiualze the winner and draw flag and sets them to None and false respectively
        self.winner = None
        self.isDraw = False

        # Assign players based on the number of players,
        # checks if there are more than 2 player and
        # sets the first player to start the game
        self.players = Game.colors[0:numPlayers]
        self.multiPlayer = numPlayers > 2
        self.currentPlayer = self.players[0]

        # Create a new board with 7 columns and 6 rows
        self.board = Board(7, 6)

        # Set game as active
        self.gameActive = True

    def newGame(self) -> None:
        """
        Reset the game to its initial state.

        This method clears the board, sets the first player as the current player,
        and resets all game-related flags, including the active state, winner, and draw status.

        :return: None
        """
        self.board.resetBoard()
        self.currentPlayer = self.players[0]
        self.gameActive = True
        self.winner = None
        self.isDraw = False


    def nextPlayer(self) -> None:
        """
        Move to the next player's turn.
        """
        currentIndex = (self.players.index(self.currentPlayer) + 1) % len(self.players)
        self.currentPlayer = self.players[currentIndex]


    def rollDice(self) -> int:
        """
        Roll a die (1-6) if more than two players; otherwise, return 3.
        """
        return random.randint(1, 6) if self.multiPlayer else 3


    def _addPiece(self, column: int) -> None:
        """
        Add the current player's piece to the board.
        This method attempts to place the current player's token in the specified column.
        If the column is already full, an IndexError is raised.
        :param column: The index of the column where the token will be placed (0-based).
        :raises IndexError: If the specified column is full.
        :return: None
        """
        if self.board.isColumnFull(column):
            raise IndexError("Invalid column")
        self.board.addToken(self.currentPlayer, column)

    def playerTurn(self, column: int) -> None:
        """
        Complete the current player's turn.

        This method places the current player's piece in the specified column, checks for
        win conditions (line or square wins), and determines if the game is a draw.
        If the game continues, it moves to the next player's turn.

        :param column: The index of the column where the current player wants to place their piece (0-based).
        :return: None
        """
        """
        Complete the current player's turn and check for win conditions
        """
        self._addPiece(column)
        winner = None

        # Check win conditions after the player's turn
        if self.board.lineWin() is not None:
            winner = self.board.lineWin()
        if self.board.squareWin() is not None:
            winner = self.board.squareWin()

        # Check for a draw after the player's turn
        counter = 0
        for column in range(self.board.columns):
            if not self.board.isColumnFull(column):
                break
            counter += 1

        if counter == 7:
            self.gameActive = False
            self.isDraw = True
            self.winner = -1

        # Check if there is a winner; if so, update the winner and end the game.
        # Otherwise, switch to the next player.
        if winner is None:
            self.nextPlayer()
        else:
            self.winner = winner + 1
            self.gameActive = False

