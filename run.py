"""Line Mine Sweeper"""

# region Imports
import os
from random import randint
from readchar import readkey
from colorama import init, Fore

# endregion


# region Global Variables
TITLE = "  LINE MINE SWEEPER!!  "
WINDOW_WIDTH = 80
MINE_VAL = -1
DEFAULT_SETTINGS = [6, 10]

# endregion


# region Game Board Class
class Board:
    """
    Minesweeper game class.
    """

    size = 0
    mines = 0
    grid_hidden = []
    grid_visable = []

    def __init__(self, settings):
        self.size = settings[0]
        self.mines = settings[1]
        self.create_grids()
        self.create_mines()
        self.set_numbers()

    def create_grids(self):
        """
        Creates both the hidden and visable grids as nested lists.
        Fills the newly created hidden grid with 0's.
        Fills the newly created visable grid with spaces.
        """

        self.grid_hidden = [
            [0 for column in range(self.size)] for row in range(self.size)
        ]
        self.grid_visable = [
            [" " for column in range(self.size)] for row in range(self.size)
        ]

    def draw_board(self):
        """
        Adds stylings to each row of the visable grid.
        Prints out visable grid row by row, using center_line function.
        """

        print_title()

        heading_top = (
            "".join(["|  " + str(i + 1) + "  " for i in range(self.size)]) +
            "|"
        )
        print(set_color(center_line(heading_top), Fore.CYAN))

        for i, row in enumerate(self.grid_visable):
            new_line = ""

            if i == 0:
                new_line = set_color("\u203E ", Fore.CYAN, True)
                new_line = (
                    new_line +
                    "".join(
                        ["|\u203E\u203E\u203E\u203E\u203E" for cell in row]
                    ) +
                    "|   "
                )
            else:
                new_line = "  "
                new_line = (
                    new_line + "".join(["|     " for cell in row]) + "|  "
                )

            print(center_line(new_line))

            new_line = set_color(str(i + 1) + " ", Fore.CYAN, True)
            new_line = (
                new_line +
                "".join(["|  " + str(cell) + "  " for cell in row]) + "|  "
            )
            print(center_line(new_line))

            new_line = set_color("_ ", Fore.CYAN, True)
            new_line = new_line + "".join(["|_____" for cell in row]) + "|  "
            print(center_line(new_line))

    def create_mines(self):
        """
        Uses the random module to create random cell locations,
        Populates cells with mines, if they aren't already mines.
        """

        for _ in range(self.mines):
            while True:
                new_row = randint(0, self.size - 1)
                new_column = randint(0, self.size - 1)

                if self.grid_hidden[new_row][new_column] != MINE_VAL:
                    self.grid_hidden[new_row][new_column] = MINE_VAL
                    break

    def set_numbers(self):
        """
        Sets the correct numbers for each cell in the hidden grid.
        Checks each cell's neighboring cells for mines.
        Increases cell value if it is next to a mine.
        """
        for row in range(self.size):
            for col, cell in enumerate(self.grid_hidden[row]):
                if cell == MINE_VAL:
                    continue

                if row > 0:
                    if (
                        col > 0 and
                        self.grid_hidden[row - 1][col - 1] == MINE_VAL
                    ):
                        self.grid_hidden[row][col] += 1

                    if self.grid_hidden[row - 1][col] == MINE_VAL:
                        self.grid_hidden[row][col] += 1

                    if (
                        col < self.size - 1 and
                        self.grid_hidden[row - 1][col + 1] == MINE_VAL
                    ):
                        self.grid_hidden[row][col] += 1

                if col > 0 and self.grid_hidden[row][col - 1] == MINE_VAL:
                    self.grid_hidden[row][col] += 1
                if (
                    col < self.size - 1 and
                    self.grid_hidden[row][col + 1] == MINE_VAL
                ):
                    self.grid_hidden[row][col] += 1

                if row < self.size - 1:
                    if (
                        col > 0 and
                        self.grid_hidden[row + 1][col - 1] == MINE_VAL
                    ):
                        self.grid_hidden[row][col] += 1

                    if self.grid_hidden[row + 1][col] == MINE_VAL:
                        self.grid_hidden[row][col] += 1

                    if (
                        col < self.size - 1 and
                        self.grid_hidden[row + 1][col + 1] == MINE_VAL
                    ):
                        self.grid_hidden[row][col] += 1

    def user_input(self):
        """
        User input manager for game.
        Takes user's input,
        and runs appropriate function based on what is received.
        """

        selection = ["", "", ""]

        print(
            center_line("\b\bPlease enter coordinates: "),
            end="",
            flush=True
        )

        try:
            for i in range(2):
                selection[i] = readkey()

                if not selection[i].isdigit():
                    raise ValueError(
                        f"INVALID INPUT: {selection[i]} is not a number."
                    )

                if int(selection[i]) < 1 or int(selection[i]) > self.size:
                    raise ValueError(
                        f"INVALID INPUT: {selection[i]} is not on the board."
                    )

                print(selection[i] + ":", end="", flush=True)
                selection[i] = int(selection[i]) - 1

            selection[2] = readkey()

            if selection[2].lower() == "f":
                selection[2] = True
            elif selection[2] == "\r":
                selection[2] = False
            else:
                raise ValueError(
                    f"INVALID INPUT: {selection[2]} is not 'f/F' or ENTER."
                )

            return selection
        except ValueError as error:
            error_message(error)
            return None

    def update_board(self, selection):
        """
        Checks if coordinates have already been revealed,
        if not updates the visable board with the user's inputted coordinates.
        """

        row, col = selection[0], selection[1]
        flag = selection[2]
        value_hidden = self.grid_hidden[row][col]
        value_visable = self.grid_visable[row][col]

        if value_visable == " " or value_visable == "F":
            if flag:
                self.grid_visable[row][col] = (
                    "F" if self.grid_visable[row][col] == " " else " "
                )
            elif value_hidden == 0:
                self.update_neighbours(row, col)
            else:
                self.grid_visable[row][col] = value_hidden

        else:
            error_message(
                f"INVALID INPUT: {row + 1}:{col + 1}"
                f" has already been already revealed!"
            )

    def update_neighbours(self, row, col):
        """
        Checks neighbouring cells for 0 values,
        Addes them to the visable board if they are
        zero's adjasent to the starting cell.
        """

        if (
            self.grid_hidden[row][col] == 0 and
            self.grid_visable[row][col] == " "
        ):
            self.grid_visable[row][col] = 0

            if row > 0 and col > 0:
                self.update_neighbours(row - 1, col - 1)

            if row > 0:
                self.update_neighbours(row - 1, col)

            if row > 0 and col < self.size - 1:
                self.update_neighbours(row - 1, col + 1)

            if col > 0:
                self.update_neighbours(row, col - 1)

            if col < self.size - 1:
                self.update_neighbours(row, col + 1)

            if row < self.size - 1 and col > 0:
                self.update_neighbours(row + 1, col - 1)

            if row < self.size - 1:
                self.update_neighbours(row + 1, col)

            if row < self.size - 1 and col < self.size - 1:
                self.update_neighbours(row + 1, col + 1)

    def check_game_over(self):
        """
        Checks if the game should end.
        Checks if all mines have been flagged and
        if all other cells have been revealed.
        """

        if -1 in (cell for row in self.grid_visable for cell in row):
            draw_game_results(False)
            return False

        if " " in (cell for row in self.grid_visable for cell in row):
            return True

        if sum(row.count("F") for row in self.grid_visable) == self.mines:
            draw_game_results(True)
            return False

        return False


