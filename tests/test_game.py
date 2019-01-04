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

    def test_check_situations(self):
        self.game.play_move('d4')
        self.game.play_move('e5')
        self.game.play_move('h3')
        self.game.play_move('Bb4')
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('Qd3'))
        self.game.play_move('Nc3')
        self.game.play_move('Bxc3')
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('Kd2'))
        self.game.play_move('Bd2')
        self.game.play_move('Qh4')
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('f4'))
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('f3'))
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('Be3'))
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('Bc1'))

    def test_king_side_castle(self):
        self.game.play_move('e4')
        self.game.play_move('e5')
        self.game.play_move('Bc4')
        self.game.play_move('Qh4')
        self.game.play_move('Bxf7')
        self.game.play_move('Kxf7')
        self.game.play_move('Qf3')
        self.game.play_move('Ke8')
        self.game.play_move('Ne2')
        self.game.play_move('Nc6')
        self.game.play_move('O-O')
        self.assertEqual(self.game.board.get_square('e1').piece, None)
        self.assertEqual(self.game.board.get_square('f1').piece, Piece(PieceType.ROOK, Color.WHITE))
        self.assertEqual(self.game.board.get_square('g1').piece, Piece(PieceType.KING, Color.WHITE))
        self.assertEqual(self.game.board.get_square('h1').piece, None)

        self.game.play_move('Bc5')
        self.game.play_move('Nc3')
        self.game.play_move('Nh6')
        self.game.play_move('d3')
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('O-O'))

    def test_queen_side_castle(self):
        self.game.play_move('d4')
        self.game.play_move('Nf6')
        self.game.play_move('c4')
        self.game.play_move('Nc6')
        self.game.play_move('Nc3')
        self.game.play_move('d6')
        self.game.play_move('Rb1')
        self.game.play_move('Bf5')
        self.game.play_move('Ra1')
        self.game.play_move('e5')
        self.game.play_move('Bg5')
        self.game.play_move('Qd7')
        self.game.play_move('Qa4')
        self.game.play_move('Ne4')
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('O-O-O'))
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('O-O'))

        self.game.play_move('h3')
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('O-O-O'))
        self.assertRaises(InvalidNotationError, lambda: self.game.play_move('O-O'))

        self.game.play_move('Nf6')
        self.game.play_move('e4')
        print(self.game.board)
        self.game.play_move('O-O-O')
        self.assertEqual(self.game.board.get_square('a8').piece, None)
        self.assertEqual(self.game.board.get_square('b8').piece, None)
        self.assertEqual(self.game.board.get_square('c8').piece, Piece(PieceType.KING, Color.BLACK))
        self.assertEqual(self.game.board.get_square('d8').piece, Piece(PieceType.ROOK, Color.BLACK))
        self.assertEqual(self.game.board.get_square('e8').piece, None)
