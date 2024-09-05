import unittest
from ChessVar import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.white_piece_player = Player(['F', 'H'])
        self.black_piece_player = Player(['f', 'h'])

    def test_update_fairy_piece_entry(self):
        self.white_piece_player.remove_from_reserve_list('F')
        self.white_piece_player.remove_from_reserve_list('H')

        # 1. Check with empty reserve list > FALSE
        self.white_piece_player.update_fairy_piece_entry()
        self.assertEqual(self.white_piece_player.get_fairy_piece_entry(), False)

        # 2. Check with full reserve list + capture_count = 0 > FALSE
        self.white_piece_player.set_reserve_list(['F', 'H'])
        self.white_piece_player.update_fairy_piece_entry()
        self.assertEqual(self.white_piece_player.get_fairy_piece_entry(), False)

        # 3. Check with capture_count = 0 > TRUE
        self.white_piece_player.set_capture_count(2)
        self.white_piece_player.update_fairy_piece_entry()
        self.assertEqual(self.white_piece_player.get_fairy_piece_entry(), True)

    def test_update_capture_count(self):
        # 1. Check decrement of capture count
        self.white_piece_player.update_capture_count(-1)
        self.assertEqual(self.white_piece_player.get_capture_count(), -1)

        # 2. Check increment of capture count
        self.white_piece_player.update_capture_count(1)
        self.assertEqual(self.white_piece_player.get_capture_count(), 0)
