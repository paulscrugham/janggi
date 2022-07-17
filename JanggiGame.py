# Author: Paul Scrugham
# Date: 3/11/2020
# Description: Portfolio Project - This program simulates the board game Janggi (or Korean chess) and allows players
#   to take turns moving their respective pieces until checkmate. The program consists of Piece, sub-Piece, and
#   JanggiGame classes with methods for initializing the board with pieces in their starting positions, finding all
#   possible moves for a piece, determining if a player is in check, and determining if a player is in checkmate.
#
#   The game will not allow a player to make a move if it is not their turn, if a move is not valid (breaks rules for
#   movement of the piece), if a move would put the current player in check, or if a player is in checkmate.
#
#   Once a player is in checkmate, the game_state will be updated to reflect which player won.

class Colors:
    """Contains colors for displaying the board in the console"""
    BLUE = '\033[94m'
    RED = '\033[31m'
    GREEN = '\033[100;30m'
    ENDC = '\033[0m'


class Piece:
    """
    Represents a base Piece object for specific piece types to inherit from. Contains data members and methods
    common to all pieces such as color, name, location, relative direction, and possible moves.
    """

    def __init__(self):
        self._color = None
        self._name = ""
        self._location = None
        self._direction = None
        self._possible_moves = []

    @staticmethod
    def _decode_pos(encoded_pos):
        """Returns the position of a piece in the format [char, num]"""
        return [ord(encoded_pos[0]), int(encoded_pos[1:])]

    @staticmethod
    def _encode_pos(decoded_pos):
        """Takes a decoded position [char, num] and returns an encoded position"""
        return str(chr(decoded_pos[0])) + str(decoded_pos[1])

    def get_name(self):
        """Returns the name of a piece as a string"""
        return self._name

    def set_color(self, color):
        """Sets the color of a piece to a string ('blue' or 'red')"""
        self._color = color

    def set_direction(self, direction):
        """Sets the relative direction of a piece"""
        self._direction = direction

    def get_direction(self):
        """Returns the relative direction of a piece"""
        return self._direction

    def get_color(self):
        """Returns the color of a piece as a string ('blue' or 'red')"""
        return self._color

    def get_location(self):
        """Returns the location of a piece in algebraic notation (e.g. 'a1')"""
        return self._location

    def set_location(self, loc):
        """Sets the location of a piece provided a coordinate in algebraic notation (e.g. 'a1')"""
        self._location = loc

    def get_possible_moves(self):
        """Returns the list of positions a piece could possibly move to"""
        return self._possible_moves


class Soldier(Piece):
    """Represents a Soldier object inheriting from the Piece class"""

    def __init__(self):
        """Returns a Soldier object"""
        super().__init__()
        self._name = "So"

    def _test_destinations(self, decoded, board):
        """Soldier specific tests for finding whether a Soldier can move to the specified location"""
        encoded = self._encode_pos(decoded)
        if board[encoded] is None:
            self._possible_moves.append(encoded)
        elif board[encoded].get_color() != self._color:
            self._possible_moves.append(encoded)

    def find_moves(self, board, palaces):
        """Finds all possible moves for a Soldier piece given its position and the state of the board"""
        self._possible_moves = []

        # no move (pass turn)
        self._possible_moves.append(self._location)

        # left move
        decoded = self._decode_pos(self._location)
        if decoded[0] > ord('a'):
            decoded[0] -= 1
            # test if a piece of opposing color is in target location
            self._test_destinations(decoded, board)

        # right move
        decoded = self._decode_pos(self._location)
        if decoded[0] < ord('i'):
            decoded[0] += 1
            # test if a piece of opposing color is in target location
            self._test_destinations(decoded, board)

        # forward move
        decoded = self._decode_pos(self._location)
        if 1 < decoded[1] < 10:
            decoded[1] += 1 * self._direction
            # test if a piece of opposing color is in target location
            self._test_destinations(decoded, board)

        # ------diagonal palace movement------
        if self._color == 'red':  # soldier can never be in it's own palace
            palace_center = palaces['blue_palace_center']
            palace_corners = palaces['blue_palace_corners']
        else:
            palace_center = palaces['red_palace_center']
            palace_corners = palaces['red_palace_corners']

        # if piece is on palace corner
        if self._location in palace_corners:
            decoded = self._decode_pos(self._location)
            if self._decode_pos(palace_center)[1] == decoded[1] + 1 * self._direction:
                if board[palace_center] is None:
                    self._possible_moves.append(palace_center)
                elif board[palace_center].get_color() != self._color:
                    self._possible_moves.append(palace_center)

        # if piece is in palace center
        if self._location == palace_center:
            decoded = self._decode_pos(self._location)
            for corner in palace_corners:
                if self._decode_pos(corner)[1] == decoded[1] + 1 * self._direction:
                    if board[corner] is None:
                        self._possible_moves.append(corner)
                    elif board[corner].get_color() != self._color:
                        self._possible_moves.append(corner)


