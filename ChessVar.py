# Author: Helen C
# GitHub username: hchao7
# Date: 3/04/24
# Description: Chess game simulator, with Falcon and Hunter added

class Player:
    """Responsibility: A class with methods for keeping track of each Player's reserve pieces
       Communicates with:
       ChessVar class — two instances of Player (white-piece player, black-piece player)
       are declared as private members in ChessVar
    """

    def __init__(self, reserve_list):
        self._reserve_list = reserve_list
        self._fairy_piece_entry = False
        self._capture_count = 0

    def set_capture_count(self, capture_count):
        """
        Purpose: Sets self._capture_count
        Parameters: capture_count (integer)
        Return value: None
        """
        self._capture_count = capture_count

    def get_capture_count(self):
        """
        Purpose: Retrieves self._capture_count
        Parameters: None
        Return value: self._capture_count
        """
        return self._capture_count

    def update_capture_count(self, value):
        """
        Purpose: Either subtracts or adds one to capture_count
                 Called by ClassVar's make_move and enter_fairy_piece method
                 adds one: if Queen, Rook, Bishop, or Knight is captured, add one
                 subtracts one: if a fairy piece is used, subtract one
        Parameters: value (either +1 or -1),
        Return value: None
        """
        self._capture_count = self._capture_count + value

    def update_fairy_piece_entry(self):
        """
        Purpose: Determines if self._fairy_piece_entry should be changed
                 Called by ClassVar's make_move and enter_fairy_piece method
        Parameters: None
        Return value: None
        """
        # All fairy pieces in use
        if not self._reserve_list:
            self._fairy_piece_entry = False

        # No main pieces captured
        elif self._capture_count == 0:
            self._fairy_piece_entry = False

        # Main pieces captured
        elif self._capture_count > 0:
            self._fairy_piece_entry = True

    def set_reserve_list(self, reserve_list):
        """
        Purpose: Sets self._reserve_list
        Parameters: reserve_list (a list)
        Return value: None
        """
        self._reserve_list = reserve_list

    def get_reserve_list(self):
        """
        Purpose: Gets self._reserve_list
        Parameters: None
        Return value: self._reserve_list
        """
        return self._reserve_list

    def remove_from_reserve_list(self, fairy_piece):
        """
        Purpose: Removes fairy piece from reserve list
        Parameters: fairy_piece
        Return value: None
        """
        self._reserve_list.remove(fairy_piece)

    def set_fairy_piece_entry(self, fairy_piece_entry):
        self._fairy_piece_entry = fairy_piece_entry

    def get_fairy_piece_entry(self):
        """
        Purpose: Retrieves self._fairy_piece_entry
        Parameters: None
        Return value: None
        """
        return self._fairy_piece_entry

