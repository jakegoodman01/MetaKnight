from metaknight.board import Board
from metaknight.move import Move
from metaknight.piece import Color, PieceType
from typing import List


class Game:
    def __init__(self):
        self.board: Board = Board()
        self.game_history: List[Move] = []
        self.to_move = Color.WHITE

        self.white_captured: List[PieceType] = []  # All captured white pieces
        self.black_captured: List[PieceType] = []  # All captured black pieces

    def play_move(self, notation):
        move = Move(self.board, notation, self.to_move)
        piece_moved = self.board.get_square(square=move.origin).piece
        self.board.get_square(square=move.origin).piece = None

        if self.board.get_square(square=move.destination).piece:
            # If there was a capture
            captured = self.board.get_square(square=move.destination).piece.piece_type
            if self.to_move is Color.WHITE:
                self.black_captured.append(captured)
            else:
                self.white_captured.append(captured)
        self.board.get_square(square=move.destination).piece = piece_moved

        self.to_move = self.to_move.switch()
        self.game_history.append(move)

