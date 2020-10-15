
class Disc:
    """
    This is a class for a disc. an object put in a '4 in a row' game board.
    the disc knows only its location on the board by coordinates and
    to which player it belongs.
    """
    def __init__(self, player, coordinates):
        """
        constructor for a disc.
        :param player: int. 1 or 2. the player that put the disc.
        :param coordinates: tuple. the coordinates of the disc on the board.
        """
        self.__player = player
        self.__coordinates = coordinates

    def get_coordinates(self):
        """
        returns the coordinates of the disc on the board
        :return: tuple
        """
        return self.__coordinates

    def get_player(self):
        """
        returns the player that put the disc.
        :return: int. 1 or 2.
        """
        return self.__player
