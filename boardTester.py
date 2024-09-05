import unittest
from experiment import coordinates_to_index

class TestCoordinates_To_Index(unittest.TestCase):

    def test_coord_to_index(self):
        self.assertEqual(coordinates_to_index('b2'), ('b','2'))

board1 = Board()
chessVar1 = ChessVar()
# created a private data member called "._board"
# actual_board = ._board.get_board()
# ._board.coordinates_to_index() > return list index (list)
# ._board.get_piece() > return piece (string)
# self.verify_player_square(piece)
# self.is_valid_move(piece, start_coordinate, end_coordinate)
