import unittest
from ChessVar import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_initialization(self):
        """_board_display is correctly initialized"""
        board_display = self.board.get_board_display()
        correct_board_display = [
        ['8','r','n','b','q','k','b','n','r'],
        ['7','p','p','p','p','p','p','p','p'],
        ['6','.','.','.','.','.','.','.','.'],
        ['5','.','.','.','.','.','.','.','.'],
        ['4','.','.','.','.','.','.','.','.'],
        ['3','.','.','.','.','.','.','.','.'],
        ['2','P','P','P','P','P','P','P','P'],
        ['1','R','N','B','Q','K','B','N','R'],
        [' ','a','b','c','d','e','f','g','h']]
        self.assertEqual(board_display, correct_board_display)

    def test_alg_coordinate_to_list_index(self):
        """Algebraic coordinates are correctly converted to list index coordinates"""
        # 1: Checks valid algebraic coordinates
        reconstructed_board_display = []
        original_board_display = self.board.get_board_display()
        for j in ['8', '7', '6', '5', '4', '3', '2', '1']:
            row = []
            for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                list_index = self.board.alg_coordinate_to_list_index(i + j)
                row.append(original_board_display[list_index[0]][list_index[1]])
            reconstructed_board_display.append(row)

        # 2: Checks invalid algebraic coordinates
        self.assertEqual(self.board.alg_coordinate_to_list_index('z9'), [False, False])


    def test_piece_methods(self):
        """"Tests place_piece(), get_piece(), and remove_piece()"""

        # 1: Checks place_piece() and get_piece()
        self.board.place_piece('a8', '*')
        self.board.place_piece('d5', '*')
        self.board.place_piece('h1', '*')

        self.assertEqual(self.board.get_piece('a8'), '*')
        self.assertEqual(self.board.get_piece('d5'), '*')
        self.assertEqual(self.board.get_piece('h1'), '*')

        # 2: Checks remove_piece()
        self.board.remove_piece('a8')
        self.board.remove_piece('d5')
        self.board.remove_piece('h1')

        self.assertEqual(self.board.get_piece('a8'), '.')
        self.assertEqual(self.board.get_piece('d5'), '.')
        self.assertEqual(self.board.get_piece('h1'), '.')