# endregion


# region Functions
def center_line(input_text):
    """
    Centers the given string based on the width of the terminal,
    set with the global WIDTH perameter.
    Splits the string by the new line operator,
    Applies the calculation to each substring.
    """

    output_text = ""

    for line in input_text.split("\n"):
        output_text += f"{' ' * int((WINDOW_WIDTH - len(line)) / 2)}{line}\n"

    return output_text[:-1]


def menu():
    """
    Menu generator.
    Creates a menu of options, and uses user input to set settings for game.
    Returns settings as list.
    """

    settings = [setting for setting in DEFAULT_SETTINGS]

    while True:
        print_title()

        print(
            center_line(
                f"\nWelcome to Line Mine Sweeper!!"
                f"\nPlease select your desired settings below:"
                f"\n\n1:"
                f"\nSet Game Size - Current: {settings[0]}X{settings[0]}"
                f"\n\n2:"
                f"\nSet Mine Count - Current: {settings[0]}"
                f"\n\n3:"
                f"\nShow Instructions"
                f"\n\nENTER:"
                f"\nStart Game!"
            )
        )

        if settings[1] > settings[0] * settings[0]:
            print(
                center_line(
                    "\n!!!MINE COUNT TOO HIGH!!!"
                    "\nPlease increase grid size, or decrease mine count!"
                )
            )

        try:
            print(
                center_line("\n\bPlease enter your selection: "),
                end="",
                flush=True,
            )
            selection = readkey()

            if selection == "1":
                print_title()
                print(
                    center_line(
                        "\nPlease enter your desired grid size."
                        "\nPlease enter a single number for grid size."
                        "(E.G. 5 = 5X5)')}"
                        "\nMinimum = 2 | Maximum = 7')}"
                        f"\nCurrent = {settings[0]} X {settings[0]}"
                    )
                )

                print(
                    center_line(
                        "\n\bPlease enter your selection: "
                    ),
                    end="",
                    flush=True,
                )
                selection = readkey()

                if not selection.isdigit():
                    raise ValueError(
                        f"INVALID INPUT: {selection} is not a number."
                    )
                if int(selection) < 2:
                    raise ValueError(f"INVALID INPUT: {selection} is too low.")
                if int(selection) > 7:
                    raise ValueError(
                        f"INVALID INPUT: {selection} is too high."
                    )

                settings[0] = int(selection)

            elif selection == "2":
                print_title()
                print(
                    center_line(
                        "\nPlease enter your desired mine count."
                        "\nPlease enter a whole number. (E.G. 5 OR 20)"
                        f"\nMinimum = 1 | Maximum = {settings[0] * settings[0]}"
                        f"\nCurrent Mines = {settings[1]}"
                    )
                )

                selection = input(
                    center_line("\n\bPlease enter your selection: ")
                )

                if not selection.isdigit():
                    raise ValueError(
                        f"INVALID INPUT: {selection} is not a number."
                    )
                if int(selection) < 1:
                    raise ValueError(f"INVALID INPUT: {selection} is too low.")
                if int(selection) > settings[0] * settings[0]:
                    raise ValueError(
                        f"INVALID INPUT: {selection} is too high."
                    )

                settings[1] = int(selection)

            elif selection == "3":
                draw_instructions()

            elif selection == "\r":
                if settings[1] > settings[0] * settings[0]:
                    raise ValueError(
                        "ERROR: Cannot start game. Too many mines."
                    )

                return settings

            else:
                raise ValueError(
                    f"UNKNOWN INPUT: {selection} is not an option."
                )
        except ValueError as error:
            error_message(error)


