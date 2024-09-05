import unittest
from ChessVar import Board, Pieces, ChessVar


class TestPieces(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.pieces = Pieces()
        self.chess_var = ChessVar()

    def test_identify_direction(self):
        """Check cardinal direction player wants to move piece in"""

        # 1. Check NORTH
        return_value_1 = self.pieces.identify_direction('b1', 'b8', self.board)
        return_value_2 = self.pieces.identify_direction('c5', 'c8', self.board)
        self.assertEqual(return_value_1, 'NORTH')
        self.assertEqual(return_value_2, 'NORTH')

        # 2. Check SOUTH
        return_value_3 = self.pieces.identify_direction('b8', 'b1', self.board)
        return_value_4 = self.pieces.identify_direction('c8', 'c5', self.board)
        self.assertEqual(return_value_3, 'SOUTH')
        self.assertEqual(return_value_4, 'SOUTH')

        # 3. Check EAST
        return_value_5 = self.pieces.identify_direction('a5', 'h5', self.board)
        return_value_6 = self.pieces.identify_direction('c3', 'd3', self.board)
        self.assertEqual(return_value_5, 'EAST')
        self.assertEqual(return_value_6, 'EAST')

        # 4. Check WEST
        return_value_7 = self.pieces.identify_direction('h5', 'a5', self.board)
        return_value_8 = self.pieces.identify_direction('d3', 'c3', self.board)
        self.assertEqual(return_value_7, 'WEST')
        self.assertEqual(return_value_8, 'WEST')

        # 5. Check NORTHEAST
        return_value_9 = self.pieces.identify_direction('c3', 'f6', self.board)
        return_value_10 = self.pieces.identify_direction('c3', 'd6', self.board)
        self.assertEqual(return_value_9, 'NORTHEAST')
        self.assertEqual(return_value_10, 'N/A')

        # 6. Check NORTHWEST
        return_value_11 = self.pieces.identify_direction('d3', 'b5', self.board)
        return_value_12 = self.pieces.identify_direction('d3', 'a5', self.board)
        self.assertEqual(return_value_11, 'NORTHWEST')
        self.assertEqual(return_value_12, 'N/A')

        # 7. Check SOUTHWEST
        return_value_13 = self.pieces.identify_direction('h8', 'a1', self.board)
        return_value_14 = self.pieces.identify_direction('h8', 'a2', self.board)
        self.assertEqual(return_value_13, 'SOUTHWEST')
        self.assertEqual(return_value_14, 'N/A')

        # 8. Check SOUTHEAST
        return_value_15 = self.pieces.identify_direction('b7', 'f3', self.board)
        return_value_16 = self.pieces.identify_direction('b7', 'c3', self.board)
        self.assertEqual(return_value_15, 'SOUTHEAST')
        self.assertEqual(return_value_16, 'N/A')

    def test_identify_blocked_square(self):
        """Check for blocked squares in all cardinal directions"""

        # 1. Check NORTH
        # Blocked, Unblocked
        return_value_1 = self.pieces.identify_blocked_square('b3', 'b8',
                                                             'NORTH', self.board)
        return_value_2 = self.pieces.identify_blocked_square('d2', 'd6', 'NORTH', self.board)
        self.assertEqual(return_value_1, False)
        self.assertEqual(return_value_2, True)

        # 2. Check SOUTH
        return_value_3 = self.pieces.identify_blocked_square('a8', 'a5',
                                                             'SOUTH', self.board)
        return_value_4 = self.pieces.identify_blocked_square('b7', 'b2', 'SOUTH', self.board)
        self.assertEqual(return_value_3, False)
        self.assertEqual(return_value_4, True)

        # 3. Check EAST
        self.board.place_piece('d6', 'P')
        return_value_5 = self.pieces.identify_blocked_square('b6', 'e6',
                                                             'EAST', self.board)
        self.board.remove_piece('d6')
        return_value_6 = self.pieces.identify_blocked_square('b6', 'e6',
                                                             'EAST', self.board)
        self.assertEqual(return_value_5, False)
        self.assertEqual(return_value_6, True)

        # 4. Check WEST
        self.board.place_piece('d6', 'P')
        return_value_7 = self.pieces.identify_blocked_square('e6', 'b6',
                                                             'WEST', self.board)
        self.board.remove_piece('d6')
        return_value_8 = self.pieces.identify_blocked_square('e6', 'b6',
                                                             'WEST', self.board)
        self.assertEqual(return_value_7, False)
        self.assertEqual(return_value_8, True)

        # 5. Check NORTHEAST
        self.board.place_piece('d5', 'P')
        return_value_9 = self.pieces.identify_blocked_square('b3', 'e6',
                                                             'NORTHEAST', self.board)
        self.board.remove_piece('d5')
        return_value_10 = self.pieces.identify_blocked_square('e6', 'b6',
                                                             'NORTHEAST', self.board)
        self.assertEqual(return_value_9, False)
        self.assertEqual(return_value_10, True)

        # 6. Check SOUTHEAST
        return_value_11 = self.pieces.identify_blocked_square('a6', 'f1',
                                                             'SOUTHEAST', self.board)
        return_value_12 = self.pieces.identify_blocked_square('e5', 'g3',
                                                             'SOUTHEAST', self.board)
        self.assertEqual(return_value_11, False)
        self.assertEqual(return_value_12, True)

        # 7. Check SOUTHWEST
        return_value_13 = self.pieces.identify_blocked_square('g4', 'd1',
                                                              'SOUTHWEST', self.board)
        return_value_14 = self.pieces.identify_blocked_square('e6', 'b3',
                                                              'SOUTHWEST', self.board)
        self.assertEqual(return_value_13, False)
        self.assertEqual(return_value_14, True)

        # 7. Check NORTHWEST
        return_value_15 = self.pieces.identify_blocked_square('c6', 'a8',
                                                              'NORTHWEST', self.board)
        return_value_16 = self.pieces.identify_blocked_square('f2', 'a7',
                                                              'NORTHWEST', self.board)
        self.assertEqual(return_value_15, False)
        self.assertEqual(return_value_16, True)

    def test_is_valid_move_for_rook(self):
        # 1. Check diagonal
        return_value_1 = self.pieces.is_valid_move_for_rook('b3', 'c4', self.chess_var)
        self.assertEqual(return_value_1, False)

        # 2. Check NORTH - blocked
        return_value_2 = self.pieces.is_valid_move_for_rook('b1', 'b8', self.chess_var)
        self.assertEqual(return_value_2, False)

        # 3. Check SOUTH - not blocked
        return_value_3 = self.pieces.is_valid_move_for_rook('e7', 'e4', self.chess_var)
        self.assertEqual(return_value_3, True)

        # 4. Check EAST - blocked
        self.chess_var._board.place_piece('e3', 'X')
        return_value_4 = self.pieces.is_valid_move_for_rook('d3', 'h3', self.chess_var)
        self.assertEqual(return_value_4, False)

        # 5. Check WEST - not blocked
        self.chess_var._board.remove_piece('e3')
        return_value_5 = self.pieces.is_valid_move_for_rook('h3', 'd3', self.chess_var)
        self.assertEqual(return_value_5, True)

    def test_is_valid_move_for_bishop(self):
        # 1. Check NORTHEAST - blocked
        self.chess_var._board.place_piece('d5', 'X')
        return_value_1 = self.pieces.is_valid_move_for_bishop('b3', 'e6', self.chess_var)
        self.assertEqual(return_value_1, False)

        # 2. Check SOUTHWEST - not blocked
        self.chess_var._board.remove_piece('d5')
        return_value_2 = self.pieces.is_valid_move_for_bishop('e6', 'b3', self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. Check NORTHWEST - blocked
        return_value_3 = self.pieces.is_valid_move_for_bishop('g1', 'b6', self.chess_var)
        self.assertEqual(return_value_3, False)

        # 4. Check SOUTHEAST - not blocked
        return_value_4 = self.pieces.is_valid_move_for_bishop('d6', 'g3', self.chess_var)
        self.assertEqual(return_value_4, True)

        # 5. Check invalid direction
        return_value_5 = self.pieces.is_valid_move_for_bishop('c3', 'f4', self.chess_var)
        self.assertEqual(return_value_5, False)

    def test_is_valid_move_for_queen(self):
        # 1. Check NORTH - blocked
        return_value_1 = self.pieces.is_valid_move_for_queen('b1', 'b8', self.chess_var)
        self.assertEqual(return_value_1, False)

        # 2. Check SOUTH - not blocked
        return_value_2 = self.pieces.is_valid_move_for_queen('e7', 'e4', self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. Check EAST - blocked
        self.chess_var._board.place_piece('e3', 'X')
        return_value_3 = self.pieces.is_valid_move_for_queen('d3', 'h3', self.chess_var)
        self.assertEqual(return_value_3, False)

        # 4. Check WEST - not blocked
        self.chess_var._board.remove_piece('e3')
        return_value_4 = self.pieces.is_valid_move_for_queen('h3', 'd3', self.chess_var)
        self.assertEqual(return_value_4, True)

        # 5. Check NORTHEAST - blocked
        self.chess_var._board.place_piece('d5', 'X')
        return_value_5 = self.pieces.is_valid_move_for_queen('b3', 'e6', self.chess_var)
        self.assertEqual(return_value_5, False)

        # 6. Check SOUTHWEST - not blocked
        self.chess_var._board.remove_piece('d5')
        return_value_6 = self.pieces.is_valid_move_for_queen('e6', 'b3', self.chess_var)
        self.assertEqual(return_value_6, True)

        # 7. Check NORTHWEST - blocked
        return_value_7 = self.pieces.is_valid_move_for_queen('g1', 'b6', self.chess_var)
        self.assertEqual(return_value_7, False)

        # 8. Check SOUTHEAST - not blocked
        return_value_8 = self.pieces.is_valid_move_for_queen('d6', 'g3', self.chess_var)
        self.assertEqual(return_value_8, True)

        # 9. Check invalid direction
        return_value_9 = self.pieces.is_valid_move_for_queen('c3', 'f4', self.chess_var)
        self.assertEqual(return_value_9, False)

    def test_is_valid_move_for_knight(self):
        # 1. Check NORTHEAST, 2 options
        return_value_1 = self.pieces.is_valid_move_for_knight('d4', 'f5', self.chess_var)
        self.assertEqual(return_value_1, True)
        return_value_2 = self.pieces.is_valid_move_for_knight('d4', 'e6', self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. Check SOUTHEAST, 2 options
        return_value_3 = self.pieces.is_valid_move_for_knight('d4', 'f3', self.chess_var)
        self.assertEqual(return_value_3, True)
        return_value_4 = self.pieces.is_valid_move_for_knight('d4', 'e2', self.chess_var)
        self.assertEqual(return_value_4, True)

        # 5. Check SOUTHWEST, 2 options
        return_value_5 = self.pieces.is_valid_move_for_knight('d4', 'c2', self.chess_var)
        self.assertEqual(return_value_5, True)
        return_value_6 = self.pieces.is_valid_move_for_knight('d4', 'b3', self.chess_var)
        self.assertEqual(return_value_6, True)

        # 4. Check NORTHWEST, 2 options
        return_value_7 = self.pieces.is_valid_move_for_knight('d4', 'c6', self.chess_var)
        self.assertEqual(return_value_7, True)
        return_value_8 = self.pieces.is_valid_move_for_knight('d4', 'b5', self.chess_var)
        self.assertEqual(return_value_8, True)

        # 5. Check INVALID DIRECTION
        return_value_9 = self.pieces.is_valid_move_for_knight('d4', 'h6', self.chess_var)
        self.assertEqual(return_value_9, False)

    def test_is_valid_move_for_king(self):
        # 1. Check NORTH, EAST, SOUTH, WEST
        return_value_1 = self.pieces.is_valid_move_for_king('f6', 'f7', self.chess_var)
        self.assertEqual(return_value_1, True)

        return_value_2 = self.pieces.is_valid_move_for_king('f6', 'g6', self.chess_var)
        self.assertEqual(return_value_2, True)

        return_value_3 = self.pieces.is_valid_move_for_king('f6', 'f5', self.chess_var)
        self.assertEqual(return_value_3, True)

        return_value_4 = self.pieces.is_valid_move_for_king('f6', 'e6', self.chess_var)
        self.assertEqual(return_value_4, True)

        # 2. Check NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST
        return_value_5 = self.pieces.is_valid_move_for_king('f6', 'g7', self.chess_var)
        self.assertEqual(return_value_5, True)

        return_value_6 = self.pieces.is_valid_move_for_king('f6', 'g5', self.chess_var)
        self.assertEqual(return_value_6, True)

        return_value_7 = self.pieces.is_valid_move_for_king('f6', 'e5', self.chess_var)
        self.assertEqual(return_value_7, True)

        return_value_8 = self.pieces.is_valid_move_for_king('f6', 'e7', self.chess_var)
        self.assertEqual(return_value_8, True)

        # 3. Check INVALID direction
        return_value_9 = self.pieces.is_valid_move_for_king('f6', 'f4', self.chess_var)
        self.assertEqual(return_value_9, False)

    def test_is_valid_move_for_pawn_black(self):

        # BLACK pawn
        # 1. No capture: 2 squares - True
        self.chess_var.set_player_turn("BLACK")
        return_value_1 = self.pieces.is_valid_move_for_pawn('c7', 'c5', self.chess_var)
        self.assertEqual(return_value_1, True)

        # 2. No capture: 1 square - True
        return_value_2 = self.pieces.is_valid_move_for_pawn('c5', 'c4', self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. No capture: 2 squares, 2nd blocked - False
        new_board_display = [['8', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                             ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                             ['6', '.', '.', '.', '.', '.', 'X', '.', '.'],
                             ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
                             ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
                             ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
                             ['2', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                             ['1', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                             [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.chess_var._board.set_board_display(new_board_display)
        return_value_3 = self.pieces.is_valid_move_for_pawn('f7', 'f5', self.chess_var)
        self.assertEqual(return_value_3, False)

        # 4. No capture: 1 square, 1st blocked - False
        return_value_4 = self.pieces.is_valid_move_for_pawn('f5', 'f6', self.chess_var)
        self.assertEqual(return_value_4, False)

        # 5. Capture: SOUTHEAST direction - True
        new_board_display_2 = [['8', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                               ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                               ['6', '.', '.', 'X', '.', 'X', '.', '.', '.'],
                               ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
                               ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
                               ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
                               ['2', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                               ['1', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                               [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.chess_var._board.set_board_display(new_board_display_2)
        return_value_5 = self.pieces.is_valid_move_for_pawn('d7', 'e6', self.chess_var)
        self.assertEqual(return_value_5, True)

        # 6. Capture: SOUTHWEST direction - True
        return_value_6 = self.pieces.is_valid_move_for_pawn('d7', 'c6', self.chess_var)
        self.assertEqual(return_value_6, True)

        # 7. Capture: SOUTHEAST direction - False (nothing to capture)
        return_value_7 = self.pieces.is_valid_move_for_pawn('f7', 'g6', self.chess_var)
        self.assertEqual(return_value_7, False)

    def test_is_valid_move_for_pawn_white(self):

        # WHITE pawn
        # 1. No capture: 2 squares - True
        return_value_1 = self.pieces.is_valid_move_for_pawn('c2', 'c4', self.chess_var)
        self.assertEqual(return_value_1, True)

        # 2. No capture: 1 square - True
        return_value_2 = self.pieces.is_valid_move_for_pawn('c4', 'c5', self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. No capture: 2 squares, 2nd blocked - False
        new_board_display = [['8','r','n','b','q','k','b','n','r'],
                            ['7','p','p','p','p','.','p','p','p'],
                            ['6','.','.','.','.','.','.','.','.'],
                            ['5','.','.','.','.','.','.','.','.'],
                            ['4','.','.','.','.','.','.','.','.'],
                            ['3','.','.','.','.','.','X','.','.'],
                            ['2','P','P','P','P','P','P','P','P'],
                            ['1','R','N','B','Q','K','B','N','R'],
                            [' ','a','b','c','d','e','f','g','h']]

        self.chess_var._board.set_board_display(new_board_display)
        return_value_3 = self.pieces.is_valid_move_for_pawn('f2', 'f4', self.chess_var)
        self.assertEqual(return_value_3, False)

        # 4. No capture: 1 square, 1st blocked - False
        return_value_4 = self.pieces.is_valid_move_for_pawn('f2', 'f3', self.chess_var)
        self.assertEqual(return_value_4, False)

        # 5. Capture: NORTHEAST direction - True
        new_board_display_2 = [['8', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                             ['7', 'p', 'p', 'p', 'p', '.', 'p', 'p', 'p'],
                             ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
                             ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
                             ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
                             ['3', '.', '.', 'X', '.', 'X', '.', '.', '.'],
                             ['2', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                             ['1', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                             [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.chess_var._board.set_board_display(new_board_display_2)
        return_value_5 = self.pieces.is_valid_move_for_pawn('d2', 'e3', self.chess_var)
        self.assertEqual(return_value_5, True)

        # 6. Capture: NORTHWEST direction - True
        return_value_6 = self.pieces.is_valid_move_for_pawn('d2', 'c3', self.chess_var)
        self.assertEqual(return_value_6, True)

        # 7. Capture: NORTHEAST direction - False (nothing to capture)
        return_value_7 = self.pieces.is_valid_move_for_pawn('f2', 'g3', self.chess_var)
        self.assertEqual(return_value_7, False)

    def test_is_valid_move_for_falcon_white(self):
        # 1. Check NORTHWEST - Blocked
        return_value_1 = self.pieces.is_valid_move_for_falcon('c6', 'a8',
                                                              self.chess_var)
        self.assertEqual(return_value_1, False)

        # 2. Check NORTHEAST - Not blocked
        return_value_2 = self.pieces.is_valid_move_for_falcon('c3', 'f6',
                                                              self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. Check SOUTH - Not blocked
        return_value_3 = self.pieces.is_valid_move_for_falcon('d6', 'd3',
                                                              self.chess_var)
        self.assertEqual(return_value_3, True)

        # 4. Check SOUTHEAST - Not blocked
        return_value_4 = self.pieces.is_valid_move_for_falcon('d6', 'g3',
                                                              self.chess_var)
        self.assertEqual(return_value_4, False)

    def test_is_valid_move_for_falcon_black(self):
        # 1. Check SOUTHWEST - Blocked
        self.chess_var.set_player_turn("BLACK")
        return_value_1 = self.pieces.is_valid_move_for_falcon('g8', 'd5',
                                                              self.chess_var)
        self.assertEqual(return_value_1, False)

        # 2. Check SOUTHEAST - Not blocked
        return_value_2 = self.pieces.is_valid_move_for_falcon('b7', 'e4',
                                                              self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. Check NORTH - Not blocked
        return_value_3 = self.pieces.is_valid_move_for_falcon('d3', 'd6',
                                                              self.chess_var)
        self.assertEqual(return_value_3, True)

        # 4. Check NORTHEAST - Not blocked
        return_value_4 = self.pieces.is_valid_move_for_falcon('a2', 'd5',
                                                              self.chess_var)
        self.assertEqual(return_value_4, False)

    def test_is_valid_move_for_hunter_white(self):
        # 1. Check SOUTHWEST - Blocked
        return_value_1 = self.pieces.is_valid_move_for_hunter('g8', 'd5',
                                                              self.chess_var)
        self.assertEqual(return_value_1, False)

        # 2. Check SOUTHEAST - Not blocked
        return_value_2 = self.pieces.is_valid_move_for_hunter('b7', 'e4',
                                                              self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. Check NORTH - Not blocked
        return_value_3 = self.pieces.is_valid_move_for_hunter('d3', 'd6',
                                                              self.chess_var)
        self.assertEqual(return_value_3, True)

        # 4. Check NORTHEAST - Not blocked
        return_value_4 = self.pieces.is_valid_move_for_hunter('a2', 'd5',
                                                              self.chess_var)
        self.assertEqual(return_value_4, False)

    def test_is_valid_move_for_hunter_black(self):
        # 1. Check NORTHWEST - Blocked
        self.chess_var.set_player_turn("BLACK")
        return_value_1 = self.pieces.is_valid_move_for_hunter('c6', 'a8',
                                                              self.chess_var)
        self.assertEqual(return_value_1, False)

        # 2. Check NORTHEAST - Not blocked
        return_value_2 = self.pieces.is_valid_move_for_hunter('c3', 'f6',
                                                              self.chess_var)
        self.assertEqual(return_value_2, True)

        # 3. Check SOUTH - Not blocked
        return_value_3 = self.pieces.is_valid_move_for_hunter('d6', 'd3',
                                                              self.chess_var)
        self.assertEqual(return_value_3, True)

        # 4. Check SOUTHEAST - Not blocked
        return_value_4 = self.pieces.is_valid_move_for_hunter('d6', 'g3',
                                                              self.chess_var)
        self.assertEqual(return_value_4, False)
