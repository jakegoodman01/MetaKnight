from unittest import TestCase
from metaknight import Board, Square, OutOfBoundsError


class SquareTests(TestCase):
    def setUp(self):
        self.square = Square('a1')

    def test_square_construction(self):
        self.assertEqual(self.square.rank, '1')
        self.assertEqual(self.square.file, 'a')

    def test_up(self):
        self.assertEqual(self.square.up(), Square('b1'))
        self.assertEqual(Square('b1').up(), Square('c1'))
        self.assertEqual(Square('c1').up(), Square('d1'))
        self.assertEqual(Square('d1').up(), Square('e1'))
        self.assertEqual(Square('e1').up(), Square('f1'))
        self.assertEqual(Square('f1').up(), Square('g1'))
        self.assertEqual(Square('g1').up(), Square('h1'))
        self.assertRaises(lambda: OutOfBoundsError, Square('h1').up())


class BoardTests(TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_construction(self):
        self.assertEqual(len(self.board.squares), 8)
        self.assertEqual(len(self.board.squares[0]), 8)
        self.assertEqual(self.board.squares[0][0], Square('a1'))
        self.assertEqual(self.board.squares[7][7], Square('h8'))
