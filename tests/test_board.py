from unittest import TestCase
from metaknight import Board


class SquareTests(TestCase):
    def setUp(self):
        pass


class BoardTests(TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_construction(self):
        self.assertEqual(len(self.board.squares), 8)
        self.assertEqual(len(self.board.squares)[0], 8)