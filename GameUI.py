# GameUI.py
#CS -270 Finals
#Niraj
from Game import*
from graphics import*

class GameUI:
    """
      the user interface for the Connect 4 War game.
     This interface supports 2-6 players and provides graphical elements
     like the game board, die button, new game button, and winner label.
     Attributes:
     game (Game): The game logic instance.
     board (Board): The game board instance.
     win (GraphWin): The main game window.
     die (Rectangle): The die button for rolling a die.
     dieLabel (Text): Label displaying the current die value.
     newGameButton (Rectangle): Button to start a new game.
     newGameText (Text): Text displayed on the new game button.
     winner (Text): Label to display the winner of the game.
     """
    def __init__(self, numPlayers) -> None:
        """
         Initialize the user interface for a Connect 4 War game.

         :param numPlayers: The number of players in the game (2-6).
         """
        self.game = Game(numPlayers)
        self.board = self.game.board

        # Initialize the main game window with a black background
        self.win = GraphWin("ConnectWarGame", 600, 800)
        self.win.setBackground("Black")


        # Winner Label
        self.winner = Text(Point(300, 130), "")
        self.winner.setSize(30)
        self.winner.setFill("red")

        # Create die button
        self.die = Rectangle(Point(500, 100), Point(580, 20))
        self.dieLabel = Text(self.die.getCenter(), "1")

        # New Game Button
        self.newGameButton = Rectangle(Point(20, 20), Point(140, 80))
        self.newGameButton.setFill("Red")
        self.newGameText = Text(Point(80, 50), "New Game")
        self.newGameText.setFill("White")

        # Create the display and start the game
        self.displayBoard()
        self.updateActivePlayer()
        self.colButtonsOff()
        self.gameOrder()

    def displayBoard(self) -> None:
        """
        draw the board on the screen with slots and dice icon if theres more than 2 players
        :return:none
        """
        # Create the board
        board = Rectangle(Point(20, 230), Point(580, 730))
        board.setFill("cyan")
        board.draw(self.win)

        # Draw the slots on the board
        slotRadius = 35
        xStart, yStart = 60, 280
        spacing = 80
        for row in range(6):
            for col in range(7):
                slotCenter = Point(xStart + col * spacing, yStart + row * spacing)
                slot = Circle(slotCenter, slotRadius)
                slot.setFill("white")
                slot.draw(self.win)


        # Draw the dice if more than two players are present
        if self.game.multiPlayer:
            self.die.setFill("red3")
            self.die.draw(self.win)

            self.dieLabel.setFill("white")
            self.dieLabel.setSize(25)
            self.dieLabel.draw(self.win)

    def addToken(self, player: int, column: int) -> None:
        """
        Adds a token to the board and displays it on the screen.
        :param player: The player placing the token.
        :param column: The column where the token is being added.
        """
        if not self.board.isColumnFull(column):
            # Find the first empty row in the column and update the game state for the players turn
            row = self.board.board[column].index(None)
            self.game.playerTurn(column)

            # Calculate token position and draw it
            tokenPosition = Point(60 + column * 80, 280 + (self.board.rows - row - 1) * 80)
            token = Circle(tokenPosition, 35)
            token.setFill(self._colorFromInt(player))
            token.draw(self.win)

            # Deactivate column buttons unless the dice rolled a 6
            if self.dieLabel.getText() != "6":
                self.colButtonsOff()

    def gameOrder(self):

        """
        controls the flow of the game, handles player turn and game logic.
        :return:none
        """

        while True:
            # Handle dice roll if more than two players
            if self.game.multiPlayer:
                self.diceButtonOn()
                while True:
                    click = self.win.getMouse()
                    x, y = click.getX(), click.getY()
                    if 500 <= x <= 580 and 20 <= y <= 100:
                        dieResult = self.diceButtonPressed()
                        break
            else:
                dieResult = 2

            # Handle player actions based on dice result
            if dieResult == 1:  # Skip turn
                self.game.nextPlayer()
            elif dieResult == 6:  # Player places two tokens
                self.colButtonsOn()
                tokensPlaced = 0
                currentPlayer = self.game.currentPlayer
                while tokensPlaced < 2 and not self.game.winner:
                    self.game.currentPlayer = currentPlayer
                    click = self.win.getMouse()
                    x, y = int(click.getX()), int(click.getY())
                    if 60 <= x <= 620 and 155 <= y <= 225:
                        self.addToken(currentPlayer, (x - 20) // 80)
                        tokensPlaced += 1
                self.colButtonsOff()  # Disable buttons after turn
            else:  # Player places one token
                self.colButtonsOn()
                while True:
                    click = self.win.getMouse()
                    x, y = int(click.getX()), int(click.getY())
                    if 60 <= x <= 620 and 155 <= y <= 225:
                        self.addToken(self.game.currentPlayer, (x - 20) // 80)
                        break

            # Update the active player and check for game results
            self.updateActivePlayer()

            if not self.game.gameActive:
                self.displayResult()
                self.newGameButton.draw(self.win)
                self.newGameText.draw(self.win)

                # Wait for user to start a new game
                while True:
                    click = self.win.getMouse()
                    x, y = int(click.getX()), int(click.getY())
                    if 20 <= x <= 140 and 20 <= y <= 80:
                        self.newGameButtonPressed()
                        break

    def updateActivePlayer(self) -> None:
        """
        Refreshes the top-right icon to reflect the current player's color.
        """
        # Create and display the player indicator
        playerIndicator = Circle(Point(460, 60), 30)
        playerIndicator.setFill(self._colorFromInt(self.game.currentPlayer))
        playerIndicator.draw(self.win)
    def colButtonsOn(self) -> None:
        """
        Activates and displays buttons for available columns.
        Each button's color corresponds to the current player's color.
        """
        buttonRadius = 35
        startX = 60
        buttonY = 190
        columnSpacing = 80

        for colIndex in range(self.board.columns):
            # Check if the column is available for a move
            if not self.board.isColumnFull(colIndex):
                position = Point(startX + colIndex * columnSpacing, buttonY)
                button = Circle(position, buttonRadius)
                button.setFill(self._colorFromInt(self.game.currentPlayer))
                button.draw(self.win)

    def colButtonsOff(self) -> None:
        """
        Deactivates all column buttons by changing their color to gray.
        """
        buttonRadius = 35
        startX = 60
        buttonY = 190
        columnSpacing = 80

        for colIndex in range(self.board.columns):
            # Recolor the button to gray to indicate inactivity
            position = Point(startX + colIndex * columnSpacing, buttonY)
            button = Circle(position, buttonRadius)
            button.setFill("gray")
            button.draw(self.win)

    def diceButtonOn(self) -> None:
        """
        Activates the dice button by highlighting it in red.
        """
        # Highlight the dice button
        self.die.setFill("red3")
        self.die.undraw()
        self.die.draw(self.win)

        # Keep the dice label visible
        self.dieLabel.undraw()
        self.dieLabel.draw(self.win)

    def diceButtonPressed(self) -> int:
        """
        Rolls the dice, updates its appearance, and displays the rolled value.
        The dice button turns gray to indicate inactivity.
        :return: The integer value of the rolled dice.
        """
        # Roll the dice and retrieve the result
        diceResult = self.game.rollDice()

        # Update the dice appearance
        self.die.setFill("gray")
        self.die.undraw()
        self.die.draw(self.win)

        # Update and display the dice label
        self.dieLabel.setText(str(diceResult))
        self.dieLabel.undraw()
        self.dieLabel.draw(self.win)

        return diceResult

    def newGameButtonPressed(self) -> None:
        """
        Clears the board and UI elements to start a fresh game.
        """
        # Remove old game elements
        elementsToUndraw = [self.newGameText, self.newGameButton, self.winner, self.die, self.dieLabel]
        for element in elementsToUndraw:
            element.undraw()

        # Start a new game and update the board
        self.game.newGame()
        self.displayBoard()
        self.updateActivePlayer()

    def displayResult(self) -> None:
        """
        Updates the game window to show the result.
        Disables all buttons except "New Game" and announces the winner or a draw.
        """
        # Turn off column buttons
        self.colButtonsOff()

        # Handle dice button state if there are more than two players
        if self.game.multiPlayer:
            self.diceButtonPressed()

        # Determine the result text
        resultText = "Draw" if self.game.isDraw else f"Player {self.game.winner} Wins!"

        # Display the result on the screen
        self.winner.setText(resultText)
        self.winner.draw(self.win)

    @staticmethod
    def _colorFromInt(playerIndex: int) -> str:
        """
        Maps a player's integer index to their corresponding color as a string.
        :param playerIndex: The integer representing the player.
        :return: The color associated with the player as a string.
        """
        colors = ["red", "blue", "green", "orange", "purple", "pink"]
        return colors[playerIndex]


def main():
    """
    Initializes and starts the Connect 4 War game.
    """
    # Define the number of players
    players = 3

    # Create the game interface
    connect4Game = GameUI(players)

    # Start the game loop
    connect4Game.gameOrder()

# Call the function to start the game
if __name__ == "__main__":
    main()

