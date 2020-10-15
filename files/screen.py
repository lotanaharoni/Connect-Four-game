import tkinter as tk
import time
from.import game
from.import ai

PLAYER_VS_PLAYER = 1
PLAYER_VS_AI = 2
AI_VS_PLAYER = 3
AI_VS_AI = 4
LEFT_SCREEN_LIMIT_X = 60
LEFT_SCREEN_LIMIT_Y = 30
LEFT_SCREEN_DOWN_X = 140
LEFT_SCREEN_DOWN_Y = 110
BOARD_Y_ORIGIN = 80
BOTTOM_LIMIT = 650
DOWN_RIGHT_CIRCLE_CORNER = 80
GAP_BETWEEN_COLUMNS = 100
GAP_BETWEEN_ROWS = 100
ILLEGAL_CLICK = (-1, -1)
INITIATE_COORDINATE_VALUE = 0
PLAYER_ONE = 1
PLAYER_TWO = 2
PLAYER_ONE_COLOR = "yellow"
PLAYER_TWO_COLOR = "red"
WINNING_COLOR = "grey"
FLASH_COLOR = "purple"
DRAW = 0
BOARD_ROWS = 6
BOARD_COLUMNS = 7
PAUSE_BETWEEN_TURNS = 0.5
X_COORDINATE = 0
Y_COORDINATE = 1
TIMES_FOR_FLASH = 4
FLASH_TIME = 10
TWO_MOVES_BY_EACH_PLAYER = 2
TINY_PAUSE = 0.01
MESSAGES = {
    "by message": "Bye Bye...",
    "AI illegal move": "No possible AI moves.",
    "player one victory": "Victory! Yellow player has won!",
    "player two victory": "Victory! Red player has won!"
}


