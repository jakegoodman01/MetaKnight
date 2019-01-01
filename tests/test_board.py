from unittest import TestCase
from metaknight.board import Board
from metaknight.square import Square
from metaknight.piece import Color


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

    def set_test_position_2(self):
        # This is a board state that I use to test certain functions
        self.board.set_board_state([
            '........',
            '..K..r..',
            '........',
            '........',
            '........',
            '...N.k..',
            '........',
            '........',
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
        self.assertEqual(self.board._pawn_moves(Square('a2')), [[Square('a3'), Square('a4')]])
        self.assertEqual(self.board._pawn_moves(Square('b2')), [[Square('b3'), Square('b4')]])
        self.assertEqual(self.board._pawn_moves(Square('c3')), [[Square('c4')], [Square('d4')]])
        self.assertEqual(self.board._pawn_moves(Square('d3')), [])
        self.assertEqual(self.board._pawn_moves(Square('e4')), [[Square('e5')]])
        self.assertEqual(self.board._pawn_moves(Square('f5')), [[Square('f6')], [Square('e6')]])
        self.assertEqual(self.board._pawn_moves(Square('g5')), [])
        self.assertEqual(self.board._pawn_moves(Square('h2')), [[Square('h3'), Square('h4')]])
        self.assertEqual(self.board._pawn_moves(Square('c5')), [])

        # black pawns
        self.assertEqual(self.board._pawn_moves(Square('a7')), [])
        self.assertEqual(self.board._pawn_moves(Square('b7')), [[Square('b6')], [Square('a6')]])
        self.assertEqual(self.board._pawn_moves(Square('c6')), [[Square('b5')]])
        self.assertEqual(self.board._pawn_moves(Square('d7')), [[Square('d6'), Square('d5')]])
        self.assertEqual(self.board._pawn_moves(Square('f7')), [[Square('f6')], [Square('g6')]])
        self.assertEqual(self.board._pawn_moves(Square('g7')), [])
        self.assertEqual(self.board._pawn_moves(Square('h7')), [[Square('h6'), Square('h5')], [Square('g6')]])

    def test_knight_moves(self):
        self.set_test_position_1()
        # white knights
        self.assertEqual(self.board._knight_moves(Square('a6')), [[Square('b8')], [Square('b4')], [Square('c7')]])
        self.assertEqual(self.board._knight_moves(Square('g6')), [[Square('f8')], [Square('h8')], [Square('f4')],
                                                                  [Square('h4')], [Square('e7')], [Square('e5')]])
        self.assertEqual(self.board._knight_moves(Square('f2')), [[Square('g4')], [Square('h3')], [Square('h1')]])
        # black knights
        self.assertEqual(self.board._knight_moves(Square('d8')), [])

    def test_bishop_moves(self):
        self.set_test_position_1()
        # white bishops
        self.assertEqual(self.board._bishop_moves(Square('b5')), [[Square('c6')], [Square('a4')], [Square('c4')]])
        # black bishops
        self.assertEqual(self.board._bishop_moves(Square('a5')), [[Square('b6'), Square('c7')],
                                                                  [Square('b4'), Square('c3')]])

    def test_rook_moves(self):
        self.set_test_position_1()
        # white rooks
        self.assertEqual(self.board._rook_moves(Square('b1')), [[Square('a1')], [Square('c1')]])
        self.assertEqual(self.board._rook_moves(Square('e1')), [[Square('e2'), Square('e3')], [Square('f1')]])
        # black rooks
        self.assertEqual(self.board._rook_moves(Square('a8')), [[Square('b8'), Square('c8')]])
        self.assertEqual(self.board._rook_moves(Square('f8')), [[Square('e8')]])

    def test_queen_moves(self):
        self.set_test_position_1()
        # white queen
        self.assertEqual(self.board._queen_moves(Square('d1')), [
            [Square('d2')], [Square('c1')], [Square('c2'), Square('b3'), Square('a4')],
            [Square('e2'), Square('f3'), Square('g4'), Square('h5')]])
        # black queen
        self.assertEqual(self.board._queen_moves(Square('e6')), [
            [Square('e7'), Square('e8')], [Square('e5'), Square('e4')], [Square('d6')], [Square('f6'), Square('g6')],
            [Square('d5'), Square('c4'), Square('b3'), Square('a2')], [Square('f5')]])

    def test_king_moves(self):
        self.set_test_position_1()
        # white king
        self.assertEqual(self.board._king_moves(Square('g1')), [[Square('g2')], [Square('h1')], [Square('f1')]])
        # black king
        self.assertEqual(self.board._king_moves(Square('g8')), [[Square('h8')]])

    def test_in_check(self):
        self.set_test_position_2()
        self.assertEqual(self.board.in_check(Color.BLACK), True)
        self.assertEqual(self.board.in_check(Color.WHITE), False)
