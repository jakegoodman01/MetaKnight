from metaknight.piece import PieceType, Piece, Color
from typing import List


class OutOfBoundsError(Exception):
    """ Raised when a square is referenced that sits outside of the standard 8x8 chess board"""
    pass


class Square:
    def __init__(self, coordinates: str):
        self.file = coordinates[0]
        self.rank = coordinates[1]
        self.piece = None

    def __repr__(self):
        return f'{self.file}{self.rank}'

    def __eq__(self, other):
        return isinstance(other, Square) and other.file == self.file and other.rank == self.rank

    def up(self):
        if self.rank == '8':
            raise OutOfBoundsError()
        next_rank = Board.ranks[Board.ranks.index(self.rank) + 1]
        return Square(self.file + next_rank)

    def down(self):
        if self.rank == '1':
            raise OutOfBoundsError()
        next_rank = Board.ranks[Board.ranks.index(self.rank) - 1]
        return Square(self.file + next_rank)

    def left(self):
        if self.file == 'a':
            raise OutOfBoundsError()
        next_file = Board.files[Board.files.index(self.file) - 1]
        return Square(next_file + self.rank)

    def right(self):
        if self.file == 'h':
            raise OutOfBoundsError()
        next_file = Board.files[Board.files.index(self.file) + 1]
        return Square(next_file + self.rank)


class Board:
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self):
        self.squares = [[Square(file + rank) for file in Board.files] for rank in Board.ranks]
        self.set_up()

    def __repr__(self):
        output = ''
        for rank in range(7, -1, -1):
            for file in range(0, 8):
                piece = self.squares[rank][file].piece
                if piece:
                    output += f'{repr(piece)} '
                else:
                    output += '. '
            output += '\n'
        return output[:-1]  # This removes the last \n character

    def clear(self):
        """ This method will only be used for debugging purposes
        """
        self.squares = [[Square(file + rank) for file in Board.files] for rank in Board.ranks]

    def set_up(self):
        # Pawns
        for i in range(8):
            self.squares[1][i].piece = Piece(PieceType.PAWN, Color.WHITE)
            self.squares[6][i].piece = Piece(PieceType.PAWN, Color.BLACK)

        # Rooks
        for i in (0, 7):
            self.squares[0][i].piece = Piece(PieceType.ROOK, Color.WHITE)
            self.squares[7][i].piece = Piece(PieceType.ROOK, Color.BLACK)

        # Knights
        for i in (1, 6):
            self.squares[0][i].piece = Piece(PieceType.KNIGHT, Color.WHITE)
            self.squares[7][i].piece = Piece(PieceType.KNIGHT, Color.BLACK)

        # Bishops
        for i in (2, 5):
            self.squares[0][i].piece = Piece(PieceType.BISHOP, Color.WHITE)
            self.squares[7][i].piece = Piece(PieceType.BISHOP, Color.BLACK)

        # Kings and queens
        self.squares[0][3].piece = Piece(PieceType.QUEEN, Color.WHITE)
        self.squares[0][4].piece = Piece(PieceType.KING, Color.WHITE)
        self.squares[7][3].piece = Piece(PieceType.QUEEN, Color.BLACK)
        self.squares[7][4].piece = Piece(PieceType.KING, Color.BLACK)

    def get_square_at_location(self, location: str) -> Square:
        """
        :param location: string coordinates of a square. For example: 'a3' or 'c8'
        :return: the square at location in this board
        """
        file = Board.files.index(location[0])
        rank = Board.ranks.index(location[1])
        return self.squares[rank][file]

    def pawn_moves(self, square: Square) -> List[List[Square]]:
        # TODO: Account for en passant
        moves = []
        square = self.get_square_at_location(repr(square))
        if square.piece.color is Color.WHITE:
            forward_square = self.get_square_at_location(repr(square.up()))
            if forward_square.piece is None:
                moves.append([forward_square])
                forward_square = self.get_square_at_location(repr(forward_square.up()))
                if square.rank == '2' and forward_square.piece is None:
                    moves[0].append(forward_square)
            if square.file != 'a':
                diagonal = self.get_square_at_location(repr(square.up()))
                diagonal = self.get_square_at_location(repr(diagonal.left()))
                if diagonal.piece and diagonal.piece.color is Color.BLACK:
                    moves.append([diagonal])
            if square.file != 'h':
                diagonal = self.get_square_at_location(repr(square.up()))
                diagonal = self.get_square_at_location(repr(diagonal.right()))
                if diagonal.piece and diagonal.piece.color is Color.BLACK:
                    moves.append([diagonal])
        else:
            forward_square = self.get_square_at_location(repr(square.down()))
            if forward_square.piece is None:
                moves.append([forward_square])
                forward_square = self.get_square_at_location(repr(forward_square.down()))
                if square.rank == '7' and forward_square.piece is None:
                    moves[0].append(forward_square)
            if square.file != 'a':
                diagonal = self.get_square_at_location(repr(square.down()))
                diagonal = self.get_square_at_location(repr(diagonal.left()))
                if diagonal.piece and diagonal.piece.color is Color.WHITE:
                    moves.append([diagonal])
            if square.file != 'h':
                diagonal = self.get_square_at_location(repr(square.down()))
                diagonal = self.get_square_at_location(repr(diagonal.right()))
                if diagonal.piece and diagonal.piece.color is Color.WHITE:
                    moves.append([diagonal])
        return moves

    def knight_moves(self, square: Square) -> List[List[Square]]:
        # TODO: Make this less horrible :)
        original = self.get_square_at_location(repr(square))
        color = original.piece.color
        moves = []

        # upper left
        try:
            square = self.get_square_at_location(repr(original.up()))
            square = self.get_square_at_location(repr(square.up()))
            square = self.get_square_at_location(repr(square.left()))
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # upper right
        try:
            square = self.get_square_at_location(repr(original.up()))
            square = self.get_square_at_location(repr(square.up()))
            square = self.get_square_at_location(repr(square.right()))
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # lower left
        try:
            square = self.get_square_at_location(repr(original.down()))
            square = self.get_square_at_location(repr(square.down()))
            square = self.get_square_at_location(repr(square.left()))
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # lower right
        try:
            square = self.get_square_at_location(repr(original.down()))
            square = self.get_square_at_location(repr(square.down()))
            square = self.get_square_at_location(repr(square.right()))
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # left upper
        try:
            square = self.get_square_at_location(repr(original.left()))
            square = self.get_square_at_location(repr(square.left()))
            square = self.get_square_at_location(repr(square.up()))
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # left lower
        try:
            square = self.get_square_at_location(repr(original.left()))
            square = self.get_square_at_location(repr(square.left()))
            square = self.get_square_at_location(repr(square.down()))
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # right upper
        try:
            square = self.get_square_at_location(repr(original.right()))
            square = self.get_square_at_location(repr(square.right()))
            square = self.get_square_at_location(repr(square.up()))
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # right lower
        try:
            square = self.get_square_at_location(repr(original.right()))
            square = self.get_square_at_location(repr(square.right()))
            square = self.get_square_at_location(repr(square.down()))
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        return moves
