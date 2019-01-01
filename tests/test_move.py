from unittest import TestCase
from metaknight.board import Board
from metaknight.square import Square
from metaknight.move import Move, InvalidNotationError
from metaknight.piece import Color


class TestMove(TestCase):
    def setUp(self):
        self.board = Board()
        self.board.set_board_state([
            'R..N.R.K',
            'PP.P..P.',
            'n.P.QP..',
            'BbP..pp.',
            '...Bp...',
            '..ppN...',
            'pp...n.p',
            '.r.qr.kb',
        ])

        # Pawn moves
        self.pawn_move_1 = Move(self.board, 'a4', Color.WHITE)
        self.pawn_move_2 = Move(self.board, 'a3', Color.WHITE)
        self.pawn_move_3 = Move(self.board, 'cxd4', Color.WHITE)
        self.pawn_move_4 = Move(self.board, 'b6', Color.BLACK)

        # Knight moves
        self.knight_move_1 = Move(self.board, 'Nxc5', Color.WHITE)
        self.knight_move_2 = Move(self.board, 'Ng4', Color.WHITE)
        self.knight_move_3 = Move(self.board, 'Nf7', Color.BLACK)

        # Bishop moves
        self.bishop_move_1 = Move(self.board, 'Bf3', Color.WHITE)
        self.bishop_move_2 = Move(self.board, 'Bxc3', Color.BLACK)
        self.bishop_move_3 = Move(self.board, 'Be5', Color.BLACK)

        # Rook moves
        self.rook_move_1 = Move(self.board, 'Rc1', Color.WHITE)
        self.rook_move_2 = Move(self.board, 'Rf7', Color.BLACK)
        self.rook_move_3 = Move(self.board, 'Rxe3', Color.WHITE)

        # Queen moves
        self.queen_move_1 = Move(self.board, 'Qd2', Color.WHITE)
        self.queen_move_2 = Move(self.board, 'Qxe4', Color.BLACK)
        self.queen_move_3 = Move(self.board, 'Qh5', Color.WHITE)

        # King moves
        self.king_move_1 = Move(self.board, 'Kg2', Color.WHITE)
        self.king_move_2 = Move(self.board, 'Kh7', Color.BLACK)
        self.king_move_3 = Move(self.board, 'Kf1', Color.WHITE)

    def test_pawn_moves(self):
        self.assertEqual(self.pawn_move_1.origin, Square('a2'))
        self.assertEqual(self.pawn_move_2.origin, Square('a2'))
        self.assertEqual(self.pawn_move_3.origin, Square('c3'))
        self.assertEqual(self.pawn_move_4.origin, Square('b7'))

        self.assertEqual(self.pawn_move_1.destination, Square('a4'))
        self.assertEqual(self.pawn_move_2.destination, Square('a3'))
        self.assertEqual(self.pawn_move_3.destination, Square('d4'))
        self.assertEqual(self.pawn_move_4.destination, Square('b6'))

        """
        self.assertEqual(self.pawn_move_1.check, False)
        self.assertEqual(self.pawn_move_2.check, False)
        self.assertEqual(self.pawn_move_3.check, False)
        self.assertEqual(self.pawn_move_4.check, False)
        """

    def test_knight_moves(self):
        self.assertEqual(self.knight_move_1.origin, Square('a6'))
        self.assertEqual(self.knight_move_2.origin, Square('f2'))
        self.assertEqual(self.knight_move_3.origin, Square('d8'))
        self.assertRaises(InvalidNotationError, lambda: Move(self.board, 'Nf4', Color.WHITE))

        self.assertEqual(self.knight_move_1.destination, Square('c5'))
        self.assertEqual(self.knight_move_2.destination, Square('g4'))
        self.assertEqual(self.knight_move_3.destination, Square('f7'))

    def test_bishop_moves(self):
        self.assertEqual(self.bishop_move_1.origin, Square('h1'))
        self.assertEqual(self.bishop_move_2.origin, Square('d4'))
        self.assertEqual(self.bishop_move_3.origin, Square('d4'))
        self.assertRaises(InvalidNotationError, lambda: Move(self.board, 'Bb4', Color.WHITE))

        self.assertEqual(self.bishop_move_1.destination, Square('f3'))
        self.assertEqual(self.bishop_move_2.destination, Square('c3'))
        self.assertEqual(self.bishop_move_3.destination, Square('e5'))

    def test_rook_moves(self):
        self.assertEqual(self.rook_move_1.origin, Square('b1'))
        self.assertEqual(self.rook_move_2.origin, Square('f8'))
        self.assertEqual(self.rook_move_3.origin, Square('e1'))
        self.assertRaises(InvalidNotationError, lambda: Move(self.board, 'Rb3', Color.WHITE))

        self.assertEqual(self.rook_move_1.destination, Square('c1'))
        self.assertEqual(self.rook_move_2.destination, Square('f7'))
        self.assertEqual(self.rook_move_3.destination, Square('e3'))

    def test_queen_moves(self):
        self.assertEqual(self.queen_move_1.origin, Square('d1'))
        self.assertEqual(self.queen_move_2.origin, Square('e6'))
        self.assertEqual(self.queen_move_3.origin, Square('d1'))
        self.assertRaises(InvalidNotationError, lambda: Move(self.board, 'Qg4', Color.BLACK))

        self.assertEqual(self.queen_move_1.destination, Square('d2'))
        self.assertEqual(self.queen_move_2.destination, Square('e4'))
        self.assertEqual(self.queen_move_3.destination, Square('h5'))

    def test_king_moves(self):
        self.assertEqual(self.king_move_1.origin, Square('g1'))
        self.assertEqual(self.king_move_2.origin, Square('h8'))
        self.assertEqual(self.king_move_3.origin, Square('g1'))
        self.assertRaises(InvalidNotationError, lambda: Move(self.board, 'Kh6', Color.BLACK))

        self.assertEqual(self.king_move_1.destination, Square('g2'))
        self.assertEqual(self.king_move_2.destination, Square('h7'))
        self.assertEqual(self.king_move_3.destination, Square('f1'))
