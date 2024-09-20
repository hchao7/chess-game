import unittest
from ChessVar import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.white_piece_player = Player(['F', 'H'])
        self.black_piece_player = Player(['f', 'h'])

    def test_update_fairy_piece_entry_method(self):
        self.white_piece_player.remove_from_reserve_list('F')
        self.white_piece_player.remove_from_reserve_list('H')

        # 1: Checks that empty _reserve_list returns False
        self.white_piece_player.update_fairy_piece_entry()
        self.assertEqual(self.white_piece_player.get_fairy_piece_entry(), False)

        # 2: Checks that full _reserve_list and _capture_count of 0 returns False
        self.white_piece_player.set_reserve_list(['F', 'H'])
        self.white_piece_player.update_fairy_piece_entry()
        self.assertEqual(self.white_piece_player.get_fairy_piece_entry(), False)

        # 3: Checks that a _capture_count greater than 0 returns True
        self.white_piece_player.set_capture_count(2)
        self.white_piece_player.update_fairy_piece_entry()
        self.assertEqual(self.white_piece_player.get_fairy_piece_entry(), True)

    def test_update_capture_count_method(self):
        # 1: Checks decrement of _capture_count
        self.white_piece_player.update_capture_count(-1)
        self.assertEqual(self.white_piece_player.get_capture_count(), -1)

        # 2: Checks increment of _capture_count
        self.white_piece_player.update_capture_count(1)
        self.assertEqual(self.white_piece_player.get_capture_count(), 0)
