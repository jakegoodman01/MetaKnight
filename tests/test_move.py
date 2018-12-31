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
            '..pp....',
            'pp...n.p',
            '.r.qr.k.',
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

        # Rook moves

        # Queen moves

        # King moves

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
