from unittest import TestCase
from metaknight.square import Square


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
        self.assertEqual(Square('a8').up(), Square('00'))

    def test_down(self):
        self.assertEqual(Square('a8').down(), Square('a7'))
        self.assertEqual(Square('a7').down(), Square('a6'))
        self.assertEqual(Square('a6').down(), Square('a5'))
        self.assertEqual(Square('a5').down(), Square('a4'))
        self.assertEqual(Square('a4').down(), Square('a3'))
        self.assertEqual(Square('a3').down(), Square('a2'))
        self.assertEqual(Square('a2').down(), Square('a1'))
        self.assertEqual(self.square.down(), Square('00'))

    def test_right(self):
        self.assertEqual(self.square.right(), Square('b1'))
        self.assertEqual(Square('b1').right(), Square('c1'))
        self.assertEqual(Square('c1').right(), Square('d1'))
        self.assertEqual(Square('d1').right(), Square('e1'))
        self.assertEqual(Square('e1').right(), Square('f1'))
        self.assertEqual(Square('f1').right(), Square('g1'))
        self.assertEqual(Square('g1').right(), Square('h1'))
        self.assertEqual(Square('h1').right(), Square('00'))

    def test_left(self):
        self.assertEqual(Square('h8').left(), Square('g8'))
        self.assertEqual(Square('g8').left(), Square('f8'))
        self.assertEqual(Square('f8').left(), Square('e8'))
        self.assertEqual(Square('e8').left(), Square('d8'))
        self.assertEqual(Square('d8').left(), Square('c8'))
        self.assertEqual(Square('c8').left(), Square('b8'))
        self.assertEqual(Square('b8').left(), Square('a8'))
        self.assertEqual(self.square.left(), Square('00'))
