from enum import Enum


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    KING = 999


class Color(Enum):
    WHITE = 0
    BLACK = 1
    

class Piece:
    pass
