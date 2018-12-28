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

    def set_board_state(self, board_state: List[str]):
        """
        Sets self.squares to the format given by board_state
        :param board_state: the pieces on each square
        """
        self.clear()
        for i in range(0, 8):
            for j in range(0, 8):
                piece = board_state[i][j]
                if piece == '.':
                    piece = None
                elif piece == 'p':
                    piece = Piece(PieceType.PAWN, Color.WHITE)
                elif piece == 'n':
                    piece = Piece(PieceType.KNIGHT, Color.WHITE)
                elif piece == 'b':
                    piece = Piece(PieceType.BISHOP, Color.WHITE)
                elif piece == 'r':
                    piece = Piece(PieceType.ROOK, Color.WHITE)
                elif piece == 'q':
                    piece = Piece(PieceType.QUEEN, Color.WHITE)
                elif piece == 'k':
                    piece = Piece(PieceType.KING, Color.WHITE)
                elif piece == 'P':
                    piece = Piece(PieceType.PAWN, Color.BLACK)
                elif piece == 'N':
                    piece = Piece(PieceType.KNIGHT, Color.BLACK)
                elif piece == 'B':
                    piece = Piece(PieceType.BISHOP, Color.BLACK)
                elif piece == 'R':
                    piece = Piece(PieceType.ROOK, Color.BLACK)
                elif piece == 'Q':
                    piece = Piece(PieceType.QUEEN, Color.BLACK)
                elif piece == 'K':
                    piece = Piece(PieceType.KING, Color.BLACK)
                self.squares[7-i][j].piece = piece

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

    def get_square_at_location(self, location=None, square=None) -> Square:
        """
        :param location: string coordinates of a square. For example: 'a3' or 'c8'
        :param square: a square object that is not located in this board
        :return: the square at location in this board
        """
        if location:
            file = Board.files.index(location[0])
            rank = Board.ranks.index(location[1])
        elif square:
            file = Board.files.index(square.file)
            rank = Board.ranks.index(square.rank)
        else:
            raise ValueError('Must enter either a string location, or a Square object')
        return self.squares[rank][file]

    def pawn_moves(self, square: Square) -> List[List[Square]]:
        # TODO: Account for en passant
        moves = []
        square = self.get_square_at_location(square=square)
        color = square.piece.color
        forward = Square.up
        rank = '2'
        if square.piece.color is Color.BLACK:
            forward = Square.down
            rank = '7'

        forward_square = self.get_square_at_location(square=forward(square))
        if forward_square.piece is None:
            moves.append([forward_square])
            forward_square = self.get_square_at_location(square=forward(forward_square))
            if square.rank == rank and forward_square.piece is None:
                moves[0].append(forward_square)
        if square.file != 'a':
            diagonal = self.get_square_at_location(square=forward(square).left())
            if diagonal.piece and diagonal.piece.color is not color:
                moves.append([diagonal])
        if square.file != 'h':
            diagonal = self.get_square_at_location(square=forward(square).right())
            if diagonal.piece and diagonal.piece.color is not color:
                moves.append([diagonal])
        return moves

    def knight_moves(self, square: Square) -> List[List[Square]]:
        # TODO: Make this less horrible :)
        original = self.get_square_at_location(square=square)
        color = original.piece.color
        moves = []

        # upper left
        try:
            square = self.get_square_at_location(square=original.up().up().left())
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # upper right
        try:
            square = self.get_square_at_location(square=original.up().up().right())
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # lower left
        try:
            square = self.get_square_at_location(square=original.down().down().left())
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # lower right
        try:
            square = self.get_square_at_location(square=original.down().down().right())
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # left upper
        try:
            square = self.get_square_at_location(square=original.left().left().up())
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # left lower
        try:
            square = self.get_square_at_location(square=original.left().left().down())
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # right upper
        try:
            square = self.get_square_at_location(square=original.right().right().up())
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        # right lower
        try:
            square = self.get_square_at_location(square=original.right().right().down())
            if not square.piece or square.piece.color is not color:
                moves.append([square])
        except OutOfBoundsError:
            pass
        return moves

    def bishop_moves(self, square: Square) -> List[List[Square]]:
        # TODO: Make this less horrible :)
        moves = []
        original = self.get_square_at_location(square=square)
        color = original.piece.color
        diagonal = []
        try:
            # upper left diagonal
            square = original
            while True:
                square = self.get_square_at_location(square=square.up())
                square = self.get_square_at_location(square=square.left())
                if not square.piece:
                    diagonal.append(square)
                elif square.piece.color is not color:
                    diagonal.append(square)
                    raise OutOfBoundsError
                else:
                    raise OutOfBoundsError
        except OutOfBoundsError:
            moves.append(diagonal.copy())
        diagonal = []
        try:
            # upper right diagonal
            square = original
            while True:
                square = self.get_square_at_location(square=square.up())
                square = self.get_square_at_location(square=square.right())
                if not square.piece:
                    diagonal.append(square)
                elif square.piece.color is not color:
                    diagonal.append(square)
                    raise OutOfBoundsError
                else:
                    raise OutOfBoundsError
        except OutOfBoundsError:
            moves.append(diagonal.copy())
        diagonal = []
        try:
            # lower left diagonal
            square = original
            while True:
                square = self.get_square_at_location(square=square.down())
                square = self.get_square_at_location(square=square.left())
                if not square.piece:
                    diagonal.append(square)
                elif square.piece.color is not color:
                    diagonal.append(square)
                    raise OutOfBoundsError
                else:
                    raise OutOfBoundsError
        except OutOfBoundsError:
            moves.append(diagonal.copy())
        diagonal = []
        try:
            # lower right diagonal
            square = original
            while True:
                square = self.get_square_at_location(square=square.down())
                square = self.get_square_at_location(square=square.right())
                if not square.piece:
                    diagonal.append(square)
                elif square.piece.color is not color:
                    diagonal.append(square)
                    raise OutOfBoundsError
                else:
                    raise OutOfBoundsError
        except OutOfBoundsError:
            moves.append(diagonal.copy())
        return moves