class Screen:
    """
    This class represents the "GUI", and it connects the "game" object,
    and the "Ai" object. The "Four in a row" game can run from the
    "Screen" object, and it operates the different parts of the game.
    """

    def __init__(self):
        """
        This method build a new Screen object. It contains a "Game" objects,
        a "Tk" object, an "Ai" object, permanent widgets and and parameters
        that help running the game.
        :return: None
        """
        self.__turn = None
        self.__restart_possible = True
        self.__game = game.Game()
        self.__root = tk.Tk()
        self.__time = time
        self.__new_coordinates = None
        self.__ai_1 = ai.AI(self.__game, PLAYER_ONE)
        self.__ai_2 = ai.AI(self.__game, PLAYER_TWO)
        self.__root.geometry("1000x1000")
        self.__title = tk.Frame(self.__root, width=1400,
                                height=50, bg="chartreuse3",
                                borderwidth=5, relief=tk.RIDGE)
        self.__manage_frame = tk.Frame(self.__root, width=210,
                                       height=950, bg="green4",
                                       borderwidth=5, relief=tk.RIDGE)
        self.__can = tk.Canvas(self.__root, width=800,
                               height=1000, bg="red4",
                               borderwidth=5, relief=tk.RIDGE)
        self.__player_label = tk.Label(self.__manage_frame,
                                       text="Yellow player's turn",
                                       font="roman 16 bold", bg="green4")
        self.__player_canvas = tk.Canvas(self.__manage_frame,
                                         width=100, height=100, bg="green4",
                                         borderwidth=5, relief=tk.RIDGE)
        self.__victory_image = tk.PhotoImage(file="files/_victory.png")
        self.__illegal_image = tk.PhotoImage(file="files/_stop.png")
        self.__full_image = tk.PhotoImage(file="files/_fullboard.png")

    def game_menu(self, restart=None):
        """
        This method creates the main menu of the game. It allows the player to choose
        what type of game he wants to play. The method creates the menu's settings and
        creates the widgets objects it needs. Moreover, it creates the "bind" function
        for the buttons.
        :param restart: bool, True- if the "restart" button was clicked and False if not
        :return: None
        """
        menu_frame = tk.Frame(self.__root, width=500, height=500, bg="red4",
                              borderwidth=10, relief=tk.RIDGE)

        # creating menu buttons
        pl_v_pl = tk.Button(menu_frame, width=25, height=1,
                            text="play against another player",
                            bg="green4", font="roman 14 bold",
                            overrelief=tk.GROOVE, borderwidth=4,
                            relief=tk.RAISED)
        pl_v_ai = tk.Button(menu_frame, width=30, height=1,
                            text="play against AI - player starts",
                            bg="green4", font="roman 14 bold",
                            overrelief=tk.GROOVE, borderwidth=4,
                            relief=tk.RAISED)
        ai_v_pl = tk.Button(menu_frame, width=30, height=1,
                            text="play against AI - AI starts",
                            bg="green4", font="roman 14 bold",
                            overrelief=tk.GROOVE, borderwidth=4,
                            relief=tk.RAISED)
        ai_v_ai = tk.Button(menu_frame, width=20, height=1,
                            text="AI against AI", bg="green4",
                            font="roman 14 bold", borderwidth=4,
                            overrelief=tk.GROOVE, relief=tk.RAISED)
        quit_button = tk.Button(menu_frame, text="quit",
                                font="roman 14 bold", bg="green4",
                                width=8, height=1, command=self.__exit_game,
                                overrelief=tk.GROOVE, borderwidth=4,
                                relief=tk.RAISED)

        # placing widgets
        menu_frame.place(x=200, y=100)
        pl_v_pl.place(x=120, y=80)
        pl_v_ai.place(x=100, y=140)
        ai_v_pl.place(x=100, y=200)
        ai_v_ai.place(x=130, y=260)
        quit_button.place(x=195, y=400)

        # binding methods to buttons
        if restart is None:

            # title for the menu when entering the game
            menu_title = tk.Label(menu_frame, text="Welcome! Play 4 in a row!",
                                  font="roman 22 bold underline", bg="red4",
                                  underline=-1)
            pl_v_pl.bind("<Button-1>", lambda e: self.__set_game(PLAYER_VS_PLAYER, menu_frame))
            pl_v_ai.bind("<Button-1>", lambda e: self.__set_game(PLAYER_VS_AI, menu_frame))
            ai_v_ai.bind("<Button-1>", lambda e: self.__set_game(AI_VS_AI, menu_frame))
            ai_v_pl.bind("<Button-1>", lambda e: self.__set_game(AI_VS_PLAYER, menu_frame))
        else:

            # title for the menu after a game ends
            menu_title = tk.Label(menu_frame, text="play again? Choose an option",
                                  font="roman 22 bold underline", bg="red4",
                                  underline=-1)
            pl_v_pl.bind("<Button-1>", lambda e: self.__restart_game(PLAYER_VS_PLAYER, menu_frame))
            pl_v_ai.bind("<Button-1>", lambda e: self.__restart_game(PLAYER_VS_AI, menu_frame))
            ai_v_ai.bind("<Button-1>", lambda e: self.__restart_game(AI_VS_AI, menu_frame))
            ai_v_pl.bind("<Button-1>", lambda e: self.__restart_game(AI_VS_PLAYER, menu_frame))
        menu_title.place(x=80, y=20)

        # running the mainloop
        self.__root.mainloop()

    def __set_game(self, game_mode, menu_frame=None):
        """
        This method creates the visual settings and the visual objects in the game.
        Moreover, it creates the widget's setting, when the game starts.
        :param game_mode: int, represent the type of the game
        :param menu_frame: widget - Frame
        :return: None
        """
        # deletes the menu frame
        if menu_frame is not None:
            menu_frame.destroy()

        # defining widgets
        self.__root.protocol("WM_DELETE_WINDOW", self.__exit_game)
        title_label = tk.Label(self.__title, text="FOUR IN A ROW!",
                               font="roman 20 bold", bg="chartreuse3")
        quit_button = tk.Button(self.__manage_frame, text="quit",
                                font="roman 10 bold", bg="indian red",
                                width=5, height=1, command=self.__exit_game,
                                overrelief=tk.GROOVE, borderwidth=4,
                                relief=tk.RAISED)
        restart_button = tk.Button(self.__manage_frame, text="restart game",
                                   font="roman 10 bold", bg="indian red",
                                   width=13, height=1, overrelief=tk.GROOVE,
                                   borderwidth=4, relief=tk.RAISED)
        restart_button.bind("<Button-1>",
                            lambda e: self.__restart_game(game_mode) if self.__restart_possible is True else None)

        # creating circles
        for row_can in range(BOARD_ROWS):
            for column_can in range(BOARD_COLUMNS):
                self.__can.create_oval(LEFT_SCREEN_LIMIT_X + (GAP_BETWEEN_COLUMNS * column_can),
                                       LEFT_SCREEN_LIMIT_Y + (GAP_BETWEEN_ROWS * row_can),
                                       LEFT_SCREEN_DOWN_X + (GAP_BETWEEN_COLUMNS * column_can),
                                       LEFT_SCREEN_DOWN_Y + (GAP_BETWEEN_ROWS * row_can),
                                       width=4, fill="white")

        # positioning widgets
        self.__title.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__manage_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.__can.pack(side=tk.RIGHT)
        title_label.place(x=350, y=2)
        quit_button.place(x=60, y=580)
        restart_button.place(x=40, y=530)
        self.__player_label.place(x=5, y=10)
        self.__player_canvas.place(x=40, y=60)
        self.__player_canvas.create_oval(20, 20, 90, 90, width=4, fill=PLAYER_ONE_COLOR)
        self.__initiate_game(game_mode)

    def __initiate_game(self, game_mode):
        """
        This method gets the game mode that the player has chose,
        and it calls the method that match to the player's choice.
        :param game_mode: int, represent the type of the game
        :return: None
        """
        # IF the player choose game between two player or player VS AI
        if game_mode == PLAYER_VS_PLAYER or game_mode == PLAYER_VS_AI:
            self.__turn = PLAYER_ONE
            self.__can.bind('<Button-1>', lambda e: self.__initiate_move(e, game_mode))
        # IF the player choose game between AI and a player
        elif game_mode == AI_VS_PLAYER:
            self.__click_on_canvas(AI_VS_PLAYER)
        # IF the player choose game between two AI's
        elif game_mode == AI_VS_AI:
            self.__click_on_canvas(AI_VS_AI)

    def __initiate_move(self, event, game_mode):
        """
        This method gets the type of the "game mode" from the
        "set_game" method. This method updates the coordinates of
        the player's click on the canvas and calls the "click_on_canvas
        method. The method is been called when the player begins the game.
        :param game_mode: int, represent the type of the game
        :return: None
        """
        # If there is no winning already and the player is player 1
        if self.__new_coordinates != ILLEGAL_CLICK and self.__turn == PLAYER_ONE:
            # If this is noe AI VS player
            if game_mode != AI_VS_PLAYER:
                # Save the coordinates of the click on the canvas
                self.__new_coordinates = (event.x, event.y)
                self.__click_on_canvas(game_mode)
            else:
                # If This is the first move
                if self.__new_coordinates is None:
                    try:
                        possible_move = self.__ai_2.find_legal_move()
                    except IndexError:
                        self.__ai_no_moves()
                        return None
                    except ValueError:
                        self.__ai_no_moves()
                        return None
                    # In case this is the Aiv first move against the player, draw the first disc
                    self.__new_coordinates = (possible_move * GAP_BETWEEN_COLUMNS + LEFT_SCREEN_LIMIT_X,
                                              INITIATE_COORDINATE_VALUE)
                    self.__draw_disc()
                    self.__can.update()
                    self.__time.sleep(PAUSE_BETWEEN_TURNS)
                else:
                    # Initiate the mode: turn the game to "player VS AI" mode
                    game_mode = PLAYER_VS_AI
                    self.__new_coordinates = (event.x, event.y)
                    self.__click_on_canvas(game_mode)

    def __click_on_canvas(self, game_mode):
        """
        This method gets the type of the "game mode" the player chose to play,
        and it operates this type of game.
        :param game_mode: int, represent the type of the game
        :return: None
        """
        if game_mode == PLAYER_VS_PLAYER:
            self.__draw_disc()
            self.__turn = PLAYER_ONE
        elif game_mode == PLAYER_VS_AI:
            self.__player_vs_ai()
        elif game_mode == AI_VS_PLAYER:
            self.__ai_vs_player()
        elif game_mode == AI_VS_AI:
            self.__ai_vs_ai()

    def __player_vs_ai(self):
        """
        This method runs a single turn for the player, that starts, and a
        single turn for the "Ai" object. The method checks if the turn is
        legal for every player.
        :return: None
        """
        # Do two turns for every game
        for each_turn in range(TWO_MOVES_BY_EACH_PLAYER):
            # If this is the first turn
            if each_turn == 0:
                self.__draw_disc()
                self.__can.update()
                # In case that the "__draw disc" method was failed
                if self.__turn == PLAYER_ONE:
                    break
                # If player 1 succeeded to draw, and there is no winning
            if each_turn == PLAYER_ONE and self.__new_coordinates != ILLEGAL_CLICK:
                self.__time.sleep(PAUSE_BETWEEN_TURNS)
                try:
                    possible_move = self.__ai_2.find_legal_move()
                except IndexError:
                    # Show the frame of no moves"
                    self.__ai_no_moves()
                    return None
                except ValueError:
                    self.__ai_no_moves()
                    return None
                # Save the new coordinates of every turn
                self.__new_coordinates = (possible_move * GAP_BETWEEN_COLUMNS + LEFT_SCREEN_LIMIT_X,
                                          INITIATE_COORDINATE_VALUE)
                self.__draw_disc()
                self.__can.update()
                # Set the turn to the first player
                self.__turn = PLAYER_ONE

    def __ai_vs_player(self):
        """
        This method runs a single turn for the "Ai" that starts the game.
        After it's turn, it initiates a "player_vs_ai" game, that the player
        starts every turn.
        :return: None
        """
        self.__can.update()
        self.__time.sleep(PAUSE_BETWEEN_TURNS)
        # The AI tries to do legal move
        try:
            possible_move = self.__ai_1.find_legal_move()
        except IndexError:
            self.__ai_no_moves()
            return None
        except ValueError:
            self.__ai_no_moves()
            return None
        self.__new_coordinates = (possible_move * GAP_BETWEEN_COLUMNS + LEFT_SCREEN_LIMIT_X,
                                  INITIATE_COORDINATE_VALUE)
        self.__draw_disc()
        # From this moment, start the "player VS AI" mode
        self.__can.bind('<Button-1>', lambda e: self.__initiate_move(e, PLAYER_VS_AI))
        self.__can.update()
        # A little pause after the AI move
        self.__time.sleep(PAUSE_BETWEEN_TURNS)
        self.__turn = PLAYER_ONE

    def __ai_vs_ai(self):
        """
        This method runs inside a loop a whole game between two "Ai" objects.
        The game is finished when one of the "Ai" objects is wins.
        :return: None
        """
        self.__new_coordinates = (INITIATE_COORDINATE_VALUE, INITIATE_COORDINATE_VALUE)
        # while loops until the game is over - no events required
        while self.__new_coordinates != ILLEGAL_CLICK:
            for move in range(TWO_MOVES_BY_EACH_PLAYER):
                # delay for human observance
                self.__time.sleep(PAUSE_BETWEEN_TURNS)
                #
                if self.__new_coordinates != ILLEGAL_CLICK:
                    # first ai
                    if move == 0:
                        try:
                            possible_move = self.__ai_1.find_legal_move()
                        except IndexError:
                            self.__ai_no_moves()
                            break
                        except ValueError:
                            self.__ai_no_moves()
                            break
                    else:
                        # second ai
                        try:
                            possible_move = self.__ai_2.find_legal_move()
                        except IndexError:
                            self.__ai_no_moves()
                            break
                        except ValueError:
                            self.__ai_no_moves()
                            break
                    self.__new_coordinates = (possible_move * GAP_BETWEEN_COLUMNS +
                                              LEFT_SCREEN_LIMIT_X, INITIATE_COORDINATE_VALUE)
                    self.__draw_disc()
                    self.__can.update()

    def __draw_disc(self):
        """
        This method draws a new disc in the canvas widget. It takes the position
        from the "self.new_coordinates" object. If the position is invalid, it
        raises exception and does not draw.
        :return: None. If the exception was raised it returns None before it finishes
        """
        what_column = self.__convert_coordinates_to_columns(self.__new_coordinates[X_COORDINATE])

        # inserting new disc
        try:
            new_disc = self.__game.make_move(what_column)
        except IndexError:
            self.__show_illegal_move_frame()
            return None
        except ValueError:
            self.__show_illegal_move_frame()
            return None

        # display disc on GUI
        new_disc_coordinates = self.__convert_column_to_coordinates(new_disc.get_coordinates())
        color = self.__choose_color()
        self.__can.create_oval(new_disc_coordinates[X_COORDINATE], new_disc_coordinates[Y_COORDINATE],
                               DOWN_RIGHT_CIRCLE_CORNER + new_disc_coordinates[X_COORDINATE],
                               DOWN_RIGHT_CIRCLE_CORNER + (new_disc_coordinates[Y_COORDINATE]),
                               width=4, fill=color)
        self.__check_game_status()
        # switching turns
        if self.__turn == PLAYER_ONE:
            self.__turn = PLAYER_TWO

    def __check_game_status(self):
        """
        This method checks if the game has been won, if it is, it calls the
        "self.winning_visual" method. If not, it does nothing.
        :return: None
        """
        winner = self.__game.get_winner()
        if winner is not None:
            if winner == DRAW:
                self.__new_coordinates = ILLEGAL_CLICK
                self.__show_draw_frame()
            else:
                self.__winning_visual()
        else:
            self.__set_player_labels()

    def __winning_visual(self):
        """
        This method is been calling when the game has been won. It
        flashes the discs that symbolizes the victory. In the ens, it
        changes the color of the discs to grey and calls the
        "show_victory_frame" method.
        :return: None
        """
        self.__restart_possible = False
        self.__new_coordinates = ILLEGAL_CLICK
        new_wining_cells = []
        winning_cells = self.__game.get_winning_cells()
        # Save the winning cells
        for cell in winning_cells:
            new_wining_cells.append(self.__convert_column_to_coordinates(cell))
        # Flash four times all the discs
        for flash in range(TIMES_FOR_FLASH):
            # Flash each disc in the sequence
            for each_flash in range(FLASH_TIME):
                # For every time that counts the flashes
                for each_disc in new_wining_cells:
                    # Flash in every 10 "milisec"
                    if each_flash % FLASH_TIME == 0:
                        changing_color = self.__choose_color()
                    else:
                        changing_color = FLASH_COLOR
                    self.__can.create_oval(each_disc[X_COORDINATE], each_disc[Y_COORDINATE],
                                           DOWN_RIGHT_CIRCLE_CORNER + each_disc[X_COORDINATE],
                                           DOWN_RIGHT_CIRCLE_CORNER + (each_disc[Y_COORDINATE]), width=4,
                                           fill=changing_color)
                    self.__can.update()
                    self.__time.sleep(TINY_PAUSE)
        for each_disc in new_wining_cells:
            self.__can.create_oval(each_disc[X_COORDINATE], each_disc[Y_COORDINATE],
                                   DOWN_RIGHT_CIRCLE_CORNER + each_disc[X_COORDINATE],
                                   DOWN_RIGHT_CIRCLE_CORNER + (each_disc[Y_COORDINATE]), width=4,
                                   fill=WINNING_COLOR)
        self.__show_victory_frame()

    def __show_victory_frame(self):
        """
        This method pops the victory frame after the game is won.
        the frame rests on the screen for 3 seconds and disappears.
        the method calls then the game menu.
        :return: None
        """
        victory_frame = tk.Frame(self.__root, width=550,
                                 height=400, bg="green4",
                                 borderwidth=10, relief=tk.RIDGE)
        if self.__game.get_current_player() == PLAYER_ONE:
            victory_text = tk.Label(victory_frame,
                                    text=MESSAGES["player two victory"],
                                    bg="green4", font="roman 26 bold")
        else:
            victory_text = tk.Label(victory_frame,
                                    text=MESSAGES["player one victory"],
                                    bg="green4", font="roman 26 bold")
        victory_image = tk.Label(victory_frame, image=self.__victory_image)
        victory_frame.place(x=150, y=100)
        victory_text.place(x=40, y=60)
        victory_image.place(x=140, y=150)
        self.__root.after(3000, victory_frame.destroy)
        # True for restart=True
        self.__root.after(3000, lambda: self.game_menu(True))

    def __show_draw_frame(self):
        """
        This method shows a draw frame when the game has been
        finished. The frame shows a picture ans a message to
        the player about the "draw" between the players.
        :return: None
        """
        full_board_frame = tk.Frame(self.__root, width=500,
                                    height=400, bg="green4",
                                    borderwidth=10, relief=tk.RIDGE)
        full_board_label = tk.Label(full_board_frame,
                                    text="Draw! Full Board!",
                                    bg="green4", font="roman 26 bold")
        full_board_image = tk.Label(full_board_frame, image=self.__full_image)
        full_board_frame.place(x=200, y=200)
        full_board_label.place(x=10, y=60)
        full_board_image.place(x=150, y=130)
        self.__root.after(4000, full_board_frame.destroy)
        self.__root.after(4000, lambda: self.game_menu(True))

    def __ai_no_moves(self):
        """
        This method sets the "Ai"'s frame and organizes it with all the other
        widgets of the game.
        :return: None
        """
        illegal_move_frame = tk.Frame(self.__root, width=400,
                                      height=400, bg="green4",
                                      borderwidth=10, relief=tk.RIDGE)
        illegal_move_label = tk.Label(illegal_move_frame,
                                      text=MESSAGES["AI illegal move"],
                                      bg="green4", font="roman 26 bold")
        illegal_move_image = tk.Label(illegal_move_frame, image=self.__illegal_image)
        illegal_move_frame.place(x=250, y=100)
        illegal_move_label.place(x=90, y=60)
        illegal_move_image.place(x=80, y=130)
        self.__root.after(700, illegal_move_frame.destroy)

    def __show_illegal_move_frame(self):
        """
        This method shows an illegal frame when an illegal move
        has been done. The frame shows a picture ans a message to
        the player about the illegal move.
        :return: None
        """
        illegal_move_frame = tk.Frame(self.__root, width=400,
                                      height=400, bg="green4",
                                      borderwidth=10, relief=tk.RIDGE)
        illegal_move_label = tk.Label(illegal_move_frame,
                                      text="Illegal move!",
                                      bg="green4", font="roman 26 bold")
        illegal_move_image = tk.Label(illegal_move_frame, image=self.__illegal_image)
        illegal_move_frame.place(x=250, y=100)
        illegal_move_label.place(x=90, y=60)
        illegal_move_image.place(x=80, y=130)
        self.__root.after(700, illegal_move_frame.destroy)

    def __set_player_labels(self):
        """
        sets the label on the right upper corner of the screen
        on every turn.
        :return: None
        """
        if self.__game.get_current_player() == PLAYER_ONE:
            self.__player_label.config(text="Yellow player's turn")
            self.__player_canvas.create_oval(20, 20, 90, 90, width=4, fill=PLAYER_ONE_COLOR)
        else:
            self.__player_label.config(text="Red player's turn")
            self.__player_canvas.create_oval(20, 20, 90, 90, width=4, fill=PLAYER_TWO_COLOR)

    def __restart_game(self, mode, menu_frame=None):
        """
        This method finishes the current game and initiates a new game with
        the initiates settings that the game needs.
        :param mode: int, represent the type of the game
        :param menu_frame: widget - Frame
        :return: None
        """
        # destroying the menu frame if exists
        if menu_frame is not None:
            menu_frame.destroy()

        # destroying GUI widgets
        self.__title.destroy()
        self.__manage_frame.destroy()
        self.__can.destroy()
        self.__player_label.destroy()
        self.__player_canvas.destroy()

        # resetting a new game
        self.__new_coordinates = None
        self.__turn = None
        self.__restart_possible = True
        self.__game = game.Game()
        self.__ai_1 = ai.AI(self.__game, PLAYER_ONE)
        self.__ai_2 = ai.AI(self.__game, PLAYER_TWO)

        # creating new widgets
        self.__title = tk.Frame(self.__root, width=1400,
                                height=50, bg="chartreuse3",
                                borderwidth=5, relief=tk.RIDGE)
        self.__manage_frame = tk.Frame(self.__root, width=210,
                                       height=950, bg="green4",
                                       borderwidth=5, relief=tk.RIDGE)
        self.__can = tk.Canvas(self.__root, width=800,
                               height=1000, bg="red4",
                               borderwidth=5, relief=tk.RIDGE)
        self.__player_label = tk.Label(self.__manage_frame,
                                       text="Yellow player's turn",
                                       font="roman 16 bold", bg="green4")
        self.__player_canvas = tk.Canvas(self.__manage_frame, width=100,
                                         height=100, bg="green4",
                                         borderwidth=5, relief=tk.RIDGE)
        self.__set_game(mode)

    def __exit_game(self):
        """
        This method finishes the current game and destroys the "root" object.
        :return: None
        """
        exit_frame = tk.Frame(self.__root, width=400,
                              height=200, bg="green4",
                              borderwidth=10, relief=tk.RIDGE)
        exit_label = tk.Label(exit_frame, text=MESSAGES["by message"],
                              bg="green4", font="roman 26 bold")
        self.__new_coordinates = ILLEGAL_CLICK
        exit_frame.place(x=250, y=300)
        exit_label.place(x=120, y=60)
        self.__root.after(2000, self.__root.destroy)

    def __convert_coordinates_to_columns(self, coord_x):
        """
        This method converts the coordinate of the "x" click on the screen
        To the match column in the game.
        :param coord_x: int, represents the "x" coordinate of the click
        :return: int, the column that math to the coordinate
        """
        # If the click is not too left on the screen
        if coord_x >= LEFT_SCREEN_LIMIT_X and\
                self.__new_coordinates[Y_COORDINATE] <= BOTTOM_LIMIT:
            return int((coord_x - LEFT_SCREEN_LIMIT_X) / GAP_BETWEEN_COLUMNS)
        else:
            return ILLEGAL_CLICK

    def __convert_column_to_coordinates(self, coordinates):
        """
        This method gets a tuple with two numbers from the "game" with a number
        of the row and a number of a column to place the new disc. THw method
        converts the two numbers inside the tuple to numbers that matches
        the location in the game that the disc should be created.
        :param coordinates: tuple, the "x" and "y" coordinates of the new disc
        :return: tuple with the right numbers that matches to the screen's location
        """
        coord_x = LEFT_SCREEN_LIMIT_X + coordinates[Y_COORDINATE] * GAP_BETWEEN_COLUMNS
        cord_y = LEFT_SCREEN_LIMIT_Y + GAP_BETWEEN_ROWS * coordinates[X_COORDINATE]
        new_coordinates = (coord_x, cord_y)
        return new_coordinates

    def __choose_color(self):
        """
        This method checks which player is playing in this current turn, and returns
        a string with the right color that represents his discs.
        :return: string, represents the player's color
        """
        if self.__game.get_current_player() == PLAYER_ONE:
            return PLAYER_TWO_COLOR
        return PLAYER_ONE_COLOR
