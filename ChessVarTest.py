import unittest
from ChessVar import Player, Board, ChessVar, Pieces

class TestChessVar(unittest.TestCase):
    def setUp(self):
        self.chess_var = ChessVar()

    def test_verify_player_square_method(self):
        # 1: Checks if start and end coordinates are the same
        return_value_1 = self.chess_var.verify_player_square('a8', 'a8')
        self.assertEqual(return_value_1, False)

        # 2: Checks if coordinates are off the grid
        return_value_2 = self.chess_var.verify_player_square('8a', 'a1')
        return_value_3 = self.chess_var.verify_player_square('a1', '8a')
        self.assertEqual(return_value_2, False)
        self.assertEqual(return_value_3, False)

        # 3: Checks if start_piece is empty
        return_value_4 = self.chess_var.verify_player_square('a6', 'a1')
        self.assertEqual(return_value_4, False)

        # 4: Checks player-dependent conditions
        self.chess_var.set_player_turn("WHITE")
        # Returns False if piece on alg_start_coordinate is opponent's
        return_value_5 = self.chess_var.verify_player_square('c7', 'a4')
        return_value_6 = self.chess_var.verify_player_square('a2', 'c1')
        self.assertEqual(return_value_5, False)
        self.assertEqual(return_value_6, False)

        self.chess_var.set_player_turn("BLACK")
        # Returns False if piece on alg_start_coordinate is opponent's
        return_value_7 = self.chess_var.verify_player_square('b1', 'a6')
        # Returns False if piece on alg_end_coordinate is current player's
        return_value_8 = self.chess_var.verify_player_square('a7', 'b7')
        self.assertEqual(return_value_7, False)
        self.assertEqual(return_value_8, False)

        # 5: Returns True if all conditions passed
        return_value_9 = self.chess_var.verify_player_square('a7', 'b2')
        self.assertEqual(return_value_9, True)

    def test_make_move_method(self):
        # 1: Checks verify_player_square() is called correctly from within make_move()
        return_value_1 = self.chess_var.make_move('c7', 'a4')
        self.assertEqual(return_value_1, False)

        # 2: Return value is False when ChessVar's _game_state != "UNFINISHED"
        self.chess_var.set_game_state("WHITE_WON")
        return_value_2 = self.chess_var.make_move('b2', 'a7')
        self.assertEqual(return_value_2, False)

        # 3: Correctly captures piece, places new piece, and resets start coordinate to "."
        self.chess_var.set_game_state("UNFINISHED")
        self.chess_var._board.remove_piece('d2')
        d7_original_piece = self.chess_var._board.get_piece('d7')
        self.assertEqual(d7_original_piece, 'p')

        self.chess_var.make_move('d1', 'd7')
        d7_new_piece = self.chess_var._board.get_piece('d7')
        self.assertEqual(d7_new_piece, 'Q')

        d1_reset = self.chess_var._board.get_piece('d1')
        self.assertEqual(d1_reset, '.')

    def test_make_move_method_with_turns(self):
        # Checks that _player_turn switches between black and white-piece players
        return_value_1 = self.chess_var.get_player_turn()
        self.assertEqual(return_value_1, "WHITE")

        self.chess_var.make_move('b1', 'c3')
        return_value_2 = self.chess_var.get_player_turn()
        self.assertEqual(return_value_2, "BLACK")

        self.chess_var.make_move('b8', 'a6')
        return_value_3 = self.chess_var.get_player_turn()
        self.assertEqual(return_value_3, "WHITE")

        self.chess_var.make_move('g1', 'f3')
        return_value_4 = self.chess_var.get_player_turn()
        self.assertEqual(return_value_4, "BLACK")

    def test_make_move_and_determine_winner_methods(self):
        """Checks that make_move() calls determine_winner() correctly"""

        # 1: Checks that _game_state is updated to "WHITE_WON"
        board_display = [
                        ['8','r','n','b','q','k','b','n','r'],
                        ['7','p','p','p','p','.','p','p','p'],
                        ['6','.','.','.','.','.','.','.','.'],
                        ['5','.','.','.','.','.','.','.','.'],
                        ['4','.','.','.','.','Q','.','.','.'],
                        ['3','.','.','.','.','.','.','.','.'],
                        ['2','P','P','P','P','P','P','P','P'],
                        ['1','R','N','B','Q','K','B','N','R'],
                        [' ','a','b','c','d','e','f','g','h']]

        self.chess_var._board.set_board_display(board_display)
        self.chess_var.make_move('e4', 'e8')
        return_value_1 = self.chess_var.get_game_state()
        self.assertEqual(return_value_1, "WHITE_WON")

        # 2: Checks that _game_state is updated to "BLACK_WON"
        board_display = [
            ['8', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['3', '.', '.', '.', 'n', '.', '.', '.', '.'],
            ['2', 'P', 'P', 'P', 'P', '.', 'P', 'P', 'P'],
            ['1', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.chess_var.set_game_state("UNFINISHED")
        self.chess_var.set_player_turn("BLACK")
        self.chess_var._board.set_board_display(board_display)
        self.chess_var.make_move('d3', 'e1')
        return_value_2 = self.chess_var.get_game_state()
        self.assertEqual(return_value_2, "BLACK_WON")

    def test_is_valid_move_method(self):
        # 1: Checks that Pieces' is_valid_move_for_rook() is correctly called
        return_value_1 = self.chess_var.is_valid_move('R', 'e7', 'e4')
        self.assertEqual(return_value_1, True)

        return_value_2 = self.chess_var.is_valid_move('R', 'b3', 'c4')
        self.assertEqual(return_value_2, False)

    def test_determine_winner_method(self):
        # 1: Checks that _game_state is set to "WHITE_WON" when "k" is captured
        self.chess_var.determine_winner("k")
        return_value_1 = self.chess_var.get_game_state()
        self.assertEqual(return_value_1, "WHITE_WON")

        # 2: Checks that _game_state is set to "BLACK_WON" when "K" is captured
        self.chess_var.determine_winner("K")
        return_value_2 = self.chess_var.get_game_state()
        self.assertEqual(return_value_2, "BLACK_WON")

        # 3: Checks that _game_state is set to "UNFINISHED" if no "k/K" is captured
        self.chess_var.set_game_state("UNFINISHED")
        self.chess_var.determine_winner("K!")
        return_value_3 = self.chess_var.get_game_state()
        self.assertEqual(return_value_3, "UNFINISHED")

    def test_verify_fairy_piece_and_position_method(self):
        # Checks for white-piece player
        # 1: Position off board > False
        return_value_1 = self.chess_var.verify_fairy_piece_and_position('F', 'h9')
        self.assertEqual(return_value_1, False)

        # 2: Position NOT in home rank > False
        return_value_2 = self.chess_var.verify_fairy_piece_and_position('F', 'h2')
        self.assertEqual(return_value_2, False)

        # 3: Position NOT empty > False
        return_value_3 = self.chess_var.verify_fairy_piece_and_position('F', 'h1')
        self.assertEqual(return_value_3, False)

        # 4: Piece NOT in reserve list > False
        self.chess_var._board.remove_piece('e1')
        return_value_4 = self.chess_var.verify_fairy_piece_and_position('f', 'h1')
        self.assertEqual(return_value_4, False)

        # 5: Piece is correct AND position is empty
        return_value_5 = self.chess_var.verify_fairy_piece_and_position('F', 'e1')
        self.assertEqual(return_value_5, True)

        # Checks for black-piece player
        self.chess_var.set_player_turn("BLACK")

        # 1: Position off board > False
        return_value_1 = self.chess_var.verify_fairy_piece_and_position('f', 'h9')
        self.assertEqual(return_value_1, False)

        # 2: Position NOT in home rank > False
        return_value_2 = self.chess_var.verify_fairy_piece_and_position('f', 'h7')
        self.assertEqual(return_value_2, False)

        # 3: Position NOT empty > False
        return_value_3 = self.chess_var.verify_fairy_piece_and_position('f', 'h8')
        self.assertEqual(return_value_3, False)

        # 4: Piece NOT in reserve list > False
        self.chess_var._board.remove_piece('e8')
        return_value_4 = self.chess_var.verify_fairy_piece_and_position('F', 'e8')
        self.assertEqual(return_value_4, False)

        # 5: Piece is correct AND position is empty
        return_value_5 = self.chess_var.verify_fairy_piece_and_position('f', 'e8')
        self.assertEqual(return_value_5, True)

    def test_enter_fairy_piece_method(self):

        # Checks for white-piece player
        # 1: Checks successful placement of fairy piece
        board_display = [['8','r','n','b','q','k','b','n','r'],
                        ['7','p','p','p','p','p','p','p','p'],
                        ['6','.','.','.','.','.','.','.','.'],
                        ['5','.','.','.','.','.','.','.','.'],
                        ['4','.','.','.','.','.','.','.','.'],
                        ['3','.','.','.','.','.','.','.','.'],
                        ['2','P','P','P','P','P','P','P','P'],
                        ['1','R','N','B','.','K','B','N','R'],
                        [' ','a','b','c','d','e','f','g','h']]

        self.chess_var._board.set_board_display(board_display)
        self.chess_var._white.set_capture_count(2)
        self.chess_var._white.set_fairy_piece_entry(True)
        return_value_1 = self.chess_var.enter_fairy_piece("F",'d1')

        fairy_piece_display = [['8','r','n','b','q','k','b','n','r'],
                                ['7','p','p','p','p','p','p','p','p'],
                                ['6','.','.','.','.','.','.','.','.'],
                                ['5','.','.','.','.','.','.','.','.'],
                                ['4','.','.','.','.','.','.','.','.'],
                                ['3','.','.','.','.','.','.','.','.'],
                                ['2','P','P','P','P','P','P','P','P'],
                                ['1','R','N','B','F','K','B','N','R'],
                                [' ','a','b','c','d','e','f','g','h']]

        self.assertEqual(return_value_1, True)
        self.assertEqual(self.chess_var._white.get_reserve_list(), ["H"])
        self.assertEqual(self.chess_var._white.get_capture_count(), 1)
        self.assertEqual(self.chess_var._white.get_fairy_piece_entry(), True)
        self.assertEqual(self.chess_var._board.get_board_display(), fairy_piece_display)
        self.assertEqual(self.chess_var.get_player_turn(), "BLACK")

        # Checks for black-piece player
        # 1: Checks successful placement of fairy piece
        board_display_2 = [['8', 'r', 'n', 'b', 'q', 'k', 'b', '.', 'r'],
                         ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                         ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['2', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                         ['1', 'R', 'N', 'B', '.', 'K', 'B', 'N', 'R'],
                         [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.chess_var._board.set_board_display(board_display_2)
        self.chess_var._black.set_capture_count(2)
        self.chess_var._black.set_fairy_piece_entry(True)
        return_value_2 = self.chess_var.enter_fairy_piece("f", 'g8')

        fairy_piece_display_2 = [['8', 'r', 'n', 'b', 'q', 'k', 'b', 'f', 'r'],
                         ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                         ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['2', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                         ['1', 'R', 'N', 'B', '.', 'K', 'B', 'N', 'R'],
                         [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.assertEqual(return_value_2, True)
        self.assertEqual(self.chess_var._black.get_reserve_list(), ["h"])
        self.assertEqual(self.chess_var._black.get_capture_count(), 1)
        self.assertEqual(self.chess_var._black.get_fairy_piece_entry(), True)
        self.assertEqual(self.chess_var._board.get_board_display(), fairy_piece_display_2)
        self.assertEqual(self.chess_var.get_player_turn(), "WHITE")

    def test_make_moves_with_black_fairy_pieces_1(self):

        # 1: Fairy piece is not placed when Player's _fairy_piece_entry is false
        board_display = [['8', 'r', 'n', '.', 'q', '.', 'b', 'n', 'r'],
                         ['7', 'p', 'p', 'p', '.', 'p', 'p', 'p', 'p'],
                         ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['2', 'P', 'P', 'P', '.', 'P', 'P', 'P', 'P'],
                         ['1', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                         [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.chess_var._board.set_board_display(board_display)
        self.chess_var.make_move("d1", "d8")
        self.chess_var.enter_fairy_piece("f", "c8")

        fairy_piece_board_display = [['8', 'r', 'n', 'f', 'Q', '.', 'b', 'n', 'r'],
                                     ['7', 'p', 'p', 'p', '.', 'p', 'p', 'p', 'p'],
                                     ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
                                     ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
                                     ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
                                     ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
                                     ['2', 'P', 'P', 'P', '.', 'P', 'P', 'P', 'P'],
                                     ['1', 'R', 'N', 'B', '.', 'K', 'B', 'N', 'R'],
                                     [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.assertEqual(self.chess_var._board.get_board_display(), fairy_piece_board_display)
        self.chess_var.set_player_turn("BLACK")
        return_value_1 = self.chess_var.enter_fairy_piece("f", "e8")
        self.assertEqual(return_value_1, False)

    def test_make_moves_with_black_fairy_pieces_2(self):

        # 1: Can only place 2 fairy pieces max
        board_display = [['8','r','.','n','.','.','b','n','.'],
                         ['7','p','.','p','p','Q','.','p','p'],
                         ['6','.','.','B','.','.','.','.','.'],
                         ['5','.','.','.','B','.','.','.','.'],
                         ['4','.','.','.','.','.','.','.','.'],
                         ['3','.','.','.','.','.','.','.','.'],
                         ['2','P','P','P','P','P','P','P','P'],
                         ['1','R','N','B','Q','K','B','N','R'],
                         [' ','a','b','c','d','e','f','g','h']]

        self.chess_var._board.set_board_display(board_display)
        self.chess_var.make_move("d5", "g8")
        self.chess_var.enter_fairy_piece('h', 'h8')
        self.chess_var.make_move("c6", "a8")
        self.chess_var.enter_fairy_piece('f', 'b8')
        self.chess_var.make_move("e7", "e8")

        return_value_2 = self.chess_var.enter_fairy_piece('f', 'd8')
        self.assertEqual(return_value_2, False)

        fairy_piece_board_display = [['8', 'B', 'f', 'n', '.', 'Q', 'b', 'B', 'h'],
                         ['7', 'p', '.', 'p', 'p', '.', '.', 'p', 'p'],
                         ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
                         ['2', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                         ['1', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                         [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.assertEqual(self.chess_var._board.get_board_display(), fairy_piece_board_display)

    def test_make_moves_with_white_fairy_pieces(self):

        # 1: Can only place 2 fairy pieces max
        board_display = [['8','r','n','b','q','k','b','n','r'],
                         ['7','p','p','p','p','p','p','p','p'],
                         ['6','.','.','.','.','.','.','.','.'],
                         ['5','.','.','.','.','.','.','.','.'],
                         ['4','.','.','.','.','.','.','.','.'],
                         ['3','.','.','.','n','n','.','.','.'],
                         ['2','P','P','p','P','P','P','P','P'],
                         ['1','.','N','B','Q','K','B','.','.'],
                         [' ','a','b','c','d','e','f','g','h']]

        self.chess_var.set_player_turn("BLACK")
        self.chess_var._board.set_board_display(board_display)

        self.chess_var.make_move('d3', 'c1')
        self.chess_var.enter_fairy_piece('H', 'a1')
        self.chess_var.make_move('e3', 'd1')
        self.chess_var.make_move('h2', 'h3')
        self.chess_var.make_move('a7','a5')
        self.chess_var.enter_fairy_piece('F','h1')

        self.assertEqual(self.chess_var._white.get_fairy_piece_entry(), False)
        self.chess_var.make_move('c2', 'b1')
        self.assertEqual(self.chess_var._white.get_fairy_piece_entry(), False)

        fairy_piece_board_display = [['8','r','n','b','q','k','b','n','r'],
                             ['7','.','p','p','p','p','p','p','p'],
                             ['6','.','.','.','.','.','.','.','.'],
                             ['5','p','.','.','.','.','.','.','.'],
                             ['4','.','.','.','.','.','.','.','.'],
                             ['3','.','.','.','.','.','.','.','P'],
                             ['2','P','P','.','P','P','P','P','.'],
                             ['1','H','p','n','n','K','B','.','F'],
                             [' ','a','b','c','d','e','f','g','h']]

        self.assertEqual(self.chess_var._board.get_board_display(), fairy_piece_board_display)