class Cannon(Piece):
    """Represents a Cannon object inheriting from the Piece class"""

    def __init__(self):
        """Returns a Cannon object"""
        super().__init__()
        self._name = 'Ca'

    def _test_destinations(self, decoded, axis, direction, board):
        """Cannon specific tests for finding whether a Cannon can move to the specified location"""
        intervening_found = False
        end_found = False
        while not intervening_found or not end_found:
            decoded[axis] += 1 * direction
            encoded = self._encode_pos(decoded)

            # test if decoded position has gone beyond board bounds
            if encoded not in board.keys():
                return

            if intervening_found:
                if board[encoded] is None:
                    self._possible_moves.append(encoded)
                elif board[encoded].get_name() == 'Ca':  # cannon cannot jump over a cannon
                    return
                elif board[encoded].get_color() != self._color:
                    self._possible_moves.append(encoded)
                    return
                else:
                    return

            if board[encoded] is not None:
                if board[encoded].get_name() == 'Ca':  # cannon cannot capture a cannon
                    return
                intervening_found = True

    def find_moves(self, board, palaces):
        """Finds all possible moves for a Cannon piece given its position and the state of the board"""
        self._possible_moves = []

        # no move (pass turn)
        self._possible_moves.append(self._location)

        # iterate forward (relative)
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, self._direction, board)

        # iterate backward (relative)
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, self._direction * -1, board)

        # iterate right
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, self._direction, board)

        # iterate left
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, self._direction * -1, board)

        # ------diagonal palace movement------
        if self._location in palaces['blue_palace_corners']:
            palace_center = palaces['blue_palace_center']
            palace_corners = palaces['blue_palace_corners']
        else:
            palace_center = palaces['red_palace_center']
            palace_corners = palaces['red_palace_corners']

        # palace-specific movement for cannons consists of jumping diagonally across the center
        if self._location in palace_corners:
            if board[palace_center] is not None:
                decoded_loc = self._decode_pos(self._location)
                decoded_center = self._decode_pos(palace_center)

                # find the opposite corner
                if decoded_loc[0] - decoded_center[0] == 1:
                    decoded_loc[0] -= 2
                else:
                    decoded_loc[0] += 2

                if decoded_loc[1] - decoded_center[1] == 1:
                    decoded_loc[1] -= 2
                else:
                    decoded_loc[1] += 2

                # add diagonal jump if destination is empty or contains piece of opposing color
                encoded = self._encode_pos(decoded_loc)
                if board[encoded] is None:
                    self._possible_moves.append(encoded)
                elif board[encoded].get_color() != self._color:
                    self._possible_moves.append(encoded)


class Chariot(Piece):
    """Represents a Chariot object inheriting from the Piece class"""

    def __init__(self):
        """Returns a Chariot object"""
        super().__init__()
        self._name = "Ch"

    def _test_destinations(self, decoded, axis, direction, board):
        """Chariot specific tests for finding whether a Chariot can move to the specified location"""
        end_found = False
        while not end_found:
            decoded[axis] += 1 * direction
            encoded = self._encode_pos(decoded)

            # test if decoded position has gone beyond board bounds
            if encoded not in board.keys():
                return

            if board[encoded] is None:
                self._possible_moves.append(encoded)
            elif board[encoded].get_color() != self._color:
                self._possible_moves.append(encoded)
                return
            else:
                return

    def find_moves(self, board, palaces):
        """Finds all possible moves for a Chariot piece given its position and the state of the board"""
        self._possible_moves = []

        # no move (pass turn)
        self._possible_moves.append(self._location)

        # ------normal board movement------
        # iterate forward (relative)
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, self._direction, board)

        # iterate backward (relative)
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, self._direction * -1, board)

        # iterate right
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, self._direction, board)

        # iterate left
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, self._direction * -1, board)

        # ------diagonal palace movement------
        if self._location in palaces['blue_palace_corners']:
            palace_center = palaces['blue_palace_center']
            palace_corners = palaces['blue_palace_corners']
        else:
            palace_center = palaces['red_palace_center']
            palace_corners = palaces['red_palace_corners']

        # test for movement from a palace corner
        if self._location in palace_corners:
            decoded_loc = self._decode_pos(self._location)
            decoded_center = self._decode_pos(palace_center)

            # test center of palace
            if board[palace_center] is None:
                self._possible_moves.append(palace_center)
            elif board[palace_center].get_color() != self._color:
                self._possible_moves.append(palace_center)

            # test opposite corner of palace
            if decoded_loc[0] - decoded_center[0] == 1:
                decoded_loc[0] -= 2
            else:
                decoded_loc[0] += 2

            if decoded_loc[1] - decoded_center[1] == 1:
                decoded_loc[1] -= 2
            else:
                decoded_loc[1] += 2

            encoded = self._encode_pos(decoded_loc)
            if board[encoded] is None:
                self._possible_moves.append(encoded)
            elif board[encoded].get_color() != self._color:
                self._possible_moves.append(encoded)

        # test for movement from palace center
        elif self._location == palace_center:
            for corner in palace_corners:
                if board[corner] is None:
                    self._possible_moves.append(corner)
                elif board[corner].get_color() != self._color:
                    self._possible_moves.append(corner)


