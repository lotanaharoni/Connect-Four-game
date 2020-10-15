from.import board
from.import disc

PLAYER_ONE = 1
PLAYER_TWO = 2
DRAW = 0
BOARD_ROWS = 6
BOARD_COLUMNS = 7
EMPTY = "_"


class Game:
    """
    This is a class of 4 in a row (connect four) game to a computer.
    Each game consists of a board, discs to put on it and two players
    playng by turns . The winner is the player that succeds on connecting four
    discs in a row, column or diagonal.
    API:
    1) make_move - makes a move in the game.
    2) get_current_player - returns the player who's turn is the current.
    3) get player at - returns which player's disc is located in a slot.
    4) get winner - identifies the situation of the game.
    """

    def __init__(self):
        """
        A constructor for a game. creates a board, sets player 1 to start
        and sets the winner of the game to be None.
        """
        self.game_board = board.Board()
        self.current_player = PLAYER_ONE
        self.winner = None

    def make_move(self, column):
        """
        The main method of the game, controls all the moves. The
        method gets the requested column, checks if the  exists in the game,
        and if it's not full already. If so, the method creates a disc, related
        to the current player and puts it on the board.
        :param column: int.
        :return: Disc - the added disc.
        """
        # check input
        coordinate = (0, column)
        if column not in range(BOARD_COLUMNS):
            raise IndexError
        elif self.game_board.cell_content(coordinate) != EMPTY:
            raise ValueError
        if self.winner is not None:
            raise ValueError
        player = self.get_current_player()
        self.__set_current_player()
        for possible_move in self.game_board.possible_moves():
            if column == possible_move[1]:
                player_new_disc = disc.Disc(player, possible_move)
                self.game_board.add_disc(player_new_disc)
                if self.game_board.are_four_connected():
                    self.__set_winner(player)
                return player_new_disc

    def get_winner(self):
        """
        The method checks the status of the game - won or not.
        in case the game is won - who won. I case the game is not
        won - is it a draw or can the game continue.
        :return: 1 if player 1 has won, 2 if player 2 has won,
                 0 if the board is full, None otherwise.
        """
        if self.winner == PLAYER_ONE:
            return PLAYER_ONE
        elif self.winner == PLAYER_TWO:
            return PLAYER_TWO
        elif self.game_board.is_full() is True:
            return DRAW
        elif self.winner is None:
            return None

    def __set_winner(self, player):
        """
        sets a winner to the game.
        :param player: int - represents a player
        :return: None
        """
        self.winner = player

    def get_player_at(self, row, col):
        """
        The method returns the content of given coordinates
        :param row: int
        :param col: int
        :return: Disc if the slot is occupied, None otherwise.
        """
        if row not in range(BOARD_ROWS) or col not in range(BOARD_COLUMNS):
            raise IndexError
        else:
            coordinates = (row, col)
            content = self.game_board.cell_content(coordinates)
            if content == PLAYER_ONE or content == PLAYER_TWO:
                return content
            else:
                return None

    def get_current_player(self):
        """
        returns the current player.
        :return: int
        """
        return self.current_player

    def __set_current_player(self):
        """
        Sets the turns. changes the current player.
        :return: None
        """
        if self.get_current_player() == PLAYER_ONE:
            self.current_player = PLAYER_TWO
        else:
            self.current_player = PLAYER_ONE

    def get_winning_cells(self):
        """
        returns the winning slots from the board
        :return: list of tuples.
        """
        return self.game_board.get_winning_cells()

