from unittest import TestCase
from metaknight.board import Board
from metaknight.square import Square
from metaknight.move import Move


class TestMove(TestCase):
    def setUp(self):
        self.board = Board()
        self.board.set_board_state([
            'R..N.R.K',
            'PP.P.PP.',
            'n.P.Q.n.',
            'Bbp..pp.',
            '...Bp...',
            '..pp....',
            'pp...n.p',
            '.r.qr.k.',
        ])

        # Pawn moves
        self.pawn_move_1 = Move(self.board, 'a4')
        self.pawn_move_2 = Move(self.board, 'a3')
        self.pawn_move_3 = Move(self.board, 'cxd4')

    def test_notation_parser(self):
        # Pawn moves
        self.assertEqual(self.pawn_move_1.origin, Square('a2'))
        self.assertEqual(self.pawn_move_2.origin, Square('a2'))
        self.assertEqual(self.pawn_move_3.origin, Square('c3'))

        self.assertEqual(self.pawn_move_1.destination, Square('a4'))
        self.assertEqual(self.pawn_move_2.destination, Square('a3'))
        self.assertEqual(self.pawn_move_3.destination, Square('d4'))

        self.assertEqual(self.pawn_move_1.check, False)
        self.assertEqual(self.pawn_move_2.check, False)
        self.assertEqual(self.pawn_move_3.check, False)