class Elephant(Piece):
    """Represents a Elephant object inheriting from the Piece class"""

    def __init__(self):
        """Returns an Elephant object"""
        super().__init__()
        self._name = "El"

    def _test_destinations(self, decoded, first_axis, second_axis, first_direction, second_direction, board):
        """Elephant specific tests for finding whether an Elephant can move to the specified location"""

        # orthogonal move
        decoded[first_axis] += 1 * first_direction

        # test if decoded position has gone beyond board bounds
        encoded = self._encode_pos(decoded)
        if encoded not in board.keys():
            return

        if board[encoded] is not None:
            return

        # first diagonal move
        decoded[first_axis] += 1 * first_direction
        decoded[second_axis] += second_direction

        # test if decoded position has gone beyond board bounds
        encoded = self._encode_pos(decoded)
        if encoded not in board.keys():
            return
        # test for intervening piece
        elif board[encoded] is not None:
            return

        # second diagonal move
        decoded[first_axis] += 1 * first_direction
        decoded[second_axis] += second_direction

        # test if decoded position has gone beyond board bounds
        encoded = self._encode_pos(decoded)
        if encoded not in board.keys():
            return

        # check if target position is occupied
        if board[encoded] is None:
            self._possible_moves.append(encoded)
            return
        elif board[encoded].get_color() != self._color:
            self._possible_moves.append(encoded)
            return
        else:
            return

    def find_moves(self, board, *palaces):  # no palace-specific movement for Elephants
        """Finds all possible moves for a Elephant piece given its position and the state of the board"""
        self._possible_moves = []

        # no move (pass turn)
        self._possible_moves.append(self._location)

        # move "forward" and left
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction, -1, board)

        # move "forward" and right
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction, 1, board)

        # move "backward" and left
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction * -1, -1, board)

        # move "backward" and right
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction * -1, 1, board)

        # move left and "forward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction, -1, board)

        # move left and "backward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction * -1, -1, board)

        # move right and "forward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction, 1, board)

        # move right and "backward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction * -1, 1, board)


class Horse(Piece):
    """Represents a Horse object inheriting from the Piece class"""

    def __init__(self):
        """Returns a Horse object"""
        super().__init__()
        self._name = "Ho"

    def _test_destinations(self, decoded, first_axis, second_axis, first_direction, second_direction, board):
        """Horse specific tests for finding whether a Horse can move to the specified location"""

        # orthogonal move
        decoded[first_axis] += 1 * first_direction

        # test if decoded position has gone beyond board bounds
        encoded = self._encode_pos(decoded)
        if encoded not in board.keys():
            return

        if board[encoded] is not None:
            return

        # diagonal move
        decoded[first_axis] += 1 * first_direction
        decoded[second_axis] += second_direction

        # test if decoded position has gone beyond board bounds
        encoded = self._encode_pos(decoded)
        if encoded not in board.keys():
            return

        # check if target position is occupied
        if board[encoded] is None:
            self._possible_moves.append(encoded)
            return
        elif board[encoded].get_color() != self._color:
            self._possible_moves.append(encoded)
            return
        else:
            return

    def find_moves(self, board, *palaces):  # no palace-specific movement for Horses
        """Finds all possible moves for a Horse piece given its position and the state of the board"""
        self._possible_moves = []

        # no move (pass turn)
        self._possible_moves.append(self._location)

        # move "forward" and left
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction, -1, board)

        # move "forward" and right
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction, 1, board)

        # move "backward" and left
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction * -1, -1, board)

        # move "backward" and right
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction * -1, 1, board)

        # move left and "forward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction, -1, board)

        # move left and "backward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction * -1, -1, board)

        # move right and "forward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction, 1, board)

        # move right and "backward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction * -1, 1, board)


