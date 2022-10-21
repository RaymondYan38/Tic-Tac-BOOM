""" Class that creates objects with attributes specific for Tic-Tac-Toe.

    This is the BoardClass class that is made for the purpose of creating
    BoardClass objects that have specific data attached to them for
    both players in a Tic-Tac-Toe game. Methods are here to help reset games
    and modify attributes.

    Typical usage example:

    player1_gameboard = BoardClass()
"""


class BoardClass:
    """A simple class that stores and updates information about a user and their game board.

    Attributes:
        username: A user's username
        wins: The number of wins the user has
        ties: The number of ties the user has
        losses: The number of losses the user has
        games: The number of games the user has played
        board: The current condition of the game board
    """
    def __init__(self, username: str) -> None:
        """Make a BoardClass.

        Args:
            username: A User's username
        """
        self._username = username
        self._last_player = None
        self._wins = 0
        self._ties = 0
        self._losses = 0
        self._games = 0
        self._board = [[" " for _ in range(3)] for i in range(3)]

    def getBoard(self) -> list:
        """Gets board of a user.

        Returns:
            A 2-dimensional list of the User's updated board
        """
        return self._board

    def updateGamesPlayed(self) -> None:
        """Increments the number of games played.
        """
        self._games += 1

    def resetGameBoard(self) -> None:
        """Resets the game board for the User to original state.
        """
        self._board = [[" " for _ in range(3)] for i in range(3)]

    def updateGameBoard(self, x: int, y: int, player: str, player_username: str) -> None:
        """Updates the game board and last person who used a move.

        Args:
            x: int value of x-position of button on board that user clicked
            y: int value of y-position of button on board that user clicked
            player: str value of what character the user is
            player_username: str value of the username of the player who made a move
        """
        self._last_player = player_username  # Player will be x or y
        self._board[x][y] = player

    def bomb_center_board(self):
        self._board[1][1] = ""

    def increaseLoss(self) -> None:
        """Increments the number of losses.
        """
        self._losses += 1

    def increaseWin(self) -> None:
        """Increments the number of wins.
        """
        self._wins += 1

    def isWinner(self, player: str) -> bool:
        """Checks to see if a player has won the game and increments losses or wins.

        Args:
            player: A string that is either a 'X' or 'O', that identifies
            if a win condition has been met

        Returns:
            A bool value that indicates if a player has won or not.
        """
        winner = None
        top_left = self._board[0][0]
        top_mid = self._board[0][1]
        top_right = self._board[0][2]
        mid_left = self._board[1][0]
        mid_mid = self._board[1][1]
        mid_right = self._board[1][2]
        bot_left = self._board[2][0]
        bot_mid = self._board[2][1]
        bot_right = self._board[2][2]
        if top_left == player and top_mid == player and top_right == player:
            winner = True
        elif mid_left == player and mid_mid == player and mid_right == player:
            winner = True
        elif bot_left == player and bot_mid == player and bot_right == player:
            winner = True
        elif top_left == player and mid_left == player and bot_left == player:
            winner = True
        elif top_mid == player and mid_mid == player and bot_mid == player:
            winner = True
        elif top_right == player and mid_right == player and bot_right == player:
            winner = True
        elif top_left == player and mid_mid == player and bot_right == player:
            winner = True
        elif top_right == player and mid_mid == player and bot_left == player:
            winner = True
        if winner and self._username == self._last_player:
            self._wins += 1
        elif winner and self._username != self._last_player:
            self._losses += 1
        return winner

    def boardIsFull(self) -> bool:
        """Checks to see if a board is full of not.

        Returns:
            A bool value indicating if a board is full or not
        """
        full_board = True
        for row in self._board:
            for value in row:
                if value == " ":
                    full_board = False
        if full_board == True:
            self._ties += 1
            return True
        else:
            return False

    def printStats(self) -> None:
        """Prints out game statistics of the user
        """
        print(f"Username: {self._username}")
        print(f"Last player to make a move: {self._last_player}")
        print(f"Number of wins: {self._wins}")
        print(f"Number of ties: {self._ties}")
        print(f"Number of losses: {self._losses}")
        print(f"Number of games played: {self._games}")

    def getUsername(self) -> str:
        """Getter method of BoardClass's username

        Returns:
            A string containing BoardClass's username
        """
        return self._username

    def getLastPlayer(self) -> str:
        """Gets the last player to make a move.

        Returns:
            A string containing the username of the last player
        """
        return self._last_player

    def decrementTies(self) -> None:
        """Decrements the number of ties
        """
        self._ties -= 1

    def getWins(self) -> int:
        """Getter method of BoardClass's wins

        Returns:
            An int containing BoardClass's number of wins
        """
        return self._wins

    def getTies(self) -> int:
        """Getter method of BoardClass's ties

        Returns:
            An int containing BoardClass's number of ties
        """
        return self._ties

    def getLosses(self) -> int:
        """Getter method of BoardClass's losses

        Returns:
            An int containing BoardClass's number of losses
        """
        return self._losses

    def getGames(self) -> int:
        """Getter method of BoardClass's number of games played

        Returns:
            An int containing BoardClass's number of games played
        """
        return self._games
