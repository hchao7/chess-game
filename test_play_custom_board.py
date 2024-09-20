import unittest
from ChessVar import Player, Board, ChessVar, Pieces, play_custom_board

class TestPlayCustomBoardMethod(unittest.TestCase):

    def test_game_end(self):
        # 1: Game ends when either player's king is captured
        # Enter moves
            # WHITE: d2/e3/x

        board = [
        ['8','r','n','b','q','.','b','n','r'],
        ['7','p','p','p','p','p','p','p','p'],
        ['6','.','.','.','.','.','.','.','.'],
        ['5','.','.','.','.','.','.','.','.'],
        ['4','.','.','.','.','.','.','.','.'],
        ['3','.','.','.','.','k','.','.','.'],
        ['2','P','P','P','P','P','P','P','P'],
        ['1','R','N','B','Q','K','B','N','R'],
        [' ','a','b','c','d','e','f','g','h']]
        play_custom_board(board)

    def test_player_turns(self):
        # 1: Game switches between white-piece and black-piece players
        # Enter moves
            # WHITE: h6/f6/x, f6/f7/x, f7/g7/x
            # BLACK: d6/d2/x, d2/d1/x, d1/e1/x

        board = [
            ['8', 'r', 'n', 'b', '.', 'k', 'b', 'n', 'r'],
            ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['6', '.', '.', '.', 'q', '.', '.', '.', 'R'],
            ['5', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['4', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['2', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['1', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', '.'],
            [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]
        play_custom_board(board)

    def test_fairy_placement(self):
        # 1: Fairy pieces are placed during turns
        # Enter moves
            # WHITE: g5/h6/x, d1/x/F, g1/f3/x, a1/x/H, e1/x/H
            # BLACK: b6/c4/x, b8/x/h, b7/a6/x, d8/x/f

        board = [
            ['8', 'r', '.', 'b', '.', 'k', 'b', 'n', '.'],
            ['7', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['6', 'R', 'n', '.', '.', 'K', '.', '.', 'r'],
            ['5', '.', '.', '.', '.', '.', '.', 'P', '.'],
            ['4', '.', '.', 'Q', '.', '.', '.', '.', '.'],
            ['3', '.', '.', '.', '.', '.', 'q', '.', '.'],
            ['2', 'P', 'P', 'P', 'P', 'P', 'P', '.', 'P'],
            ['1', '.', 'N', 'B', '.', '.', 'B', 'N', 'R'],
            [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']]
        play_custom_board(board)