class Guard(Piece):
    """Represents a Guard object inheriting from the Piece class"""

    def __init__(self):
        """Returns a Guard object"""
        super().__init__()
        self._name = "Gu"

    def _test_destinations(self, decoded, x_distance, y_distance, direction, board, palaces):
        """Guard specific tests for finding whether a Guard can move to the specified location"""

        decoded[0] += x_distance * direction
        decoded[1] += y_distance * direction

        # test if decoded position is in the palace
        encoded = self._encode_pos(decoded)
        if self._color == 'red':
            palace = palaces['red_palace']
        else:
            palace = palaces['blue_palace']

        if encoded in palace:

            if board[encoded] is None:
                self._possible_moves.append(encoded)
            elif board[encoded].get_color() != self._color:
                self._possible_moves.append(encoded)
            else:
                return
        else:
            return

    def find_moves(self, board, palaces):
        """Finds all possible moves for a Guard piece given its position and the state of the board"""
        self._possible_moves = []

        # ------orthogonal moves------
        # no move (pass turn)
        self._possible_moves.append(self._location)

        # move "forward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction, board, palaces)

        # move "backward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction * -1, board, palaces)

        # move left
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, -1, 0, self._direction, board, palaces)

        # move right
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction, board, palaces)

        # ------diagonal palace movement------
        if self._color == 'red':
            palace_center = palaces['red_palace_center']
            palace_corners = palaces['red_palace_corners']
        else:
            palace_center = palaces['blue_palace_center']
            palace_corners = palaces['blue_palace_corners']

        # if guard piece is on palace corner
        if self._location in palace_corners:
            if board[palace_center] is None:
                self._possible_moves.append(palace_center)
            elif board[palace_center].get_color() != self._color:
                self._possible_moves.append(palace_center)

        # if guard piece is in palace center
        if self._location == palace_center:
            for corner in palace_corners:
                if board[corner] is None:
                    self._possible_moves.append(corner)
                elif board[corner].get_color() != self._color:
                    self._possible_moves.append(corner)


class General(Piece):
    """Represents a General object inheriting from the Piece class"""

    def __init__(self):
        """Returns a General object"""
        super().__init__()
        self._name = "Ge"

    def _test_destinations(self, decoded, x_distance, y_distance, direction, board, palaces):
        """General specific tests for finding whether a General can move to the specified location"""

        decoded[0] += x_distance * direction
        decoded[1] += y_distance * direction

        # test if decoded position is in the palace
        encoded = self._encode_pos(decoded)
        if self._color == 'red':
            palace = palaces['red_palace']
        else:
            palace = palaces['blue_palace']

        if encoded in palace:

            if board[encoded] is None:
                self._possible_moves.append(encoded)
            elif board[encoded].get_color() != self._color:
                self._possible_moves.append(encoded)
            else:
                return
        else:
            return

    def find_moves(self, board, palaces):
        """Finds all possible moves for a General piece given its position and the state of the board"""
        self._possible_moves = []

        # ------orthogonal moves------
        # no move (pass turn)
        self._possible_moves.append(self._location)

        # move "forward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction, board, palaces)

        # move "backward"
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 0, 1, self._direction * -1, board, palaces)

        # move left
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, -1, 0, self._direction, board, palaces)

        # move right
        decoded = self._decode_pos(self._location)
        self._test_destinations(decoded, 1, 0, self._direction, board, palaces)

        # ------diagonal palace movement------
        if self._color == 'red':
            palace_center = palaces['red_palace_center']
            palace_corners = palaces['red_palace_corners']
        else:
            palace_center = palaces['blue_palace_center']
            palace_corners = palaces['blue_palace_corners']

        # if General piece is on palace corner
        if self._location in palace_corners:
            if board[palace_center] is None:
                self._possible_moves.append(palace_center)
            elif board[palace_center].get_color() != self._color:
                self._possible_moves.append(palace_center)

        # if General piece is in palace center
        if self._location == palace_center:
            for corner in palace_corners:
                if board[corner] is None:
                    self._possible_moves.append(corner)
                elif board[corner].get_color() != self._color:
                    self._possible_moves.append(corner)