class Pieces:
    """Responsibility: A class with static methods that determine
                       the validity of moves for all pieces
       Communicates with:
       ChessVar class — an instance of Pieces is declared as a private member in ChessVar to determine if
       a move entered by the player is valid
       Board class — several Piece methods accept an instance of Board as an argument
    """

    def is_valid_move_for_king(self, alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Purpose: Determines if it is valid for king to move to alg_end_coordinate
        Parameters: alg_start_coordinate (king's current position),
                    alg_end_coordinate (king's potential end position),
                    board (instance of Board class)
        Return value: True (move is valid) / False (move is invalid)
        """
        board = chess_var.get_board()
        direction = self.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Invalid direction
        if direction == 'N/A':
            return False

        # Converts algebraic coordinates to list indexes
        start_list_index = board.alg_coordinate_to_list_index(alg_start_coordinate)
        start_row, start_column = start_list_index[0], start_list_index[1]
        end_list_index = board.alg_coordinate_to_list_index(alg_end_coordinate)
        end_row, end_column = end_list_index[0], end_list_index[1]

        row_difference = abs(end_row - start_row)
        column_difference = abs(end_column - start_column)

        # Distance traveled
        sum_of_difference = row_difference + column_difference

        # King travels in a valid direction, check distance traveled
        if (direction in ["NORTH", "EAST", "SOUTH", "WEST"]) & (sum_of_difference == 1):
            return True
        elif (direction in ["NORTHEAST", "SOUTHEAST", "SOUTHWEST", "NORTHWEST"]) & (sum_of_difference == 2):
            return True

        return False

    def is_valid_move_for_queen(self, alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Purpose: Determines if it is valid for queen to move to alg_end_coordinate
        Parameters: alg_start_coordinate (queen's current position),
                    alg_end_coordinate (queen's potential end position),
                    board (instance of Board class)
        Return value: True (move is valid) / False (move is invalid)
        """
        board = chess_var.get_board()
        direction = self.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Invalid direction
        if direction == 'N/A':
            return False
        open_path = self.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)

        # Path is blocked
        if open_path is False:
            return False

        return True

    def is_valid_move_for_rook(self, alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Purpose: Determines if it is valid for rook to move to alg_end_coordinate
        Parameters: alg_start_coordinate (rook's current position),
                    alg_end_coordinate (rook's potential end position), board (instance of Board class)
        Return value: True (move is valid) / False (move is invalid)
        """
        board = chess_var.get_board()
        direction = self.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Invalid direction
        if direction not in ['NORTH', 'SOUTH', 'EAST', 'WEST']:
            return False
        open_path = self.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)

        # Path is blocked
        if open_path is False:
            return False

        return True

    def is_valid_move_for_bishop(self, alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Purpose: Determines if it is valid for bishop to move to alg_end_coordinate
        Parameters: alg_start_coordinate (bishop's current position),
                    alg_end_coordinate (bishop's potential end position), board (instance of Board class)
        Return value: True (move is valid) / False (move is invalid)
        """
        board = chess_var.get_board()
        direction = self.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Invalid direction
        if direction not in ['NORTHEAST', 'SOUTHWEST', 'NORTHWEST', 'SOUTHEAST']:
            return False

        # Path is blocked
        open_path = self.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
        if open_path is False:
            return False

        return True

    def is_valid_move_for_knight(self, alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Purpose: Determines if it is valid for knight to move to alg_end_coordinate
        Parameters: alg_start_coordinate (knight's current position),
                    alg_end_coordinate (knight's potential end position), board (instance of Board class)
        Return value: True (move is valid) / False (move is invalid)
        """
        board = chess_var.get_board()
        # Converts algebraic coordinates to list indexes
        start_list_index = board.alg_coordinate_to_list_index(alg_start_coordinate)
        start_row, start_column = start_list_index[0], start_list_index[1]
        end_list_index = board.alg_coordinate_to_list_index(alg_end_coordinate)
        end_row, end_column = end_list_index[0], end_list_index[1]

        row_difference = abs(end_row - start_row)
        column_difference = abs(end_column - start_column)

        # Check that distance traveled is valid
        if (row_difference == 2) & (column_difference == 1):
            return True
        elif (row_difference == 1) & (column_difference == 2):
            return True

        return False

    def is_valid_move_for_pawn(self, alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Purpose: Determines if it is valid for pawn to move to alg_end_coordinate
        Parameters: alg_start_coordinate (pawn's current position),
                    alg_end_coordinate (pawn's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        board = chess_var.get_board()
        player_turn = chess_var.get_player_turn()
        if player_turn == "WHITE":
            return self.is_valid_move_for_pawn_white(alg_start_coordinate, alg_end_coordinate, board)
        else:
            return self.is_valid_move_for_pawn_black(alg_start_coordinate, alg_end_coordinate, board)


    def is_valid_move_for_pawn_black(self, alg_start_coordinate, alg_end_coordinate, board):
        """
        Purpose: Determines if it is valid for WHITE pawn to move to alg_end_coordinate
        Parameters: alg_start_coordinate (pawn's current position),
                    alg_end_coordinate (pawn's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        start_list_index = board.alg_coordinate_to_list_index(alg_start_coordinate)
        start_row = start_list_index[0]
        start_column = start_list_index[1]

        end_list_index = board.alg_coordinate_to_list_index(alg_end_coordinate)
        end_row = end_list_index[0]
        end_column = end_list_index[1]

        row_difference = abs(end_row - start_row)
        col_difference = abs(end_column - start_column)
        total_difference = row_difference + col_difference
        direction = self.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Check for valid non-capture: valid direction, distance, and end position
        if direction == "SOUTH":
            open_end_position = board.get_piece_with_list_index(end_list_index)

            # Check that distance traveled is valid & pawn is NOT capturing
            # 1. Pawn starting on home rank
            if (row_difference == 2) & (start_row == 1) & (open_end_position == "."):
                open_path = self.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
                if open_path is True:
                    return True

            # 2. Pawn starting on non-home rank
            if (row_difference == 1) & (open_end_position == "."):
                return True

        # Check for valid capture: valid direction, distance, and end position
        if (direction == "SOUTHEAST") | (direction == "SOUTHWEST"):
            occupied_end_position = board.get_piece_with_list_index(end_list_index)
            if (occupied_end_position != ".") & (total_difference == 2):
                return True

        return False

    def is_valid_move_for_pawn_white(self, alg_start_coordinate, alg_end_coordinate, board):
        """
        Purpose: Determines if it is valid for WHITE pawn to move to alg_end_coordinate
        Parameters: alg_start_coordinate (pawn's current position),
                    alg_end_coordinate (pawn's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        start_list_index = board.alg_coordinate_to_list_index(alg_start_coordinate)
        start_row = start_list_index[0]
        start_column = start_list_index[1]

        end_list_index = board.alg_coordinate_to_list_index(alg_end_coordinate)
        end_row = end_list_index[0]
        end_column = end_list_index[1]

        row_difference = abs(end_row - start_row)
        col_difference = abs(end_column - start_column)
        total_difference = row_difference + col_difference
        direction = self.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Check for valid non-capture: valid direction, distance, and end position
        if direction == "NORTH":
            open_end_position = board.get_piece_with_list_index(end_list_index)

            # Check that distance traveled is valid & pawn is NOT capturing
            # 1. Pawn starting on home rank
            if (row_difference == 2) & (start_row == 6) & (open_end_position == "."):
                open_path = self.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
                if open_path is True:
                    return True
            # 2. Pawn starting on non-home rank
            if (row_difference == 1) & (open_end_position == "."):
                return True

        # Check for valid capture: valid direction, distance, and end position
        if (direction == "NORTHEAST") | (direction == "NORTHWEST"):
            occupied_end_position = board.get_piece_with_list_index(end_list_index)
            if (occupied_end_position != ".") & (total_difference == 2):
                return True

        return False

    def is_valid_move_for_falcon(self, alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Purpose: Determines if it is valid for falcon to move to alg_end_coordinate
        Parameters: alg_start_coordinate (falcon's current position),
                    alg_end_coordinate (falcon's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        board = chess_var.get_board()
        player_turn = chess_var.get_player_turn()
        if player_turn == "WHITE":
            return self.is_valid_move_for_falcon_white(alg_start_coordinate, alg_end_coordinate, board)
        else:
            return self.is_valid_move_for_falcon_black(alg_start_coordinate, alg_end_coordinate, board)

    def is_valid_move_for_falcon_white(self, alg_start_coordinate, alg_end_coordinate,  board):
        """
        Purpose: Determines if it is valid for white falcon to move to alg_end_coordinate
        Parameters: alg_start_coordinate (falcon's current position),
                    alg_end_coordinate (falcon's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        direction = self.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Check valid direction
        if direction not in ["NORTHWEST", "NORTHEAST", "SOUTH"]:
            return False

        # Check open path
        open_path = self.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
        if open_path is False:
            return False
        return True

    def is_valid_move_for_falcon_black(self, alg_start_coordinate, alg_end_coordinate,  board):
        """
        Purpose: Determines if it is valid for black falcon to move to alg_end_coordinate
        Parameters: alg_start_coordinate (falcon's current position),
                    alg_end_coordinate (falcon's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        direction = self.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Check valid direction
        if direction not in ["SOUTHWEST", "SOUTHEAST", "NORTH"]:
            return False

        # Check open path
        open_path = self.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
        if open_path is False:
            return False
        return True

    def is_valid_move_for_hunter(self, alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Purpose: Determines if it is valid for hunter to move to alg_end_coordinate
        Parameters: alg_start_coordinate (hunter's current position),
                    alg_end_coordinate (hunter's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        board = chess_var.get_board()
        player_turn = chess_var.get_player_turn()
        if player_turn == "WHITE":
            return self.is_valid_move_for_hunter_white(alg_start_coordinate, alg_end_coordinate, board)
        else:
            return self.is_valid_move_for_hunter_black(alg_start_coordinate, alg_end_coordinate, board)

    def is_valid_move_for_hunter_white(self, alg_start_coordinate, alg_end_coordinate, board):
        """
        Purpose: Determines if it is valid for white hunter to move to alg_end_coordinate
        Parameters: alg_start_coordinate (hunter's current position),
                    alg_end_coordinate (hunter's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        return self.is_valid_move_for_falcon_black(alg_start_coordinate, alg_end_coordinate, board)

    def is_valid_move_for_hunter_black(self, alg_start_coordinate, alg_end_coordinate, board):
        """
        Purpose: Determines if it is valid for black hunter to move to alg_end_coordinate
        Parameters: alg_start_coordinate (hunter's current position),
                    alg_end_coordinate (hunter's potential end position),
                    board (instance of Board class)
        Return value: (Boolean) True (move is valid) / False (move is invalid)
        """
        return self.is_valid_move_for_falcon_white(alg_start_coordinate, alg_end_coordinate, board)

    def identify_direction(self, alg_start_coordinate, alg_end_coordinate, board):
        """
        Purpose: Determines the direction from alg_start_coord to alg_end_coord
        Parameters: alg_start_coordinate (start point),
                    alg_end_coordinate (end point),
                    board (instance of Board class)
        Return value: (string) 'NORTH', 'NORTHEAST', 'EAST', 'SOUTHEAST',
                      'SOUTH', 'SOUTHWEST', 'WEST', 'NORTHWEST'
        """
        start_list_index = board.alg_coordinate_to_list_index(alg_start_coordinate)
        start_row, start_column = start_list_index[0], start_list_index[1]
        end_list_index = board.alg_coordinate_to_list_index(alg_end_coordinate)
        end_row, end_column = end_list_index[0], end_list_index[1]

        # Identify vertical and horizontal direction
        if start_column == end_column:
            if end_row - start_row > 0:
                return 'SOUTH'
            else:
                return 'NORTH'

        if start_row == end_row:
            if end_column - start_column > 0:
                return 'EAST'
            else:
                return 'WEST'

        row_difference = end_row - start_row
        column_difference = end_column - start_column


        # Identify diagonal direction
        if abs(row_difference) == abs(column_difference):
            if (row_difference < 0) & (column_difference) > 0:
                return 'NORTHEAST'
            elif (row_difference > 0) & (column_difference < 0):
                return 'SOUTHWEST'
            elif (row_difference < 0) & (column_difference < 0):
                return 'NORTHWEST'
            elif (row_difference > 0) & (column_difference > 0):
                return 'SOUTHEAST'

        # Invalid direction
        return 'N/A'

    def identify_blocked_square(self, alg_start_coordinate, alg_end_coordinate, direction, board):
        """
        Purpose: For pieces that cannot jump — determines if a piece is blocking the path from
                 alg_start_coord to alg_end_coord
        Parameters: alg_start_coordinate (start point),
                    alg_end_coordinate (end point),
                    board (instance of Board class),
                    direction (direction of the path to check)
        Return value: True (move is valid) / False (move is invalid)
        """
        start_list_index = board.alg_coordinate_to_list_index(alg_start_coordinate)
        start_row, start_column = start_list_index[0], start_list_index[1]
        end_list_index = board.alg_coordinate_to_list_index(alg_end_coordinate)
        end_row, end_column = end_list_index[0], end_list_index[1]

        # Check blockages for vertical and horizontal directions
        if direction == 'NORTH':
            for row in range(start_row-1, end_row, -1):
                if board.get_piece_with_list_index([row, start_column]) != ".":
                    return False

        elif direction == 'SOUTH':
            for row in range(start_row+1, end_row):
                if board.get_piece_with_list_index([row, start_column]) != ".":
                    return False

        elif direction == 'EAST':
            for column in range(start_column+1, end_column):
                if board.get_piece_with_list_index([start_row, column]) != ".":
                    return False

        elif direction == 'WEST':
            for column in range(start_column-1, end_column, -1):
                if board.get_piece_with_list_index([start_row, column]) != ".":
                    return False

        num_of_checked_squares = abs(end_row - start_row) - 1

        # Check blockages for diagonal directions
        if direction == 'NORTHEAST':
            for square in range(num_of_checked_squares):
                start_row = start_row - 1
                start_column = start_column + 1
                if board.get_piece_with_list_index([start_row, start_column]) != ".":
                    return False

        elif direction == 'SOUTHEAST':
            for square in range(num_of_checked_squares):
                start_row = start_row + 1
                start_column = start_column + 1
                if board.get_piece_with_list_index([start_row, start_column]) != ".":
                    return False

        elif direction == 'SOUTHWEST':
            for square in range(num_of_checked_squares):
                start_row = start_row + 1
                start_column = start_column - 1
                if board.get_piece_with_list_index([start_row, start_column]) != ".":
                    return False

        elif direction == 'NORTHWEST':
            for square in range(num_of_checked_squares):
                start_row = start_row - 1
                start_column = start_column - 1
                if board.get_piece_with_list_index([start_row, start_column]) != ".":
                    return False

        return True

class Board:
    """Responsibility: Represents a board the chess game is played on, with methods for
                       placing, removing, and retrieving pieces on the board
       Communicates with:
       ChessVar class — an instance of Board is declared as a private member in ChessVar, so players have a
       "board" to play on
       Pieces class — several Pieces methods accept an instance of Board as an argument
    """

    def __init__(self):
        """Purpose: Initialize an instance of board, with
           self._board_display initialized with starting positions of all pieces,
           except reserve falcon and hunter
           Parameters: None
           Return value: None
        """
        # Lowercase letters: BLACK pieces
        # Uppercase letters: WHITE pieces
        self._board_display = [
        ['8','r','n','b','q','k','b','n','r'],
        ['7','p','p','p','p','p','p','p','p'],
        ['6','.','.','.','.','.','.','.','.'],
        ['5','.','.','.','.','.','.','.','.'],
        ['4','.','.','.','.','.','.','.','.'],
        ['3','.','.','.','.','.','.','.','.'],
        ['2','P','P','P','P','P','P','P','P'],
        ['1','R','N','B','Q','K','B','N','R'],
        [' ','a','b','c','d','e','f','g','h']]

        # Dictionaries used in alg_coordinate_to_list_index method
        self._letter_to_column_dict = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4,
            'e': 5, 'f': 6, 'g': 7, 'h': 8
        }
        self._number_to_row_dict = {
            '1': 7, '2': 6, '3': 5, '4': 4,
            '5': 3, '6': 2, '7': 1, '8': 0
        }

    def get_board_display(self):
        """Purpose: Get self._board_display
           Parameters: None
           Return value: self._board_display
        """
        return self._board_display

    def set_board_display(self, board_display):
        """Purpose: Set ._board_display
           Parameters: None
           Return value: None
        """
        self._board_display = board_display

    def print_board_display(self):
        """Purpose: Print ._board_display
           Parameters: None
           Return value: None
        """
        for row in range(9):
            row_string = "  ".join(self._board_display[row])
            print(row_string)

    def alg_coordinate_to_list_index(self, alg_coordinate):
        """
        Purpose: Convert algebraic coordinates to a list index that can be used to access
                 ._board_display
        Parameters: alg_coordinate
        Return value: list with row index and column index [row, column]
        """
        # Split string into letter, number
        letter = alg_coordinate[0]
        number = alg_coordinate[1]

        # Create list index
        try:
            column = self._letter_to_column_dict[letter]
            row = self._number_to_row_dict[number]
        except KeyError:
            return False

        return [row, column]

    def place_piece(self, alg_coordinate, piece):
        """
        Purpose: Place piece in alg_coordinate position
        Parameters: alg_coordinate
        Return value: None
        """
        list_index = self.alg_coordinate_to_list_index(alg_coordinate)
        row = list_index[0]
        column = list_index[1]
        self._board_display[row][column] = piece

    def remove_piece(self, alg_coordinate):
        """
        Purpose: Remove piece by setting alg_coordinate position to "."
        Parameters: alg_coordinate
        Return value: None
        """
        list_index = self.alg_coordinate_to_list_index(alg_coordinate)
        row = list_index[0]
        column = list_index[1]
        self._board_display[row][column] = '.'

    def get_piece(self, alg_coordinate):
        """
        Purpose: Identify piece in target position
        Parameters: alg_coordinate
        Return value: "." or letter that represents the piece in the position
        """
        list_index = self.alg_coordinate_to_list_index(alg_coordinate)
        row = list_index[0]
        column = list_index[1]
        piece = self._board_display[row][column]

        return piece

    def get_piece_with_list_index(self, list_index):
        """
        Purpose: Identify piece in target position
        Parameters: alg_coordinate
        Return value: "." or letter that represents the piece in the position
        """
        row = list_index[0]
        column = list_index[1]
        piece = self._board_display[row][column]

        return piece

class ChessVar:
    """Responsibility: Represents one round of a chess-variation game,
       with methods to determine game state, player turns, and make moves
       Communicates with:
       Board class — an instance of Board is declared as a private member
       in ChessVar so players have a "board" to play on
       Pieces class — an instance of Pieces is declared as a private member
       in ChessVar to determine if a move entered by the player is valid
    """

    def __init__(self):
        """Purpose: Initialize private board, player_turn, and game_state
           Parameters:
           Return value:
        """
        self._pieces = Pieces()
        self._board = Board()
        self._white = Player(['F', 'H'])
        self._black = Player(['f', 'h'])
        self._player_turn = 'WHITE'
        self._game_state = 'UNFINISHED'
        self._white_pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 'F', 'H']
        self._black_pieces = ['p', 'r', 'n', 'b', 'q', 'k', 'f', 'h']

    def get_board(self):
        """Purpose: Returns ._board
           Parameters: None
           Return value: ._board
        """
        return self._board

    def get_game_state(self):
        """Purpose: Returns ._game_state
           Parameters: None
           Return value: (string) 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'
        """
        return self._game_state

    def set_game_state(self, game_state):
        """Purpose: Sets ._game_state
           Parameters: None
           Return value: None
        """
        self._game_state = game_state

    def get_player_turn(self):
        """Purpose: Returns ._game_state
           Parameters: None
           Return value: (string) 'WHITE' or 'BLACK'
        """
        return self._player_turn

    def make_move(self, alg_start_coordinate, alg_end_coordinate):
        """Purpose: Moves piece from alg_start_coordinate to alg_end_coordinate if allowed
           Parameters: alg_start_coordinate (current position of piece to be moved)
                       alg_end_coordinate (position to move piece to)
           Return value: (Boolean) True or False
        """
        #1: Check several conditions for coordinates
        if self.verify_player_square(alg_start_coordinate, alg_end_coordinate) is False:
            return False

        #2: Check if ._game_state is unfinished
        if self.get_game_state() != "UNFINISHED":
            return False

        #3: Check if move is valid
        piece = self._board.get_piece(alg_start_coordinate)
        valid_move = self.is_valid_move(piece, alg_start_coordinate, alg_end_coordinate)
        if valid_move is False:
            return False

        # Capture opponent piece
        captured_piece = self._board.get_piece(alg_end_coordinate)
        self._board.remove_piece(alg_end_coordinate)
        # Place new piece
        self._board.place_piece(alg_end_coordinate, piece)
        # Reset alg_start_coordinate to "."
        self._board.remove_piece(alg_start_coordinate)

        # Update fairy piece state
        self.determine_fairy_piece(captured_piece)
        # Update game state
        self.determine_winner(captured_piece)
        # Update turn
        self.update_player_turn()
        return True


    def verify_player_square(self, alg_start_coordinate, alg_end_coordinate):
        """
        Purpose: Checks several conditions for start and end coordinates
        Parameters: alg_coordinate
        Return value: True or False
        """
        #1: Check if start and end_coordinate are the same
        if alg_start_coordinate == alg_end_coordinate:
            return False

        #2: Check if coordinates are off the grid
        start_on_grid = self._board.alg_coordinate_to_list_index(alg_start_coordinate)
        end_on_grid = self._board.alg_coordinate_to_list_index(alg_end_coordinate)

        if (start_on_grid is False) | (end_on_grid is False):
            return False

        # Retrieve pieces
        start_piece = self._board.get_piece(alg_start_coordinate)
        end_piece = self._board.get_piece(alg_end_coordinate)

        #3: Check if start_piece is empty
        if start_piece == ".":
            return False

        #4: Check conditions dependent on player and piece color
        # Check if start_piece belongs to opponent
        # Check if end_piece belongs to current player
        if self._player_turn == "WHITE":
           if (start_piece not in self._white_pieces) | (end_piece in self._white_pieces):
               return False

        if self._player_turn == "BLACK":
           if (start_piece not in self._black_pieces) | (end_piece in self._black_pieces):
              return False

        # All conditions passed
        return True

    def determine_fairy_piece(self, captured_piece):
        """
        Purpose: Call Player class update_fairy_piece_entry
        Parameters: captured_piece
        Return value: None
        """

        # White piece captured black main piece, so update black fairy piece status
        if (self._player_turn == "WHITE") & (captured_piece in ['q', 'r', 'b', 'n']):
            self._black.update_capture_count(1)
            self._black.update_fairy_piece_entry()

        # Black piece captured white main piece, so update white fairy piece status
        if (self._player_turn == "BLACK") & (captured_piece in ['Q', 'R', 'B', 'N']):
            self._white.update_capture_count(1)
            self._white.update_fairy_piece_entry()

    def determine_winner(self, captured_piece):
        """
        Purpose: Call set_game_state
        Parameters: captured_piece
        Return value: None
        """
        if captured_piece == 'k':
            self._game_state = "WHITE_WON"
        elif captured_piece == 'K':
            self._game_state = "BLACK_WON"

    def set_player_turn(self, color):
        """
        Purpose: Set ._player_turn
        Parameters: None
        Return value: None
        """
        self._player_turn = color

    def update_player_turn(self):
        """
        Purpose: Update ._player_turn by calling set_player_turn
        Parameters: None
        Return value: None
        """
        if self._player_turn == "WHITE":
            self._player_turn = "BLACK"
        else:
            self._player_turn = "WHITE"

    def is_valid_move(self, piece, alg_start_coordinate, alg_end_coordinate):
        """Purpose: Checks if valid for piece to move from start to end position
           Parameters: piece, alg_start_coordinate (start position), alg_end_coordinate (end_position)
           Return value: True or False
        """
        piece = piece.upper()

        # Call the Piece class method that corresponds to the chosen piece
        if piece == 'R':
            return self._pieces.is_valid_move_for_rook(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'B':
            return self._pieces.is_valid_move_for_bishop(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'Q':
            return self._pieces.is_valid_move_for_queen(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'N':
            return self._pieces.is_valid_move_for_knight(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'K':
            return self._pieces.is_valid_move_for_king(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'P':
            return self._pieces.is_valid_move_for_pawn(alg_start_coordinate, alg_end_coordinate,
                                                       self)
        elif piece == 'F':
            return self._pieces.is_valid_move_for_falcon(alg_start_coordinate, alg_end_coordinate,
                                                       self)
        elif piece == 'H':
            return self._pieces.is_valid_move_for_hunter(alg_start_coordinate, alg_end_coordinate,
                                                         self)

    def enter_fairy_piece(self, fairy_piece_type, placement_square):
        """Purpose: Determines if fairy piece can be entered onto the board
           Parameters: piece_type (string), placement_square (algebraic coordinates)
           Return value: True or False
        """
        # Perform initial checks
        if self.verify_fairy_piece_and_position(fairy_piece_type, placement_square) is False:
            return False

        if self._player_turn == "WHITE":
            if self._white.get_fairy_piece_entry() is False:
                return False
            else:
                self.fairy_piece_actions(self._white, fairy_piece_type)

        if self._player_turn == "BLACK":
            if self._black.get_fairy_piece_entry() is False:
                return False
            else:
                self.fairy_piece_actions(self._black, fairy_piece_type)

        # Place fairy piece
        self._board.place_piece(placement_square, fairy_piece_type)
        # Update turn
        self.update_player_turn()
        return True

    def fairy_piece_actions(self, player, piece):
        """Purpose: Determines if fairy piece can be entered onto the board
           Parameters: piece_type (string), placement_square (algebraic coordinates)
           Return value: True or False
        """

        # Remove in-play fairy piece from reserve list
        player.remove_from_reserve_list(piece)

        # Decrement capture count
        player.update_capture_count(-1)
        player.update_fairy_piece_entry

    def verify_fairy_piece_and_position(self, fairy_piece_type, placement_square):
        """Purpose: Performs initial checks for enter_fairy_piece
           Parameters: piece_type (string), placement_square (algebraic coordinates)
           Return value: True or False
        """
        list_index = self._board.alg_coordinate_to_list_index(placement_square)

        # Placement square is off board
        if list_index is False:
            return False
        row, column = list_index[0], list_index[1]

        # Perform initial checks
        # WHITE
        if self._player_turn == "WHITE":
            # Check if fairy piece placed on home rank
            if row != 7:
                return False
            # Check if placement_square is empty
            if (self._board.get_piece_with_list_index(list_index) != "."):
                return False
            # Check if fairy_piece_type is valid
            if fairy_piece_type not in self._white.get_reserve_list():
                return False

        # BLACK
        if self._player_turn == "BLACK":
            if row != 0:
                return False
            if (self._board.get_piece_with_list_index(list_index) != "."):
                return False
            if fairy_piece_type not in self._black.get_reserve_list():
                return False

        return True

