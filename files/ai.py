import random

BOARD_ROWS = 6
BOARD_COLUMNS = 7
VALUE = 0
UP_ROW = 0
SINGLE_RESULT = 1


class AI:
    """
    This class represents the artificial intelligence that can play
    the game. The Ai object has a parameter of a game and a parameter
    of a player. The Ai object can guess a play that can be done in
    the game.
    """

    def __init__(self, game, player):
        """
        This method construct a new Ai object.
        :return: None
        """
        self.__game = game
        self.__player = player
        self.__possible_moves = None

    def find_legal_move(self, timeout=None):
        """
        This method finds a possible move for the AI -
        finds an empty slot.
        :return: int, the move that can be done.
        """
        winner = self.__game.get_winner()
        # check if the board has already a winner
        if winner is not None:
            raise ValueError
        self.__possible_moves = self.__check_possible_move()
        # check if the board is already full
        return self.__possible_moves

    def __check_possible_move(self):
        """
        This method runs over the game's board's columns and finds
        all the possible slots for a disc (one in each column).
        :return: int, the random column that the player can insert disc
        """
        all_options = []
        for column in range(BOARD_COLUMNS):
            try:
                player_at = self.__game.get_player_at(UP_ROW, column)
            except IndexError:
                continue
            if player_at is None:
                all_options.append(column)
        if len(all_options) != 0:
            random_column = random.sample(all_options, SINGLE_RESULT)
            return random_column[VALUE]
        else:
            return None

    def get_last_found_move(self):
        """
        This method returns the last move the Ai object has found
        :return: int, the last move
        """
        pass