def error_message(error):
    """
    Formats and displays an error the program has encountered.
    Takes in the error as a string,
    and adjusts the terminal display to show it.
    """

    print_title()
    print(
        center_line(
            f"\n{set_color('ERROR HAS BEEN ENCOUNTERED!!!', Fore.YELLOW, True)}"
            f"\n\n{set_color(repr(str(error)), Fore.YELLOW, True)}"
            "\n\nPlease press any key to continue... "
        ),
        end="",
        flush=True,
    )
    readkey()


def print_title():
    """
    Clears the current screen.
    Prints title to terminal.
    Uses TITLE constant for title, and fills rest in with hashtags.
    """

    os.system("cls" if os.name in ["nt", "dos"] else "clear")

    new_line_section = "#" * int((WINDOW_WIDTH - len(TITLE)) / 2)
    print(
        set_color(f"{new_line_section}{TITLE}{new_line_section}", Fore.GREEN)
    )


def draw_game_results(winner):
    """
    Draws the game results screen,
    Displays Game Over if a mine was hit,
    Displays You Win! if all mines were found.
    """

    print_title()

    if winner:
        print(
            set_color(
                center_line(
                    "\n ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ "
                    "\n█░█▄─█▀▀▀█─▄█▄─▄█▄─▀█▄─▄█▄─▀█▄─▄█▄─▄▄─█▄─▄▄▀█░█"
                    "\n█▄██─█─█─█─███─███─█▄▀─███─█▄▀─███─▄█▀██─▄─▄█▄█"
                    "\n▀▄██▄▄▄█▄▄▄██▄▄▄█▄▄▄██▄▄█▄▄▄██▄▄█▄▄▄▄▄█▄▄█▄▄█▄▀"
                ),
                Fore.GREEN
            )
        )

        print(
            center_line(
                "\nYEAH!!!"
                "\n\nYou Found All The Mines!"
                "\n\nYou Won! :)"
                "\n\nPress Any Key To Continue... "
            ),
            end="",
            flush=True,
        )
    else:
        print(
            set_color(
                center_line(
                    "\n ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ "
                    "\n█░█─▄▄▄▄██▀▄─██▄─▀█▀─▄█▄─▄▄─███─▄▄─█▄─█─▄█▄─▄▄─█▄─▄▄▀█░█"
                    "\n█▄█─██▄─██─▀─███─█▄█─███─▄█▀███─██─██▄▀▄███─▄█▀██─▄─▄█▄█"
                    "\n▀▄█▄▄▄▄▄█▄▄█▄▄█▄▄▄█▄▄▄█▄▄▄▄▄███▄▄▄▄███▄███▄▄▄▄▄█▄▄█▄▄█▄▀"
                ),
                Fore.RED
            )
        )

        print(
            center_line(
                "\nOH NO!!!"
                "\n\nYou Hit A Mine!"
                "\n\nBetter Luck Next Time :)"
                "\n\nPress Any Key To Continue..."
            ),
            end="",
            flush=True,
        )

    readkey()


