from enum import Enum


class PieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5


class Color(Enum):
    WHITE = 0
    BLACK = 1

    def switch(self):
        if self.value == 0:
            return Color.BLACK
        return Color.WHITE


class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.piece_type = piece_type
        self.color = color

    def __repr__(self):
        if self.color is Color.WHITE:
            if self.piece_type is PieceType.PAWN:
                return '\u2659'
            if self.piece_type is PieceType.KNIGHT:
                return '\u2658'
            if self.piece_type is PieceType.BISHOP:
                return '\u2657'
            if self.piece_type is PieceType.ROOK:
                return '\u2656'
            if self.piece_type is PieceType.QUEEN:
                return '\u2655'
            if self.piece_type is PieceType.KING:
                return '\u2654'
        elif self.color is Color.BLACK:
            if self.piece_type is PieceType.PAWN:
                return '\u265f'
            if self.piece_type is PieceType.KNIGHT:
                return '\u265e'
            if self.piece_type is PieceType.BISHOP:
                return '\u265d'
            if self.piece_type is PieceType.ROOK:
                return '\u265c'
            if self.piece_type is PieceType.QUEEN:
                return '\u265b'
            if self.piece_type is PieceType.KING:
                return '\u265a'

    def __eq__(self, other):
        return isinstance(other, Piece) and \
               other.piece_type == self.piece_type and \
               other.color == self.color
