from unittest import TestCase
from metaknight.game import Game
from metaknight.piece import Piece, PieceType, Color


class TestGame(TestCase):
    def setUp(self):
        self.game = Game()

    def test_play_move(self):
        self.game.play_move('e4')
        self.assertEqual(self.game.board.get_square(location='e2').piece, None)
        self.assertEqual(self.game.board.get_square(location='e4').piece, Piece(PieceType.PAWN, Color.WHITE))
        self.assertEqual(self.game.to_move, Color.BLACK)

        self.game.play_move('Nc6')
        self.assertEqual(self.game.board.get_square(location='b8').piece, None)
        self.assertEqual(self.game.board.get_square(location='c6').piece, Piece(PieceType.KNIGHT, Color.BLACK))
        self.assertEqual(self.game.to_move, Color.WHITE)