def set_color(text, color, shift=False):
    """
    Adds supplied color index to supplied string.
    """

    return (
        f"          {color}{text}{Fore.RESET}"
        if shift
        else f"{color}{text}{Fore.RESET}"
    )


def draw_instructions():
    """
    Prints the instructions for the game to the terminal,
    Waits for any user input before continuing.
    """

    print_title()
    print(
        center_line(
            "\nInstructions!"
            "\n\nAim Of The Game!"
            "\nThe aim of the game is to flag all of the mines in the grid,"
            "\nand reveal all non-mine spaces. To Win the game, all mines"
            "\nhave to be flagged, "
            "and all non-mine spaces have to be revealed."
            "\n\nPress any key to continue... "),
        end="",
        flush=True
    )
    readkey()

    print(
        center_line(
            "\n\nHow To Play!"
            "\nTo select a space, enter the row number first, then the column,"
            "\nthen press f to flag the space, or ENTER to reveal the space."
            "\nE.G. 2:5:f"
            "\n\nPress any key to continue... "),
        end="",
        flush=True
    )
    readkey()


# endregion


# region Main
def main():
    """
    Main function
    """

    while True:
        game = Board(menu())

        while game.check_game_over():
            game.draw_board()

            user_input = game.user_input()

            if user_input is not None:
                game.update_board(user_input)


init()
main()

# endregion
