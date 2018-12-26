from unittest import TestCase
from metaknight import Board, Square, OutOfBoundsError


class SquareTests(TestCase):
    def setUp(self):
        self.square = Square('a1')

    def test_square_construction(self):
        self.assertEqual(self.square.rank, '1')
        self.assertEqual(self.square.file, 'a')

    def test_up(self):
        self.assertEqual(self.square.up(), Square('a2'))
        self.assertEqual(Square('a2').up(), Square('a3'))
        self.assertEqual(Square('a3').up(), Square('a4'))
        self.assertEqual(Square('a4').up(), Square('a5'))
        self.assertEqual(Square('a5').up(), Square('a6'))
        self.assertEqual(Square('a6').up(), Square('a7'))
        self.assertEqual(Square('a7').up(), Square('a8'))
        self.assertRaises(lambda: OutOfBoundsError, Square('a8').up())


class BoardTests(TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_construction(self):
        self.assertEqual(len(self.board.squares), 8)
        self.assertEqual(len(self.board.squares[0]), 8)
        self.assertEqual(self.board.squares[0][0], Square('a1'))
        self.assertEqual(self.board.squares[7][7], Square('h8'))