class JanggiGame:
    """
    Represents a Janggi game object that initializes a game object, initializes a board object, and contains
    methods for moving pieces, determining if a player is in check, and showing the game state (unfinished,
    blue wins, or red wins).
    """

    def __init__(self):
        """Returns a JanggiGame object with methods for moving pieces and determining the game state"""
        self._game_state = "UNFINISHED"
        self._turn = 'blue'
        self._check = False
        self._current_move = 0
        self._positions = {}

        self._init_positions = {'red_soldier': ['a4', 'c4', 'e4', 'g4', 'i4'],
                                'blue_soldier': ['a7', 'c7', 'e7', 'g7', 'i7'],
                                'red_cannon': ['b3', 'h3'],
                                'blue_cannon': ['b8', 'h8'],
                                'red_chariot': ['a1', 'i1'],
                                'blue_chariot': ['a10', 'i10'],
                                'red_elephant': ['b1', 'g1'],
                                'blue_elephant': ['b10', 'g10'],
                                'red_horse': ['c1', 'h1'],
                                'blue_horse': ['c10', 'h10'],
                                'red_guard': ['d1', 'f1'],
                                'blue_guard': ['d10', 'f10'],
                                'red_general': ['e2'],
                                'blue_general': ['e9']}

        self._palaces = {'red_palace': ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3'],
                         'red_palace_center': 'e2',
                         'red_palace_corners': ['d1', 'd3', 'f1', 'f3'],
                         'blue_palace': ['d8', 'd9', 'd10', 'e8', 'e9', 'e10', 'f8', 'f9', 'f10'],
                         'blue_palace_center': 'e9',
                         'blue_palace_corners': ['d8', 'd10', 'f8', 'f10']}

        # fill board with pieces at their starting locations when game object is initialized
        def init_piece_type(init_list, piece_type, color):
            for position in init_list:
                piece = piece_type()
                piece.set_color(color)
                piece.set_location(position)
                self._positions[position] = piece

                # set piece direction based on color
                if color == 'red':
                    piece.set_direction(1)
                else:
                    piece.set_direction(-1)

        # nested loop to initialize the board dictionary
        for num in range(1, 11):
            for char in range(97, 106):
                self._positions[chr(char) + str(num)] = None

        # initialize soldiers
        init_piece_type(self._init_positions['red_soldier'], Soldier, 'red')
        init_piece_type(self._init_positions['blue_soldier'], Soldier, 'blue')

        # initialize cannons
        init_piece_type(self._init_positions['red_cannon'], Cannon, 'red')
        init_piece_type(self._init_positions['blue_cannon'], Cannon, 'blue')

        # initialize chariots
        init_piece_type(self._init_positions['red_chariot'], Chariot, 'red')
        init_piece_type(self._init_positions['blue_chariot'], Chariot, 'blue')

        # initialize elephants
        init_piece_type(self._init_positions['red_elephant'], Elephant, 'red')
        init_piece_type(self._init_positions['blue_elephant'], Elephant, 'blue')

        # initialize horses
        init_piece_type(self._init_positions['red_horse'], Horse, 'red')
        init_piece_type(self._init_positions['blue_horse'], Horse, 'blue')

        # initialize guards
        init_piece_type(self._init_positions['red_guard'], Guard, 'red')
        init_piece_type(self._init_positions['blue_guard'], Guard, 'blue')

        # initialize generals
        init_piece_type(self._init_positions['red_general'], General, 'red')
        init_piece_type(self._init_positions['blue_general'], General, 'blue')

    def get_positions(self):
        """Returns the dictionary representing current piece positions"""
        return self._positions

    def get_palaces(self):
        """Returns the dictionary representing palace coordinates"""
        return self._palaces

    def is_in_check(self, player):
        """
        Determines if a player is in check by comparing their General's position to possible positions
        of the opposing player's pieces. Returns True if in check, False if not.
        """
        if player == 'red':
            opp_player = 'blue'
        else:
            opp_player = 'red'

        for position in self._positions:
            if self._positions[position] is not None:
                if self._positions[position].get_color() == opp_player:
                    # find all possible moves of an opposing piece
                    self._positions[position].find_moves(self._positions, self._palaces)

                    # search for a General piece in a piece's possible moves
                    for move in self._positions[position].get_possible_moves():
                        if self._positions[move] is not None:
                            if self._positions[move].get_name() == 'Ge':
                                if self._positions[move].get_color() == player:
                                    return True
        return False

    def is_in_checkmate(self, player):
        """Determines if a player is in checkmate by testing all possible moves"""
        for position in self._positions:
            piece = self._positions[position]
            if piece is not None:
                if piece.get_color() == player:
                    piece.find_moves(self._positions, self._palaces)
                    test_moves = piece.get_possible_moves()

                    # test for check in each possible move of a piece
                    for move in test_moves:
                        saved_board = self._positions.copy()  # save current board to test move
                        self.update_position(piece, piece.get_location(), move)
                        check_test = self.is_in_check(self._turn)
                        self._positions = saved_board  # restore board
                        piece.set_location(position)  # restore piece location
                        if check_test is False:
                            return False
        return True

    def update_position(self, piece, source, destination):
        """Updates a piece's position on the board"""
        positions = self._positions
        positions[destination] = positions[source]
        piece.set_location(destination)  # update piece's location data member

        # set source position to None if non-passing move
        if source != destination:
            positions[source] = None

    def make_move(self, source, destination):
        """
        If a valid move, modifies a position in a Board object's dictionary. Movement validity is determined
        using the is_in_check and is_in_checkmate methods. Returns True if a piece is moved successfully, False if not.
        """
        print("Attempting: ", source, "->", destination)

        # get board
        positions = self._positions

        # check if source position has a piece and that the piece is the current player's turn
        if positions[source] is not None:
            if positions[source].get_color() == self._turn:
                piece = positions[source]
            else:
                return False
        else:
            return False

        # calculate all possible moves for the provided piece
        piece.find_moves(positions, self._palaces)

        # check if destination is in provided piece's possible_moves list
        if destination in piece.get_possible_moves():
            # check if movement will put current player in check
            saved_board = positions.copy()  # save current board to test move
            self.update_position(piece, source, destination)
            check_test = self.is_in_check(self._turn)

            if check_test is True:
                self._positions = saved_board  # restore board
                return False

            # increment turn counter for display purposes
            self._current_move += 1

            # update turn to next player
            if self._turn == 'blue':
                self._turn = 'red'
            else:
                self._turn = 'blue'

            # find if next player is in check
            if self.is_in_check(self._turn):
                self._check = True
            else:
                self._check = False

            # if next player is in check, evaluate checkmate scenario
            if self._check:
                checkmate_test = self.is_in_checkmate(self._turn)
                if checkmate_test:
                    if self._turn == 'red':
                        self._game_state = 'BLUE_WON'
                    else:
                        self._game_state = 'RED_WON'

            return True
        else:
            return False

    def get_game_state(self):
        """Returns the state of the game as a string (can be UNFINISHED, BLUE WINS, or RED WINS)"""
        return self._game_state

    def display_board(self):
        """Prints the board and current piece locations to the console"""
        if self._turn == 'red':
            turn = 'Red'
        else:
            turn = 'Blue'

        print()
        print("Move " + str(self._current_move) + " - " + turn)
        print(end="     ")

        for char in range(97, 106):
            print(chr(char), end='    ')
        print()

        for count, key in enumerate(self._positions):
            if count % 9 == 0 and count != 0:
                print()

            if self._positions[key] is None:
                name = ' ___ '
            else:
                name = " " + str(self._positions[key].get_color()[0]) + str(self._positions[key].get_name()) + " "
            if count % 9 == 0:
                if key[1:] == '10':
                    print(key[1:], end=' ')
                else:
                    print(" " + key[1:], end=' ')
            if self._positions[key] is None:
                print(Colors.GREEN + name + Colors.ENDC, end='')
            elif self._positions[key].get_color() == 'red':
                print(Colors.RED + name + Colors.ENDC, end='')
            else:
                print(Colors.BLUE + name + Colors.ENDC, end='')
        print()
        print()


def main():
    game = JanggiGame()
    
    player_input = ''

    while player_input != 'exit':
        game.display_board()
        state = game.get_game_state()
        if state == 'UNFINISHED':
            if game.is_in_check('red'):
                print('Red player is in check')
            if game.is_in_check('blue'):
                print('Blue player is in check')
            first_move = input('Enter a position to move from: ')
            second_move = input('Enter a position to move to: ')
            game.make_move(first_move, second_move)
        else:
            print(state)
            break


    print('The game is now exiting')


if __name__ == '__main__':
    main()
