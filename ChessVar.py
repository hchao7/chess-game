# Author: Helen C
# GitHub username: hchao7
# Date: 09/06/24
# Description: Implementation of an abstract board game that is a variant of chess

class Player:
    """
    A class representing a chess player.

    This class keeps track of a player's fairy pieces (falcon and hunter).
    It communicates with:
    ChessVar class — 2 Player instances (white-piece player and black-piece player) declared as attributes.

    Attributes:
        _reserve_list (list): A list of fairy pieces that are available for use.
        _fairy_piece_entry (bool): Indicates whether a fairy piece can be played.
        _capture_count (int): The count of captured Queen, Rook, Bishop, and Knight pieces.
    """

    def __init__(self, reserve_list):
        """
        Initializes a new Player instance.

        A white-piece Player's _reserve_list is initialized with ["F", "H"], for fairy and hunter.
        A black-piece Player's _reserve_list is initialized with ["f", "h"], for fairy and hunter.

        Args:
            reserve_list (list): Fairy pieces assigned to player.
        """
        self._reserve_list = reserve_list
        self._fairy_piece_entry = False
        self._capture_count = 0

    def set_capture_count(self, capture_count):
        """
        Sets _capture_count.

        Args:
            capture_count (int): Value _capture_count should be set to.

        Returns:
            None: This method does not return any value.
        """
        self._capture_count = capture_count

    def get_capture_count(self):
        """
        Retrieves _capture_count.

        This method does not require any arguments.

        Returns:
            _capture_count (int): The count of captured Queen, Rook, Bishop, and Knight pieces.
        """
        return self._capture_count

    def update_capture_count(self, value):
        """
        Updates _capture_count.

        This method is called by ChessVar's make_move() and enter_fairy_piece().
        It increases _capture_count by 1 if a Queen, Rook, Bishop, or Knight is captured.
        It decreases _capture_count by -1 if a fairy piece is used.

        Args:
            value (int): Value _capture_count should be adjusted by.

        Returns:
            None: This method does not return any value.
        """
        self._capture_count = self._capture_count + value

    def update_fairy_piece_entry(self):
        """
        Updates _fairy_piece_entry.

        This method is called by ChessVar's make_move() and enter_fairy_piece().
        It checks several conditions to update _fairy_piece_entry.
        This method does not require any arguments.

        Returns:
            None: This method does not return any value.
        """
        # No more fairy pieces in reserve
        if not self._reserve_list:
            self._fairy_piece_entry = False

        # No main pieces (Queen, Rook, Bishop, or Knight) captured
        elif self._capture_count == 0:
            self._fairy_piece_entry = False

        # Main piece(s) captured and fairy piece(s) in reserve
        elif self._capture_count > 0:
            self._fairy_piece_entry = True

    def set_reserve_list(self, reserve_list):
        """
        Sets _reserve_list.

        Args:
            reserve_list (list): Fairy pieces assigned to player.

        Returns:
            None: This method does not return any value.
        """
        self._reserve_list = reserve_list

    def get_reserve_list(self):
        """
        Retrieves _reserve_list.

        This method does not require any arguments.

        Returns:
            _reserve_list (list): Fairy pieces assigned to player.
        """
        return self._reserve_list

    def remove_from_reserve_list(self, fairy_piece):
        """
        Removes fairy piece from reserve list.

        This method is called by ChessVar's fairy_piece_actions() when a fairy piece is placed on the board.
        The piece is removed from _reserve_list.

        Args:
            fairy_piece (str): Fairy piece to be removed.

        Returns:
            None: This method does not return any value.
        """
        self._reserve_list.remove(fairy_piece)

    def set_fairy_piece_entry(self, fairy_piece_entry):
        """
        Sets _fairy_piece_entry.

        Args:
            fairy_piece_entry (bool): Indicates if a fairy piece can be played.

        Returns:
            None: This method does not return any value.
        """
        self._fairy_piece_entry = fairy_piece_entry

    def get_fairy_piece_entry(self):
        """
        Retrieves _fairy_piece_entry.

        This method does not require any arguments.

        Returns:
            _fairy_piece_entry (bool): Indicates if a fairy piece can be played.
        """
        return self._fairy_piece_entry

