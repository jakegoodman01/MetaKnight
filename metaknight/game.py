from metaknight.board import Board
from metaknight.move import Move
from metaknight.piece import Color, PieceType
from typing import List


class Game:
    def __init__(self):
        self.board: Board = Board()
        self.game_history: List[Move] = []
        self.to_move: Color = Color.WHITE

        # For the following variables, the 0th index represents white, and the 1st index represents black
        self.a_rook_moved = [False, False]
        self.h_rook_moved = [False, False]
        self.king_moved = [False, False]

        self.white_captured: List[PieceType] = []  # All captured white pieces
        self.black_captured: List[PieceType] = []  # All captured black pieces

    def play_move(self, notation):
        move = Move(self.board, notation, self.to_move, en_passant_file=self.en_passant_file(),
                    king_moved=self.king_moved[self.to_move.value],
                    h_rook_moved=self.h_rook_moved[self.to_move.value],
                    a_rook_moved=self.a_rook_moved[self.to_move.value])

        if move.piece_moved.piece_type == PieceType.KING:
            self.king_moved[self.to_move.value] = True
        elif move.piece_moved.piece_type == PieceType.ROOK:
            if move.origin.file == 'a':
                self.a_rook_moved[self.to_move.value] = True
            elif move.origin.file == 'h':
                self.h_rook_moved[self.to_move.value] = True

        self.board.get_square(square=move.origin).piece = None
        if self.board.get_square(square=move.destination).piece:
            # If there was a capture
            captured = self.board.get_square(square=move.destination).piece.piece_type
            if self.to_move is Color.WHITE:
                self.black_captured.append(captured)
            else:
                self.white_captured.append(captured)
        self.board.get_square(square=move.destination).piece = move.piece_moved

        self.to_move = self.to_move.switch()
        self.game_history.append(move)

    def en_passant_file(self) -> str:
        """
        :return: The file of a pawn that advanced forward two squares, legalizing en passant. None if no pawn did this
        """
        if len(self.game_history) > 1:
            last_move = self.game_history[-1]
            piece_moved = last_move.piece_moved.piece_type
            origin_rank = int(last_move.origin.rank)
            destination_rank = int(last_move.destination.rank)
            increment = 2 if self.to_move is Color.BLACK else -2

            if piece_moved is PieceType.PAWN and origin_rank + increment == destination_rank:
                return last_move.origin.file



