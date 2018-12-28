from unittest import TestCase
from metaknight.board import Board
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


class BoardTests(TestCase):
    def setUp(self):
        self.board = Board()

    def set_test_position_1(self):
        # This is a board state that I use to test certain functions
        self.board.set_board_state([
            'R..N.RK.',
            'PP.P.PPP',
            'n.P.Q.n.',
            'Bbp..pp.',
            '...Bp...',
            '..pp....',
            'pp...n.p',
            '.r.qr.k.',
        ])

    def test_board_construction(self):
        self.assertEqual(len(self.board.squares), 8)
        self.assertEqual(len(self.board.squares[0]), 8)
        self.assertEqual(self.board.squares[0][0], Square('a1'))
        self.assertEqual(self.board.squares[7][7], Square('h8'))

    def test_get_square(self):
        self.assertEqual(self.board.get_square(location='c4'), Square('c4'))
        self.assertEqual(self.board.get_square(location='a1'), Square('a1'))
        self.assertEqual(self.board.get_square(location='a8'), Square('a8'))
        self.assertEqual(self.board.get_square(location='h1'), Square('h1'))
        self.assertEqual(self.board.get_square(location='h8'), Square('h8'))
        self.assertRaises(ValueError, lambda: self.board.get_square(location='a9'))

    def test_set_up(self):
        b = '♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ ' \
            '\n♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ ' \
            '\n♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ '
        self.assertEqual(repr(Board()), b)

    def test_clear(self):
        b = '. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . ' \
            '\n. . . . . . . . '
        bo = Board()
        bo.clear()
        self.assertEqual(repr(bo), b)

    def test_pawn_moves(self):
        # TODO: en passant
        self.set_test_position_1()
        # white pawns
        self.assertEqual(self.board.pawn_moves(Square('a2')), [[Square('a3'), Square('a4')]])
        self.assertEqual(self.board.pawn_moves(Square('b2')), [[Square('b3'), Square('b4')]])
        self.assertEqual(self.board.pawn_moves(Square('c3')), [[Square('c4')], [Square('d4')]])
        self.assertEqual(self.board.pawn_moves(Square('d3')), [])
        self.assertEqual(self.board.pawn_moves(Square('e4')), [[Square('e5')]])
        self.assertEqual(self.board.pawn_moves(Square('f5')), [[Square('f6')], [Square('e6')]])
        self.assertEqual(self.board.pawn_moves(Square('g5')), [])
        self.assertEqual(self.board.pawn_moves(Square('h2')), [[Square('h3'), Square('h4')]])
        self.assertEqual(self.board.pawn_moves(Square('c5')), [])

        # black pawns
        self.assertEqual(self.board.pawn_moves(Square('a7')), [])
        self.assertEqual(self.board.pawn_moves(Square('b7')), [[Square('b6')], [Square('a6')]])
        self.assertEqual(self.board.pawn_moves(Square('c6')), [[Square('b5')]])
        self.assertEqual(self.board.pawn_moves(Square('d7')), [[Square('d6'), Square('d5')]])
        self.assertEqual(self.board.pawn_moves(Square('f7')), [[Square('f6')], [Square('g6')]])
        self.assertEqual(self.board.pawn_moves(Square('g7')), [])
        self.assertEqual(self.board.pawn_moves(Square('h7')), [[Square('h6'), Square('h5')], [Square('g6')]])

    def test_knight_moves(self):
        self.set_test_position_1()
        # white knights
        self.assertEqual(self.board.knight_moves(Square('a6')), [[Square('b8')], [Square('b4')], [Square('c7')]])
        self.assertEqual(self.board.knight_moves(Square('g6')), [[Square('f8')], [Square('h8')], [Square('f4')],
                                                                 [Square('h4')], [Square('e7')], [Square('e5')]])
        self.assertEqual(self.board.knight_moves(Square('f2')), [[Square('g4')], [Square('h3')], [Square('h1')]])
        # black knights
        self.assertEqual(self.board.knight_moves(Square('d8')), [])

    def test_bishop_moves(self):
        self.set_test_position_1()
        # white bishops
        self.assertEqual(self.board.bishop_moves(Square('b5')), [[Square('c6')], [Square('a4')], [Square('c4')]])
        # black bishops
        self.assertEqual(self.board.bishop_moves(Square('a5')), [[Square('b6'), Square('c7')],
                                                                 [Square('b4'), Square('c3')]])

    def test_rook_moves(self):
        self.set_test_position_1()
        # white rooks
        self.assertEqual(self.board.rook_moves(Square('b1')), [[Square('a1')], [Square('c1')]])
        self.assertEqual(self.board.rook_moves(Square('e1')), [[Square('e2'), Square('e3')], [Square('f1')]])
        # black rooks
        self.assertEqual(self.board.rook_moves(Square('a8')), [[Square('b8'), Square('c8')]])
        self.assertEqual(self.board.rook_moves(Square('f8')), [[Square('e8')]])

    def test_queen_moves(self):
        self.set_test_position_1()
        # white queen
        self.assertEqual(self.board.queen_moves(Square('d1')), [
            [Square('d2')], [Square('c1')], [Square('c2'), Square('b3'), Square('a4')],
            [Square('e2'), Square('f3'), Square('g4'), Square('h5')]])
        # black queen
        self.assertEqual(self.board.queen_moves(Square('e6')), [
            [Square('e7'), Square('e8')], [Square('e5'), Square('e4')], [Square('d6')], [Square('f6'), Square('g6')],
            [Square('d5'), Square('c4'), Square('b3'), Square('a2')], [Square('f5')]])

    def test_king_moves(self):
        self.set_test_position_1()
        print(self.board)
        # white king
        self.assertEqual(self.board.king_moves(Square('g1')), [[Square('g2')], [Square('h1')], [Square('f1')]])
        # black king
        self.assertEqual(self.board.king_moves(Square('g8')), [[Square('h8')]])
