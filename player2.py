"""Class that creates server side player for a Tic-Tac-Toe Game.

    The PlayerTwo class is a class that orchestrates the entire server
    side of a Tic-Tac-Toe game. It has methods that create connections to
    sockets and setting usernames, as well as create a GUI for user's to
    play Tic-Tac-Toe on. It takes care of every aspect of the game such as
    only certain people can put a piece at a time and much more.

    Typical usage example:

    player2 = PlayerTwo()
"""


import socket
from gameboard import BoardClass
import sys
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import random


class PlayerTwo:
    """A simple class that runs player1/client side of a Tic-Tac-Toe Game.

    Attributes:
        host: host for socket connection
        port: port for socket connection
        p1_username: player1's username
        p2_username: player2's username
        try_again: Boolean for if a user wants to attempt something again
        window: Tkinter Window
        server: server
        clientAddress: client's connection address
        connection: client connection to socket
        p2_gameboard: BoardClass instance
        entire_board: A 2-dimensional list displaying the board of buttons
        your_turn: A message saying it is the user's turn
        opp_turn: A message saying it is the opponent's turn
        p1_decision: A string containing whether or not the user wants to continue playing
    """
    def __init__(self) -> None:
        """Make a PlayerTwo
        """
        self.windowSetUp()
        self.initTKVariables()
        self.createHostPortEntry()
        self.setUsername()
        self.confirmInstructions()
        self.runGame()
        self.runUI(self.window)

    def initTKVariables(self) -> None:
        """Initiates Tk variables
        """
        self.host = tk.StringVar()
        self.port = tk.IntVar()
        self.p1_username = tk.StringVar()
        self.p1_username.set("$")
        self.p2_username = tk.StringVar()
        self.p2_username.set("$")
        self.try_again = tk.StringVar()
        self.try_again.set("@")

    def windowSetUp(self) -> None:
        """Sets up TKinter window
        """
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe(Player 2 perspective)")
        self.window.configure(background='blue')

    def createHostPortEntry(self) -> None:
        """Creates connection between server and host and if connection failed, user asked to potentially try again.
        """
        while True:
            self.host.set(simpledialog.askstring("Tic-Tac-Toe: Host",
                                                 prompt="Player2, Please enter the host: "))
            self.port.set(simpledialog.askinteger("Tic-Tac-Toe: Port",
                                                  prompt="Player2, Please enter the integer value of the port between "
                                                         "0-65535 that should be used: "))
            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.bind((self.host.get(), self.port.get()))
                self.server.listen(1)
                self.connection, self.clientAddress = self.server.accept()
                break
            except (ConnectionRefusedError, OverflowError, socket.error):
                while self.try_again.get()[0].upper() != "Y" and self.try_again.get()[0].upper() != "N":
                    self.try_again.set(simpledialog.askstring("Tic-Tac-Toe: Connection Issue",
                                                              prompt="An error has occurred when connection, would you "
                                                                     "like to try again? Please type 'Y' or 'N'"))
                if self.try_again.get()[0].upper() == "Y":
                    self.try_again.set("@")
                    continue
                elif self.try_again.get()[0].upper() == "N":
                    self.window.destroy()
                    sys.exit()

    def setUsername(self) -> None:
        """Makes sure that the user sets up an alphanumeric username.
        """
        self.p1_username.set(self.connection.recv(1024).decode())
        while not self.p2_username.get().isalnum():
            self.p2_username.set(simpledialog.askstring("Tic-Tac-Toe: Username", prompt="Player2, you will be o/O. "
                                                                                        "Please enter an alphanumeric "
                                                                                        "username. NO special symbols "
                                                                                        "allowed. You will be asked "
                                                                                        "again if you username is "
                                                                                        "invalid: "))
        self.sendInformation(self.p2_username.get())

    def confirmInstructions(self) -> None:
        """Makes sure user understands Tic-Tac-Toe.
        """
        tk.messagebox.showinfo(title="Tic-Tac-Toe: Instructions", message=f"{self.p2_username.get()}, Tic Tac Toe "
                                                                                          "is a game of Xs and Os "
                                                                                          "where we will be marking "
                                       "spaces in a 3x3 grid. A winner is decided once someone has "
                                       "succeeded in placing three of their pieces in a row: horizontally, "
                                       "vertically, or diagonally. The way this specific version will work "
                                       "is that each user will be prompted to click a square of where they "
                                       "want to place their piece. Good Luck!", icon="info")
        self.p2_gameboard = BoardClass(self.p2_username.get())

    def sendInformation(self, user_entry: str) -> None:
        """Sends information through sockets.

        Args:
            user_entry: A string containing whatever the user wants to send over
        """
        self.connection.sendall(user_entry.encode())

    def createGameBoard(self) -> None:
        """Creates board of interactive buttons.
        """
        self.entire_board = []
        for x in range(3):
            row = []
            for y in range(3):
                row.append(tk.Button(self.window, text="", command=lambda x=x, y=y: self.initiateGame(x, y, "O"),
                                     font='bold', width=5, height=5))
                row[-1].grid(row=x+1, column=y, sticky="nsew")
            self.entire_board.append(row)
            if x == 2 and y == 2:
                p1_move = self.connection.recv(1024).decode()
                if p1_move == "center":
                    self.p2_gameboard.updateGameBoard(int(p1_move[-2]), int(p1_move[-1]), "X", self.p1_username.get())
                    self.entire_board[int(p1_move[-2])][int(p1_move[-1])]['text'] = 'X'
                    self.entire_board[int(p1_move[-2])][int(p1_move[-1])]['state'] = 'disabled'
                    self.entire_board[int(p1_move[-2])][int(p1_move[-1])].update()
                    tk.messagebox.showinfo(title="Tic-Tac-Toe: Game Event",
                                           message="The center of the board was cleared!")
                    self.entire_board[1][1]['text'] = ""
                    self.entire_board[1][1]['state'] = "normal"
                elif p1_move == "boom":
                    self.resetGameboards()
                    tk.messagebox.showinfo(title="Tic-Tac-Toe: Game Event",
                                           message="BOOM! The entire board was cleared")
                else:
                    self.p2_gameboard.updateGameBoard(int(p1_move[0]), int(p1_move[1]), "X", self.p1_username.get())
                    self.entire_board[int(p1_move[0])][int(p1_move[1])]['text'] = 'X'
                    self.entire_board[int(p1_move[0])][int(p1_move[1])]['state'] = 'disabled'
        self.your_turn = tk.Label(text=f'It is currently {self.p2_username.get()}\'s turn', bg='blue', fg='white')
        self.your_turn.grid(row=1, column=4)

    def initiateGame(self, x: int, y: int, player: str) -> None:
        """Places users piece on board, handles if a games end, and calls receiveMove() function.

            Args:
                x: int value of x-position of button on board that user clicked
                y: int value of y-position of button on board that user clicked
                player: str value of what character the user is
        """
        self.p2_gameboard.updateGameBoard(x, y, "O", self.p2_username.get())
        self.entire_board[x][y].config(text=player)
        self.entire_board[x][y]['state'] = 'disabled'
        self.entire_board[x][y].update()
        p2_move = str(x) + str(y)
        random_bomb = self.random_bomb()
        if type(random_bomb) == str:
            game_ended = self.checkWinTie(player)
            self.sendInformation(random_bomb + p2_move)
        else:
            self.sendInformation(p2_move)
            game_ended = self.checkWinTie(player)
        if game_ended:
            if self.p1_decision == "Play Again":
                self.resetGameboards()
                self.receiveMove()
            else:
                self.your_turn.destroy()
                self.your_turn.update()
                for x in range(3):
                    for y in range(3):
                        self.entire_board[x][y]['text'] = ""
                        self.entire_board[x][y]['state'] = "disabled"
                        self.entire_board[x][y].update()
        else:
            self.your_turn.destroy()
            self.opp_turn = tk.Label(text=f'It is currently {self.p1_username.get()}\'s turn', bg='blue', fg='white')
            self.opp_turn.grid(row=1, column=4)
            self.opp_turn.update()
            self.receiveMove()

    def receiveMove(self) -> None:
        """Places opponents piece on board, handles if a games end
        """
        p1_move = self.connection.recv(1024).decode()
        if "center" in p1_move:
            self.p2_gameboard.updateGameBoard(int(p1_move[-2]), int(p1_move[-1]), "X", self.p1_username.get())
            self.entire_board[int(p1_move[-2])][int(p1_move[-1])]['text'] = 'X'
            self.entire_board[int(p1_move[-2])][int(p1_move[-1])]['state'] = 'disabled'
            self.entire_board[int(p1_move[-2])][int(p1_move[-1])].update()
            tk.messagebox.showinfo(title="Tic-Tac-Toe: Game Event", message="The center of the board was cleared!")
            self.entire_board[1][1]['text'] = ""
            self.entire_board[1][1]['state'] = "normal"
        elif "boom" in p1_move:
            self.resetGameboards()
            tk.messagebox.showinfo(title="Tic-Tac-Toe: Game Event", message="BOOM! The entire board was cleared")
        else:
            self.entire_board[int(p1_move[0])][int(p1_move[1])].config(text="X")
            self.entire_board[int(p1_move[0])][int(p1_move[1])]['state'] = 'disabled'
            self.p2_gameboard.updateGameBoard(int(p1_move[0]), int(p1_move[1]), "X", self.p1_username.get())
            self.entire_board[int(p1_move[0])][int(p1_move[1])].update()
        self.opp_turn.destroy()
        self.your_turn = tk.Label(text=f'It is currently {self.p2_username.get()}\'s turn', bg='blue', fg='white')
        self.your_turn.grid(row=1, column=4)
        self.your_turn.update()
        game_ended = self.checkWinTie("X")
        if game_ended:
            if self.p1_decision == 'Play Again':
                self.resetGameboards()
                self.receiveMove()
            else:
                self.your_turn.destroy()
                self.your_turn.update()
                for x in range(3):
                    for y in range(3):
                        self.entire_board[x][y]['text'] = ""
                        self.entire_board[x][y]['state'] = "disabled"
                        self.entire_board[x][y].update()

    def afterGame(self, win: bool, tie: bool) -> None:
        """Deals with whatever decision player1 decides to do after a game ends.

        Args:
            win: bool containing whether a win has occurred
            tie: bool containing whether a tie has occurred
        """
        self.p2_gameboard.updateGamesPlayed()
        if win:
            tk.messagebox.showinfo(title="Tic-Tac-Toe: Game Results",
                                   message=f"Game Over! {self.p2_gameboard.getLastPlayer()} has won the game!")
        elif tie:
            tk.messagebox.showinfo(title="Tic-Tac-Toe: Game Results",
                                   message=f"Game Over! The game against {self.p1_username.get()} has ended in a tie")
        self.p1_decision = self.connection.recv(1024).decode()
        if self.p1_decision == "Play Again":
            self.your_turn.destroy()
            self.opp_turn = tk.Label(text=f'It is currently {self.p1_username.get()}\'s turn', bg='blue', fg='white')
            self.opp_turn.grid(row=1, column=4)
            self.opp_turn.update()
        elif self.p1_decision == "Fun Times":
            gameStatsUsername1 = tk.Label(self.window, text=f"Username: ", bg="blue", fg="white")
            gameStatsUsername1.grid(row=5, column=0)
            gameStatsUsername2 = tk.Label(self.window, text=f"{self.p2_username.get()}", bg="blue", fg="white")
            gameStatsUsername2.grid(row=5, column=1)
            gameStatsLastPlayer1 = tk.Label(self.window, text=f"Last player to make a move: ", bg="blue", fg="white")
            gameStatsLastPlayer1.grid(row=6, column=0)
            gameStatsLastPlayer2 = tk.Label(self.window, text=f"{self.p2_gameboard.getLastPlayer()}", bg="blue", fg="white")
            gameStatsLastPlayer2.grid(row=6, column=1)
            gameStatsWins1 = tk.Label(self.window, text=f"Number of wins: ", bg="blue", fg="white")
            gameStatsWins1.grid(row=7, column=0)
            gameStatsWins2 = tk.Label(self.window, text=f"{self.p2_gameboard.getWins()}", bg="blue", fg="white")
            gameStatsWins2.grid(row=7, column=1)
            gameStatsTies1 = tk.Label(self.window, text=f"Number of ties: ", bg="blue", fg="white")
            gameStatsTies1.grid(row=8, column=0)
            gameStatsTies2 = tk.Label(self.window, text=f"{self.p2_gameboard.getTies()}", bg="blue", fg="white")
            gameStatsTies2.grid(row=8, column=1)
            gameStatsLosses1 = tk.Label(self.window, text=f"Number of losses: ", bg="blue", fg="white")
            gameStatsLosses1.grid(row=9, column=0)
            gameStatsLosses2 = tk.Label(self.window,
                                             text=f"{self.p2_gameboard.getLosses()}", bg="blue", fg="white")
            gameStatsLosses2.grid(row=9, column=1)
            gameStatsGames1 = tk.Label(self.window,
                                            text=f"Number of games played: ", bg="blue", fg="white")
            gameStatsGames1.grid(row=10, column=0)
            gameStatsGames1 = tk.Label(self.window,
                                            text=f"{self.p2_gameboard.getGames()}", bg="blue", fg="white")
            gameStatsGames1.grid(row=10, column=1)

    def checkWinTie(self, player: str) -> bool:
        """Checks whether there was a winner from the last turn.

        Args:
            player: A string containing character "X" or "O"

        Returns:
            A bool value indicating whether ot not a game has ended
        """
        win = self.p2_gameboard.isWinner(player)
        tie = self.p2_gameboard.boardIsFull()
        if win and tie:
            self.p2_gameboard.decrementTies()
        if win or tie:
            self.afterGame(win, tie)
            return True
        else:
            return False

    def resetGameboards(self) -> None:
        """Resets the game board
        """
        self.p2_gameboard.resetGameBoard()
        for x in range(3):
            for y in range(3):
                self.entire_board[x][y]['text'] = ""
                self.entire_board[x][y]['state'] = "normal"

    def runGame(self) -> None:
        """Officially starts the game and calls createGameBoard function
        """
        self.createGameBoard()

    def random_bomb(self):
        rand = random.randrange(1, 10)
        if rand == 1:
            self.entire_board[1][1]['text'] = ""
            self.entire_board[1][1]['state'] = "normal"
            tk.messagebox.showinfo(title="Tic-Tac-Toe: Game Event", message="The center of the board was cleared!")
            return "center"
        rand2 = random.randrange(1, 100)
        if rand2 == 1:
            self.resetGameboards()
            tk.messagebox.showinfo(title="Tic-Tac-Toe: Game Event", message="BOOM! The entire board was cleared")
            return "boom"
        return False

    def runUI(self, windowName: tk) -> None:
        """Activates our window for use

            Args:
                windowName: The name of a window
        """
        windowName.mainloop()


if __name__ == "__main__":
    player_two = PlayerTwo()