class Pieces:
    """
        A static class representing chess pieces.

        This class has static methods that determine if a chess move by any chess piece is valid.
        Each method checks the validity of moves based on the specific movement rules of each piece.
        It communicates with:
        ChessVar class — Called by is_valid_move() to determine if a move is valid.

        Attributes:
            None
    """

    def is_valid_move_for_king(alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Checks if king can move to alg_end_coordinate legally.

        Args:
            alg_start_coordinate (str): King's current position.
            alg_end_coordinate (str): King's potential end position.
            chess_var (ChessVar): Instance of the current game state.

        Returns:
            True or False (bool): Indicates if move is illegal or legal.
        """

        # Checks direction of move
        board = chess_var.get_board()
        direction = Pieces.identify_direction(alg_start_coordinate, alg_end_coordinate, board)
        if direction == 'N/A':  # Invalid direction
            return False

        # Calculates distance traveled between start and end coordinates
        start_row, start_column = board.alg_coordinate_to_list_index(alg_start_coordinate)
        end_row, end_column = board.alg_coordinate_to_list_index(alg_end_coordinate)
        row_difference, column_difference = Pieces.row_column_difference(end_row, start_row, end_column, start_column)
        total_difference = row_difference + column_difference

        # Checks if King traveled a valid direction and distance
        if (direction in ["NORTH", "EAST", "SOUTH", "WEST"]) and (total_difference == 1):
            return True
        elif (direction in ["NORTHEAST", "SOUTHEAST", "SOUTHWEST", "NORTHWEST"]) and (total_difference == 2):
            return True

        return False

    def is_valid_move_for_queen(alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Checks if queen can move to alg_end_coordinate legally.

        Args:
            alg_start_coordinate (str): Queen's current position.
            alg_end_coordinate (str): Queen's potential end position.
            chess_var (ChessVar): Instance of the current game state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        # Checks direction of move
        board = chess_var.get_board()
        direction = Pieces.identify_direction(alg_start_coordinate, alg_end_coordinate, board)
        if direction == 'N/A':  # Invalid direction
            return False

        # Checks if path is blocked by another piece
        open_path = Pieces.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
        if open_path is False:
            return False

        return True

    def is_valid_move_for_rook(alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Checks if rook can move to alg_end_coordinate legally.

        Args:
            alg_start_coordinate (str): Rook's current position.
            alg_end_coordinate (str): Rook's potential end position.
            chess_var (ChessVar): Instance of the current game state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        # Checks direction of move
        board = chess_var.get_board()
        direction = Pieces.identify_direction(alg_start_coordinate, alg_end_coordinate, board)
        if direction not in ['NORTH', 'SOUTH', 'EAST', 'WEST']:
            return False

        # Checks if path is blocked
        open_path = Pieces.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
        if open_path is False:
            return False

        return True

    def is_valid_move_for_bishop(alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Checks if bishop can move to alg_end_coordinate legally.

        Args:
            alg_start_coordinate (str): Bishop's current position.
            alg_end_coordinate (str): Bishop's potential end position.
            chess_var (ChessVar): Instance of the current game state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        # Checks direction of move
        board = chess_var.get_board()
        direction = Pieces.identify_direction(alg_start_coordinate, alg_end_coordinate, board)
        if direction not in ['NORTHEAST', 'SOUTHWEST', 'NORTHWEST', 'SOUTHEAST']:
            return False

        # Checks if path is blocked
        open_path = Pieces.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
        if open_path is False:
            return False

        return True

    def is_valid_move_for_knight(alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Checks if knight can move to alg_end_coordinate legally.

        Args:
            alg_start_coordinate (str): Knight's current position.
            alg_end_coordinate (str): Knight's potential end position.
            chess_var (ChessVar): Instance of the current game state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        # Calculates distance traveled between start and end coordinates
        board = chess_var.get_board()
        start_row, start_column = board.alg_coordinate_to_list_index(alg_start_coordinate)
        end_row, end_column = board.alg_coordinate_to_list_index(alg_end_coordinate)
        row_difference, column_difference = Pieces.row_column_difference(end_row, start_row, end_column, start_column)

        # Checks if knight traveled a valid distance
        if (row_difference == 2) and (column_difference == 1):
            return True
        elif (row_difference == 1) and (column_difference == 2):
            return True

        return False

    def is_valid_move_for_pawn(alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Checks if pawn can move to alg_end_coordinate legally.

        This method calls helper methods is_valid_move_for_pawn_white() or is_valid_move_for_pawn_black().

        Args:
            alg_start_coordinate (str): Pawn's current position.
            alg_end_coordinate (str): Pawn's potential end position.
            chess_var (ChessVar): Instance of the current game state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        board = chess_var.get_board()
        player_turn = chess_var.get_player_turn()

        # Calls helper method based on player_turn
        if player_turn == "WHITE":
            return Pieces.is_valid_move_for_pawn_white(alg_start_coordinate, alg_end_coordinate, board)
        else:
            return Pieces.is_valid_move_for_pawn_black(alg_start_coordinate, alg_end_coordinate, board)


    def is_valid_move_for_pawn_black(alg_start_coordinate, alg_end_coordinate, board):
        """
        Checks if black pawn can move to alg_end_coordinate legally.

        This method is a helper method for is_valid_move_for_pawn().
        Rules for pawn moves vary depending on whether the pawn is capturing another piece.

        Args:
            alg_start_coordinate (str): Pawn's current position.
            alg_end_coordinate (str): Pawn's potential end position.
            board (Board): Instance of the current board state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        # Calculates distance traveled between start and end coordinates
        start_row, start_column = board.alg_coordinate_to_list_index(alg_start_coordinate)
        end_row, end_column = board.alg_coordinate_to_list_index(alg_end_coordinate)
        row_difference, column_difference = Pieces.row_column_difference(end_row, start_row, end_column, start_column)
        total_difference = row_difference + column_difference

        # Identifies direction of move
        direction = Pieces.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Checks if non-capture moves are valid
        # Checks direction, distance traveled, and end coordinate
        # Square represented by end coordinate must be empty
        if direction == "SOUTH":
            open_end_position = board.get_piece_with_list_index([end_row, end_column])

            # 1. Condition where pawn starts on home rank
            if (row_difference == 2) and (start_row == 1) and (open_end_position == "."):
                # Checks if path is blocked
                open_path = Pieces.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
                if open_path is True:
                    return True

            # 2. Condition where pawn starts on non-home rank
            if (row_difference == 1) and (open_end_position == "."):
                return True

        # Checks if capture moves are valid
        # Checks direction, distance traveled, and end coordinate
        if (direction == "SOUTHEAST") or (direction == "SOUTHWEST"):
            occupied_end_position = board.get_piece_with_list_index([end_row, end_column])
            if (occupied_end_position != ".") and (total_difference == 2):
                return True

        return False

    def is_valid_move_for_pawn_white(alg_start_coordinate, alg_end_coordinate, board):
        """
        Checks if white pawn can move to alg_end_coordinate legally.

        This method is a helper method for is_valid_move_for_pawn().
        Rules for pawn moves vary depending on whether the pawn is capturing another piece.

        Args:
            alg_start_coordinate (str): Pawn's current position.
            alg_end_coordinate (str): Pawn's potential end position.
            board (Board): Instance of the current board state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        # Calculates distance traveled between start and end coordinates
        start_row, start_column = board.alg_coordinate_to_list_index(alg_start_coordinate)
        end_row, end_column = board.alg_coordinate_to_list_index(alg_end_coordinate)
        row_difference, column_difference = Pieces.row_column_difference(end_row, start_row, end_column, start_column)
        total_difference = row_difference + column_difference

        # Identifies direction of move
        direction = Pieces.identify_direction(alg_start_coordinate, alg_end_coordinate, board)

        # Checks if non-capture moves are valid
        # Checks direction, distance traveled, and end coordinate
        # Square represented by end coordinate must be empty
        if direction == "NORTH":
            open_end_position = board.get_piece_with_list_index([end_row, end_column])

            # 1. Condition where pawn starts on home rank
            if (row_difference == 2) and (start_row == 6) and (open_end_position == "."):
                # Checks if path is blocked
                open_path = Pieces.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
                if open_path is True:
                    return True

            # 2. Condition where pawn starts on non-home rank
            if (row_difference == 1) and (open_end_position == "."):
                return True

        # Checks if capture moves are valid
        # Checks direction, distance traveled, and end coordinate
        if (direction == "NORTHEAST") or (direction == "NORTHWEST"):
            occupied_end_position = board.get_piece_with_list_index([end_row, end_column])
            if (occupied_end_position != ".") and (total_difference == 2):
                return True

        return False

    def is_valid_move_for_falcon(alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Checks if falcon can move to alg_end_coordinate legally.

        This method calls helper methods is_valid_move_for_falcon_white() or is_valid_move_for_falcon_black().

        Args:
            alg_start_coordinate (str): Falcon's current position.
            alg_end_coordinate (str): Falcon's potential end position.
            chess_var (ChessVar): Instance of the current game state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        board = chess_var.get_board()
        player_turn = chess_var.get_player_turn()

        # Calls helper method based on player_turn
        if player_turn == "WHITE":
            return Pieces.is_valid_move_for_falcon_white(alg_start_coordinate, alg_end_coordinate, board)
        else:
            return Pieces.is_valid_move_for_falcon_black(alg_start_coordinate, alg_end_coordinate, board)

    def is_valid_move_for_falcon_white(alg_start_coordinate, alg_end_coordinate, board):
        """
        Checks if white falcon can move to alg_end_coordinate legally.

        This method is a helper method for is_valid_move_for_falcon().

        Args:
            alg_start_coordinate (str): Falcon's current position.
            alg_end_coordinate (str): Falcon's potential end position.
            board (Board): Instance of the current board state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        # Checks direction of move
        direction = Pieces.identify_direction(alg_start_coordinate, alg_end_coordinate, board)
        if direction not in ["NORTHWEST", "NORTHEAST", "SOUTH"]:
            return False

        # Checks if path is blocked
        open_path = Pieces.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
        if open_path is False:
            return False

        return True

    def is_valid_move_for_falcon_black(alg_start_coordinate, alg_end_coordinate, board):
        """
        Checks if black falcon can move to alg_end_coordinate legally.

        This method is a helper method for is_valid_move_for_falcon().

        Args:
            alg_start_coordinate (str): Falcon's current position.
            alg_end_coordinate (str): Falcon's potential end position.
            board (Board): Instance of the current board state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        # Checks direction of move
        direction = Pieces.identify_direction(alg_start_coordinate, alg_end_coordinate, board)
        if direction not in ["SOUTHWEST", "SOUTHEAST", "NORTH"]:
            return False

        # Checks if path is blocked
        open_path = Pieces.identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board)
        if open_path is False:
            return False

        return True

    def is_valid_move_for_hunter(alg_start_coordinate, alg_end_coordinate, chess_var):
        """
        Checks if hunter can move to alg_end_coordinate legally.

        This method calls helper methods is_valid_move_for_hunter_white() or is_valid_move_for_hunter_black().

        Args:
            alg_start_coordinate (str): Hunter's current position.
            alg_end_coordinate (str): Hunter's potential end position.
            chess_var (ChessVar): Instance of the current game state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        board = chess_var.get_board()
        player_turn = chess_var.get_player_turn()

        # Calls helper method based on player_turn
        if player_turn == "WHITE":
            return Pieces.is_valid_move_for_hunter_white(alg_start_coordinate, alg_end_coordinate, board)
        else:
            return Pieces.is_valid_move_for_hunter_black(alg_start_coordinate, alg_end_coordinate, board)

    def is_valid_move_for_hunter_white(alg_start_coordinate, alg_end_coordinate, board):
        """
        Checks if white hunter can move to alg_end_coordinate legally.

        This method is a helper method for is_valid_move_for_hunter().
        The white hunter follows the same rules as the black falcon.
        Therefore, is_valid_move_for_falcon_black() is called.

        Args:
            alg_start_coordinate (str): Hunter's current position.
            alg_end_coordinate (str): Hunter's potential end position.
            board (Board): Instance of the current board state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        return Pieces.is_valid_move_for_falcon_black(alg_start_coordinate, alg_end_coordinate, board)

    def is_valid_move_for_hunter_black(alg_start_coordinate, alg_end_coordinate, board):
        """
        Checks if black hunter can move to alg_end_coordinate legally.

        This method is a helper method for is_valid_move_for_hunter().
        The black hunter follows the same rules as the white falcon.
        Therefore, is_valid_move_for_falcon_white() is called.

        Args:
            alg_start_coordinate (str): Hunter's current position.
            alg_end_coordinate (str): Hunter's potential end position.
            board (Board): Instance of the current board state.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        return Pieces.is_valid_move_for_falcon_white(alg_start_coordinate, alg_end_coordinate, board)

    def identify_direction(alg_start_coordinate, alg_end_coordinate, board):
        """
        Determines the direction from start to end coordinate.

        Each type of chess piece can only travel in a certain direction(s).
        This method is called by other Piece methods that responsible for
        validating moves, like is_valid_move_for_king().

        Args:
            alg_start_coordinate (str): Start position of chess piece.
            alg_end_coordinate (str): End position of chess piece.
            board (Board): Instance of the current board state.

        Returns:
            (str): Cardinal or ordinal direction
        """
        # Checks for cardinal direction
        start_row, start_column = board.alg_coordinate_to_list_index(alg_start_coordinate)
        end_row, end_column = board.alg_coordinate_to_list_index(alg_end_coordinate)

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

        # Checks for ordinal direction
        row_difference = end_row - start_row
        column_difference = end_column - start_column

        if abs(row_difference) == abs(column_difference):
            if (row_difference < 0) and (column_difference) > 0:
                return 'NORTHEAST'
            elif (row_difference > 0) and (column_difference < 0):
                return 'SOUTHWEST'
            elif (row_difference < 0) and (column_difference < 0):
                return 'NORTHWEST'
            elif (row_difference > 0) and (column_difference > 0):
                return 'SOUTHEAST'

        # Invalid direction (not cardinal or ordinal)
        return 'N/A'

    def identify_blocked_square(alg_start_coordinate, alg_end_coordinate, direction, board):
        """
        Determines if any chess piece blocks the path from start to end coordinate.

        This method is called by other Piece methods that
        validate moves for chess pieces that cannot jump, like is_valid_move_for_queen().

        Args:
            alg_start_coordinate (str): Start position of chess piece.
            alg_end_coordinate (str): End position of chess piece.
            direction (str): Direction chess piece will move in.
            board (Board): Instance of the current board state.

        Returns:
            True or False (bool): Indicates if path is unblocked or blocked
        """
        start_row, start_column = board.alg_coordinate_to_list_index(alg_start_coordinate)
        end_row, end_column = board.alg_coordinate_to_list_index(alg_end_coordinate)

        # Checks blockages for cardinal directions
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

        # Checks blockages for ordinal directions
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

    def row_column_difference(end_row, start_row, end_column, start_column):
        """
        Calculates differences between row indexes and column indexes.

        Some types of chess piece can only travel a specific distance.
        This method is called by other Piece methods to validate moves for chess pieces,
        like is_valid_move_for_king().

        Args:
            end_row (int): Index of row of end coordinate
            start_row (int): Index of row of start coordinate
            end_column (int): Index of column of end coordinate
            start_column (int): Index of column of start coordinate

        Returns:
            row_diff, column_diff (tuple): Represents row and column differences
        """
        row_diff = abs(end_row - start_row)
        column_diff = abs(end_column - start_column)
        return row_diff, column_diff

class Board:
    """
        A class representing a chess board.

        This class has methods for placing, removing, and retrieving chess pieces on a board.
        It communicates with:
        ChessVar class — Has 1 Board instance declared as an attribute.

        Attributes:
            _board_display (list): Chess board (a grid) with rows and columns.
            _letter_to_column_dict (dict): Maps each letter to its corresponding column index in _board_display.
            _number_to_row_dict (dict): Maps each number to its corresponding row index in _board_display.
    """

    def __init__(self):
        """
        Initializes a new Board instance.

        _board_display is initialized with the white and black chess pieces in their starting positions.
        This method does not require any arguments.

        Returns:
            None
        """
        # Lowercase letters represent black pieces
        # Uppercase letters represent white pieces
        # "." represents an empty square
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

        self._letter_to_column_dict = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4,
            'e': 5, 'f': 6, 'g': 7, 'h': 8
        }
        self._number_to_row_dict = {
            '1': 7, '2': 6, '3': 5, '4': 4,
            '5': 3, '6': 2, '7': 1, '8': 0
        }

    def get_board_display(self):
        """
        Retrieves _board_display.

        This method does not require any arguments.

        Returns:
            _board_display (list): Grid with rows and columns.
        """
        return self._board_display

    def set_board_display(self, board_display):
        """
        Sets _board_display.

        Args:
            board_display (list): Grid with rows and columns.

        Returns:
            None
        """
        self._board_display = board_display

    def print_board_display(self):
        """
        Prints _board_display.

        This method does not require any arguments.

        Returns:
            None
        """
        for row in range(9):
            row_string = "  ".join(self._board_display[row])
            print(row_string)

    def alg_coordinate_to_list_index(self, alg_coordinate):
        """
        Converts algebraic coordinates to a row index and column index.

        Players will reference squares on the chess board by their algebraic coordinates.
        To access _board_display, these coordinates must be converted to a row index and column index.

        Args:
            alg_coordinate (str): Represents a square on the board.

        Returns:
            row, column (tuple): Row index and column index.
        """
        letter, number = alg_coordinate
        try:
            column = self._letter_to_column_dict[letter]
            row = self._number_to_row_dict[number]
        except KeyError:
            return [False, False]

        return [row, column]

    def place_piece(self, alg_coordinate, piece):
        """
        Places piece on chess board.

        Args:
            alg_coordinate (str): Square where piece will be placed.
            piece (str): Piece that will be placed.

        Returns:
            None
        """
        row, column = self.alg_coordinate_to_list_index(alg_coordinate)
        self._board_display[row][column] = piece

    def remove_piece(self, alg_coordinate):
        """
        Removes piece from chess board.

        Args:
            alg_coordinate (str): Square where piece should be removed from.

        Returns:
            None
        """
        row, column = self.alg_coordinate_to_list_index(alg_coordinate)
        self._board_display[row][column] = '.'

    def get_piece(self, alg_coordinate):
        """
        Retrieves piece from chess board without removing.

        Args:
            alg_coordinate (str): Square where piece should be retrieved from.

        Returns:
            piece (str): Piece on requested square, or "." if square is empty.
        """
        row, column = self.alg_coordinate_to_list_index(alg_coordinate)
        piece = self._board_display[row][column]
        return piece

    def get_piece_with_list_index(self, list_index):
        """
        Retrieves piece from chess board using row index and column index.

        Args:
            list_index (str): Square where piece should be retrieved from.

        Returns:
            piece (str): Piece on board, or "." if requested square is empty.
        """
        row, column = list_index
        piece = self._board_display[row][column]
        return piece

