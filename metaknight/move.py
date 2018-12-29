from metaknight.board import Board
from metaknight.square import Square
from metaknight.piece import Piece, PieceType, Color


class Move:
    def __init__(self, board: Board, notation: str):
        self.origin: Square = None  # the square at which the piece began
        self.destination: Square = None  # the square at which the piece was moved to
        self.piece_moved: Piece = None  # the piece that was moved
        self.piece_captured: Piece = None  # the piece that was captured, if any. None if no piece was captured
        self.check: bool = False  # True if the move results in a check

        


