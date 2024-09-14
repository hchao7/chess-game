import unittest
from ChessVar import Player, Board, ChessVar, Pieces, play_chess_game

class TestClassVar(unittest.TestCase):

    # def test_game_end(self):
    #     # 1: Game ends when either king is captured
    #     # Enter moves
    #         # WHITE: d2/e3/x
    #
    #     game = ChessVar()
    #     board_display = [
    #     ['8','r','n','b','q','.','b','n','r'],
    #     ['7','p','p','p','p','p','p','p','p'],
    #     ['6','.','.','.','.','.','.','.','.'],
    #     ['5','.','.','.','.','.','.','.','.'],
    #     ['4','.','.','.','.','.','.','.','.'],
    #     ['3','.','.','.','.','k','.','.','.'],
    #     ['2','P','P','P','P','P','P','P','P'],
    #     ['1','R','N','B','Q','K','B','N','R'],
    #     [' ','a','b','c','d','e','f','g','h']]
    #
    #     game.get_board().set_board_display(board_display)
    #     play_chess_game(game)
    #     self.assertEqual(game.get_game_state(), "WHITE_WON")

    # def test_player_turns(self):
    #     # 1: Game switches between white-piece and black-piece players
    #     # Enter moves
    #         # WHITE: h6/f6/x, f6/f7/x, f7/g7/x
    #         # BLACK: d6/d2/x, d2/d1/x, d1/e1/x
    #
    #     game = ChessVar()
    #     pre_game_display = [
    #         ['8', 'r', 'n', 'b', '.', 'k', 'b', 'n', 'r'],
    #         ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    #         ['6', '.', '.', '.', 'q', '.', '.', '.', 'R'],
    #         ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['2', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    #         ['1', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', '.'],
    #         [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]
    #
    #     game.get_board().set_board_display(pre_game_display)
    #     play_chess_game(game)
    #     board = game.get_board().get_board_display()
    #     post_board_display = [
    #         ['8', 'r', 'n', 'b', '.', 'k', 'b', 'n', 'r'],
    #         ['7', 'p', 'p', 'p', 'p', 'p', '.', 'R', 'p'],
    #         ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['2', 'P', 'P', 'P', '.', 'P', 'P', 'P', 'P'],
    #         ['1', 'R', 'N', 'B', '.', 'q', 'B', 'N', '.'],
    #         [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]
    #
    #     self.assertEqual(game.get_game_state(), "BLACK_WON")
    #     self.assertEqual(board, post_board_display)

    def test_fairy_placement(self):
        # 1: Fairy pieces are placed during turns
        # Enter moves
            # WHITE: g5/h6/x, d1/x/F, g1/f3/x
            # BLACK: b6/c4/x, b8/x/h, f7/e6/x

        game = ChessVar()
        pre_game_display = [
            ['8', 'r', '.', 'b', 'q', 'k', 'b', 'n', '.'],
            ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['6', '.', 'n', '.', '.', 'K', '.', '.', 'r'],
            ['5', '.', '.', '.', '.', '.', '.', 'P', '.'],
            ['4', '.', '.', 'Q', '.', '.', '.', '.', '.'],
            ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['2', 'P', 'P', 'P', 'P', 'P', 'P', '.', 'P'],
            ['1', 'R', 'N', 'B', '.', '.', 'B', 'N', 'R'],
            [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        game.get_board().set_board_display(pre_game_display)
        play_chess_game(game)
        board = game.get_board().get_board_display()
        post_board_display = [
            ['8', 'r', 'h', 'b', 'q', 'k', 'b', 'n', '.'],
            ['7', 'p', 'p', 'p', 'p', 'p', '.', 'p', 'p'],
            ['6', '.', '.', '.', '.', 'p', '.', '.', 'P'],
            ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['4', '.', '.', 'n', '.', '.', '.', '.', '.'],
            ['3', '.', '.', '.', '.', '.', 'N', '.', '.'],
            ['2', 'P', 'P', 'P', 'P', 'P', 'P', '.', 'P'],
            ['1', 'R', 'N', 'B', 'F', '.', 'B', '.', 'R'],
            [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]

        self.assertEqual(game.get_game_state(), "BLACK_WON")
        self.assertEqual(board, post_board_display)