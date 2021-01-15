import copy

PLAYER_1 = 1
PLAYER_2 = 2
BOARD_ROWS = 6
BOARD_COLUMNS = 7
EMPTY = "_"
INITIATE_VALUE = 0
DIRECTION_NAME = 0
ROW = 0
COLUMN = 1
SEQUENCE = 3
COUNTER = 1
REQUIRED_SEQUENCE = 4
DIRECTIONS = {
    "D": "down",
    "R": "right",
    "L": "left",
    "D_U_L": "diagonal_up_left",
    "D_U_R": "diagonal_up_right",
    "D_D_R": "diagonal_down_right",
    "D_D_L": "diagonal_down_left"
}


class Board:
    """
    This class represents the game's board.
    """

    def __init__(self):
        """
        This method buildS a new Board object.
        """
        self.__board = []
        self.__wining_cells = []
        self.__last_disc = None
        temp = []

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                temp.append(EMPTY)
            self.__board.append(copy.deepcopy(temp))
            temp = []

    def __str__(self):
        """
        This method prints the board object
        :return: None
        """
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                print(self.__board[row][column], end=" ")
            print()
        print()

    def cell_content(self, coordinates):
        """
        :param coordinates: tuple, with "x" and "y" value
        :return: string in case of empty cell, int in case of full cell
        """
        return self.__board[coordinates[ROW]][coordinates[COLUMN]]

    def __all_cells(self):
        """
        :return: list of all the coordinates in the board
        """
        all_coordinates = []
        for row in range(len(self.__board)):
            for column in range(len(self.__board[row])):
                all_coordinates.append((row, column))
        return all_coordinates

    def add_disc(self, disc):
        """
        This method gets a "disc" object and adds it into the game's board.
        :param disc: An "Disc" object
        :return: None
        """
        disc_coordinates = disc.get_coordinates()
        player = disc.get_player()
        self.__board[disc_coordinates[ROW]][disc_coordinates[COLUMN]] = player
        self.__last_disc = disc

    def is_full(self):
        """
        This method checks if all the cells in the board are full.
        :return: True- if all the cells are full, and False- if not
        """
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if self.__board[row][col] == EMPTY:
                    return False
        return True

    def possible_moves(self):
        """
        This method returns all the legal moves that a player can do.
        :return: list of all the possible moves.
        """
        possible_moves = []
        for column in range(len(self.__board[ROW])):
            # For the highest cell in the column
            for row in range(len(self.__board))[::-1]:
                if self.__board[row][column] == EMPTY:
                    possible_moves.append((row, column))
                    break
        return possible_moves

    def update_winning_cells(self, directions):
        """
        This method updates the "winning cells" parameters.
        :param directions: list, represents the illness's name
        :return: None
        """
        last_disc_coordinates = self.__last_disc.get_coordinates()
        disc_x = last_disc_coordinates[ROW]
        disc_y = last_disc_coordinates[COLUMN]
        self.__wining_cells.append((disc_x, disc_y))
        # create the winning cells from the winning direction
        for direction in directions.items():
            for amount in range(1, direction[COUNTER] + 1):
                if direction[DIRECTION_NAME] == DIRECTIONS["R"]:
                    self.__wining_cells.append((disc_x, disc_y + 1 * amount))
                if direction[DIRECTION_NAME] == DIRECTIONS["D"]:
                    self.__wining_cells.append((disc_x + 1 * amount, disc_y))
                if direction[DIRECTION_NAME] == DIRECTIONS["L"]:
                    self.__wining_cells.append((disc_x, disc_y - 1 * amount))
                if direction[DIRECTION_NAME] == DIRECTIONS["D_U_L"]:
                    self.__wining_cells.append((disc_x - 1 * amount, disc_y - 1 * amount))
                if direction[DIRECTION_NAME] == DIRECTIONS["D_D_L"]:
                    self.__wining_cells.append((disc_x + 1 * amount, disc_y - 1 * amount))
                if direction[DIRECTION_NAME] == DIRECTIONS["D_U_R"]:
                    self.__wining_cells.append((disc_x - 1 * amount, disc_y + 1 * amount))
                if direction[DIRECTION_NAME] == DIRECTIONS["D_D_R"]:
                    self.__wining_cells.append((disc_x + 1 * amount, disc_y + 1 * amount))

    def get_winning_cells(self):
        """
        This method returns the "self.__winning cells" parameter
        :return: list
        """
        return self.__wining_cells

    def are_four_connected(self):
        """
        This method checks if the last disc that inserted to the board is
        a part of a sequence of four, or more, discs.
        :return: If there is a sequence, it returns the cells that build
                 the sequence, and if there is not sequence, it returns False
        """

        directions = {DIRECTIONS["D"]: INITIATE_VALUE, DIRECTIONS["R"]: INITIATE_VALUE,
                      DIRECTIONS["L"]: INITIATE_VALUE, DIRECTIONS["D_U_L"]: INITIATE_VALUE,
                      DIRECTIONS["D_U_R"]: INITIATE_VALUE, DIRECTIONS["D_D_R"]: INITIATE_VALUE,
                      DIRECTIONS["D_D_L"]: INITIATE_VALUE}

        if self.__last_disc is not None:
            coordinates = self.__last_disc.get_coordinates()
            player = self.__last_disc.get_player()
            if self.is_full() is False:
                directions = self.__check_four(coordinates[0], coordinates[1], player, directions)

                # If there is a horizontal sequence
                if directions[DIRECTIONS["R"]] + directions[DIRECTIONS["L"]] >= SEQUENCE:
                    self.update_winning_cells({DIRECTIONS["R"]: directions[DIRECTIONS["R"]],
                                               DIRECTIONS["L"]: directions[DIRECTIONS["L"]]})
                    return self.__last_disc.get_player()

                # If there is a diagonal down sequence
                if directions[DIRECTIONS["D_U_L"]] + directions[DIRECTIONS["D_D_R"]] >= SEQUENCE:
                    self.update_winning_cells({DIRECTIONS["D_U_L"]: directions[DIRECTIONS["D_U_L"]],
                                               DIRECTIONS["D_D_R"]: directions[DIRECTIONS["D_D_R"]]})
                    return self.__last_disc.get_player()

                # If there is a diagonal up sequence
                if directions[DIRECTIONS["D_U_R"]] + directions[DIRECTIONS["D_D_L"]] >= SEQUENCE:
                    self.update_winning_cells({DIRECTIONS["D_U_R"]: directions[DIRECTIONS["D_U_R"]],
                                               DIRECTIONS["D_D_L"]: directions[DIRECTIONS["D_D_L"]]})
                    return self.__last_disc.get_player()

                # If there is a down sequence
                if directions[DIRECTIONS["D"]] == SEQUENCE:
                    self.update_winning_cells({DIRECTIONS["D"]: directions[DIRECTIONS["D"]]})
                    return self.__last_disc.get_player()
        return False

    def __check_four(self, disc_row, disc_col, player, directions):
        """
        This method runs 3 times the method "__find_optionals", and checks
        if the last disc that inserted to the board is a part of a
        sequence with 3 cells in every direction
        :param disc_row: int, represents the row in the board
        :param disc_col: int, represents the column in the board
        :param player: int, represents the number of the player
        :param directions: dictionary with all the directions
        :return: A dictionary od all the directions and the counter of them
        """

        all_directions = [DIRECTIONS["D"], DIRECTIONS["R"], DIRECTIONS["L"],
                          DIRECTIONS["D_U_L"], DIRECTIONS["D_U_R"],
                          DIRECTIONS["D_D_R"], DIRECTIONS["D_D_L"]]

        # runs 3 times the "__find_optionals" and try to find a sequence of 4 cells
        for time in range(1, REQUIRED_SEQUENCE):
            directions = self.__find_optionals(disc_row, disc_col, player,
                                               directions, time, all_directions)
        return directions

    def __find_optionals(self, disc_row, disc_col,
                         player, directions, times, all_directions):
        """
        This method checks if there is a sequence in all the directions, for the
        disc that inserted to the board, "times" cells in every direction
        :param disc_row: int, represents the row in the board
        :param disc_col: int, represents the column in the board
        :param player: int, represents the number of the player
        :param directions: dictionary with all the directions
        :param all_directions: list with all the names of the directions
        :return: A dictionary od all the directions and the counter of them
        """
        names_to_remove = []
        for item in all_directions:
            if_exist = False
            # If the sequence can be continue with "down" direction
            if item == DIRECTIONS["D"]:
                if disc_row + times <= BOARD_ROWS - 1 and \
                        self.__board[disc_row + times][disc_col] == player:
                    if_exist = True
            # If the sequence can be continue with "right" direction
            elif item == DIRECTIONS["R"]:
                if disc_col + times <= BOARD_COLUMNS - 1 and \
                        self.__board[disc_row][disc_col + times] == player:
                    if_exist = True
            # If the sequence can be continue with "left" direction
            elif item == DIRECTIONS["L"]:
                if disc_col - times >= 0 and \
                        self.__board[disc_row][disc_col - times] == player:
                    if_exist = True
            # If the sequence can be continue with "diagonal up left" direction
            elif item == DIRECTIONS["D_U_L"]:
                if disc_row - times >= 0 and disc_col - times >= 0 and \
                            self.__board[disc_row - times][disc_col - times] == player:
                    if_exist = True
            # If the sequence can be continue with "diagonal up right" direction
            elif item == DIRECTIONS["D_U_R"]:
                if disc_row - times >= 0 and disc_col + times <= BOARD_COLUMNS - 1 and \
                            self.__board[disc_row - times][disc_col + times] == player:
                    if_exist = True
            # If the sequence can be continue with "diagonal down left" direction
            elif item == DIRECTIONS["D_D_L"]:
                if disc_row + times <= BOARD_ROWS - 1 and disc_col - times >= 0 and \
                            self.__board[disc_row + times][disc_col - times] == player:
                    if_exist = True
            # If the sequence can be continue with "diagonal down right" direction
            elif item == DIRECTIONS["D_D_R"]:
                if disc_row + times <= BOARD_ROWS - 1 and disc_col + times <= BOARD_COLUMNS - 1 and \
                            self.__board[disc_row + times][disc_col + times] == player:
                    if_exist = True
            # If there is no disc in the specific direction to make a sequence
            if if_exist is False:
                # prepare to stop checking in this direction
                names_to_remove.append(item)
            # If there is a disc in the specific direction, add to the counter
            else:
                directions[item] = directions[item] + 1
        # Remove the directions without a sequence in order to stop checking them
        for name in names_to_remove:
            all_directions.remove(name)

        return directions
