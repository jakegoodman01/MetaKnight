from unittest import TestCase
from metaknight.game import Game
from metaknight.move import InvalidNotationError
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

    def test_en_passant(self):
        self.game.play_move('e4')
        self.game.play_move('f5')
        self.game.play_move('exf5')
        self.game.play_move('g5')
        self.game.play_move('fxg6')
        self.game.play_move('hxg6')
        self.game.play_move('h4')
        self.game.play_move('g5')
        self.game.play_move('a3')
        self.game.play_move('g4')
        self.game.play_move('f4')
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('gxh3'))
        self.game.play_move('gxf3')