class ChessVar:
    """
    A class representing one round of a chess-variation game.

    This class has methods to determine game state, player turns, and execute player moves.
    It communicates with:
    Board class — described in Attributes.
    Player class — describe in Attributes.

    Attributes:
        _reserve_list (list): A list of fairy pieces that are available for use.
        _board (Board): An instance of Board that the chess game is played on.
        _white (Player): An instance of Player that represents the white-piece player.
        _black (Player): An instance of Player that represents the black-piece player.
        _player_turn (str): Indicates player turn.
        _game_state (str): Indicates game state.
        _white_pieces (list): List of white chess pieces.
        _black_pieces (list): List of black chess pieces.
    """

    def __init__(self):
        """
        Initializes a new ChessVar instance.

        This method does not require any arguments.
        The white-piece player has the first turn.

        Returns:
            None
        """
        self._board = Board()
        self._white = Player(['F', 'H'])
        self._black = Player(['f', 'h'])
        self._player_turn = 'WHITE'
        self._game_state = 'UNFINISHED'
        self._white_pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 'F', 'H']
        self._black_pieces = ['p', 'r', 'n', 'b', 'q', 'k', 'f', 'h']

    def get_board(self):
        """
        Retrieves _board.

        This method does not require any arguments.

        Returns:
            _board (Board): Board chess game is played on.
        """
        return self._board

    def get_game_state(self):
        """
        Retrieves _game_state.

        This method does not require any arguments.

        Returns:
            _game_state (str): Indicates game state.
        """
        return self._game_state

    def set_game_state(self, game_state):
        """
        Sets _game_state.

        Args:
            _game_state (str): Indicates game state.

        Returns:
            None
        """
        self._game_state = game_state

    def get_player_turn(self):
        """
        Retrieves _player_turn.

        This method does not require any arguments.

        Returns:
            _player_turn (str): Indicates player turn.
        """
        return self._player_turn

    def set_player_turn(self, color):
        """
        Sets _player_turn.

        Args:
            color (str): Player that has the current turn.

        Returns:
            None
        """
        self._player_turn = color

    def make_move(self, alg_start_coordinate, alg_end_coordinate):
        """
        Moves chess piece from start to end coordinate if allowed.

        Args:
            alg_start_coordinate (str): Piece's current position.
            alg_end_coordinate (str): Piece's potential end position.

        Returns:
            True or False (bool): Indicates if move was successful or unsuccessful.
        """
        # Checks several conditions for coordinates
        if self.verify_player_square(alg_start_coordinate, alg_end_coordinate) is False:
            return False

        # Checks if _game_state is unfinished
        if self.get_game_state() != "UNFINISHED":
            return False

        # Checks if move is valid
        piece = self._board.get_piece(alg_start_coordinate)
        valid_move = self.is_valid_move(piece, alg_start_coordinate, alg_end_coordinate)
        if valid_move is False:
            return False

        # Captures opponent piece, places player piece, and resets start position to be empty
        captured_piece = self._board.get_piece(alg_end_coordinate)
        self._board.remove_piece(alg_end_coordinate)
        self._board.place_piece(alg_end_coordinate, piece)
        self._board.remove_piece(alg_start_coordinate)

        # Updates variables related to fairy pieces, _game_state, _player_turn
        self.determine_fairy_piece(captured_piece)
        self.determine_winner(captured_piece)
        self.update_player_turn()
        return True

    def verify_player_square(self, alg_start_coordinate, alg_end_coordinate):
        """
        Checks that start and end coordinates are valid.

        Args:
            alg_start_coordinate (str): Piece's current position.
            alg_end_coordinate (str): Piece's potential end position.

        Returns:
            True or False (bool): Indicates if coordinates are valid or invalid.
        """
        # Checks if start and end coordinates are the same
        if alg_start_coordinate == alg_end_coordinate:
            return False

        # Checks if coordinates are out of bounds
        start_on_grid = self._board.alg_coordinate_to_list_index(alg_start_coordinate)
        end_on_grid = self._board.alg_coordinate_to_list_index(alg_end_coordinate)
        if (start_on_grid == [False, False]) or (end_on_grid == [False, False]):
            return False

        # Retrieves pieces from coordinates
        start_piece = self._board.get_piece(alg_start_coordinate)
        end_piece = self._board.get_piece(alg_end_coordinate)

        # Checks if start_piece is empty
        if start_piece == ".":
            return False

        # Checks conditions related to player and piece color
        # Checks if start_piece belongs to current player
        # Checks if end_piece, if there is any, belongs to opponent
        if self._player_turn == "WHITE":
           if (start_piece not in self._white_pieces) or (end_piece in self._white_pieces):
               return False

        if self._player_turn == "BLACK":
           if (start_piece not in self._black_pieces) or (end_piece in self._black_pieces):
              return False

        # All conditions passed
        return True

    def determine_fairy_piece(self, captured_piece):
        """
        Updates Player's _fairy_piece_entry and _capture_count.

        This method is called whenever a player's queen, rook, bishop, or knight is captured.
        When one of these pieces is taken, it allows the player to introduce a fairy piece.

        Args:
            captured_piece (str): Piece that was captured.

        Returns:
            None
        """
        # Updates _black fairy piece variables because black piece has been captured
        if (self._player_turn == "WHITE") and (captured_piece in ['q', 'r', 'b', 'n']):
            self._black.update_capture_count(1)
            self._black.update_fairy_piece_entry()

        # Updates _white fairy piece variables because white piece has been captured
        if (self._player_turn == "BLACK") and (captured_piece in ['Q', 'R', 'B', 'N']):
            self._white.update_capture_count(1)
            self._white.update_fairy_piece_entry()

    def determine_winner(self, captured_piece):
        """
        Updates _game_state if the game has a winner.

        This method is called whenever a player's king is captured.

        Args:
            captured_piece (str): Piece that was captured.

        Returns:
            None
        """
        if captured_piece == 'k':
            self._game_state = "WHITE_WON"
        elif captured_piece == 'K':
            self._game_state = "BLACK_WON"

    def update_player_turn(self):
        """
        Updates _player_turn.

        This method is called whenever a player has finished their turn.
        This method does not require any arguments.

        Returns:
            None
        """
        if self._player_turn == "WHITE":
            self._player_turn = "BLACK"
        else:
            self._player_turn = "WHITE"

    def is_valid_move(self, piece, alg_start_coordinate, alg_end_coordinate):
        """
        Checks if piece is allowed to move from start to end coordinate.

        This method is called whenever a player makes a move.

        Args:
            piece (str): Piece that will be moved.
            alg_start_coordinate (str): Start position of piece.
            alg_end_coordinate (str): Potential end position of piece.

        Returns:
            True or False (bool): Indicates if move is valid or invalid.
        """
        piece = piece.upper()

        # Calls the Pieces method that will validate the move of the piece
        if piece == 'R':
            return Pieces.is_valid_move_for_rook(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'B':
            return Pieces.is_valid_move_for_bishop(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'Q':
            return Pieces.is_valid_move_for_queen(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'N':
            return Pieces.is_valid_move_for_knight(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'K':
            return Pieces.is_valid_move_for_king(alg_start_coordinate, alg_end_coordinate, self)
        elif piece == 'P':
            return Pieces.is_valid_move_for_pawn(alg_start_coordinate, alg_end_coordinate,
                                                       self)
        elif piece == 'F':
            return Pieces.is_valid_move_for_falcon(alg_start_coordinate, alg_end_coordinate,
                                                       self)
        elif piece == 'H':
            return Pieces.is_valid_move_for_hunter(alg_start_coordinate, alg_end_coordinate,
                                                         self)

    def enter_fairy_piece(self, fairy_piece_type, placement_square):
        """
        Places the fairy piece on the board if it is allowed.

        Args:
            fairy_piece_type (str): Fairy piece that will be placed.
            placement_square (str): Square where fairy piece will be placed.

        Returns:
            True or False (bool): Indicates if placement is valid or invalid.
        """
        # Performs initial checks
        if self.verify_fairy_piece_and_position(fairy_piece_type, placement_square) is False:
            return False

        # Checks if player is allowed to place a fairy piece
        if self._player_turn == "WHITE":
            if self._white.get_fairy_piece_entry() is False:
                return False
            else:
                # Updates self._white attributes
                self.fairy_piece_actions(self._white, fairy_piece_type)

        if self._player_turn == "BLACK":
            if self._black.get_fairy_piece_entry() is False:
                return False
            else:
                # Updates self._black attributes
                self.fairy_piece_actions(self._black, fairy_piece_type)

        # Places fairy piece, updates turn
        self._board.place_piece(placement_square, fairy_piece_type)
        self.update_player_turn()
        return True

    def fairy_piece_actions(self, player, piece):
        """
        Updates Player attributes when a fairy piece is about to be placed.

        Args:
            player (Player): Player that will place the piece.
            piece (str): Fairy piece that will be placed.

        Returns:
            None
        """
        # Removes fairy piece from reserve list because it will be placed
        player.remove_from_reserve_list(piece)

        # Decrements _capture_count
        player.update_capture_count(-1)
        player.update_fairy_piece_entry

    def verify_fairy_piece_and_position(self, fairy_piece_type, placement_square):
        """
        Checks if the fairy piece and its placement are valid.

        Args:
            fairy_piece_type (str): Fairy piece that will be placed.
            placement_square (str): Square where fairy piece will be placed.

        Returns:
            True or False (bool): Indicates if placement is valid or invalid.
        """

        # Checks if placement square is out of bounds
        row, column = self._board.alg_coordinate_to_list_index(placement_square)
        if [row, column] == [False, False]:
            return False

        # Checks for white-piece player
        if self._player_turn == "WHITE":
            # Checks if placement_square is in home rank
            if row not in [6, 7]:
                return False
            # Checks if placement_square is empty
            if (self._board.get_piece_with_list_index([row, column]) != "."):
                return False
            # Checks if fairy_piece_type is valid
            if fairy_piece_type not in self._white.get_reserve_list():
                return False

        # Checks for black-piece player
        if self._player_turn == "BLACK":
            if row not in [0, 1]:
                return False
            if (self._board.get_piece_with_list_index([row, column]) != "."):
                return False
            if fairy_piece_type not in self._black.get_reserve_list():
                return False

        return True

def play_chess_game(game):
    while game.get_game_state() == "UNFINISHED":
        print(game.get_player_turn(), "TURN:")
        start, end, fairy = input("Enter move (start/end/fairy): ").split("/")
        if fairy == 'x':
            game.make_move(start, end)
        else:
            game.enter_fairy_piece(start, fairy)

    print(game.get_game_state())