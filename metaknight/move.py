from metaknight.board import Board
from metaknight.square import Square
from metaknight.piece import Color, Piece, PieceType

from copy import deepcopy


class InvalidNotationError(Exception):
    pass


class Move:
    def __init__(self, board: Board, to_move: Color, origin: Square, destination: Square, en_passant: bool=False):
        """
        :param board: The board that this move is being played on
        :param to_move: The player that made this move: Color.WHITE or Color.BLACK
        :param origin: The square that the piece started on
        :param destination: The square that the piece moves to
        """

        self.board: Board = board
        self.to_move: Color = to_move
        self.origin: Square = board.get_square(square=origin)
        self.destination: Square = board.get_square(square=destination)
        self.piece_moved: Piece = self.origin.piece
        self.en_passant = en_passant

        if not self.origin.piece or self.origin.piece.color != self.to_move:
            raise InvalidNotationError

        if self.en_passant:
            func = Square.up if self.to_move is Color.BLACK else Square.down
            square = func(self.destination)
            self.piece_captured: Piece = self.board.get_square(square=square).piece
        else:
            if self.destination.piece and self.destination.piece.color == to_move:
                raise InvalidNotationError
            self.piece_captured: Piece = self.destination.piece  # None if no piece was captured
        self._not_in_check()

    def __repr__(self):
        if self.en_passant:
            return f'{self.origin} takes {self.destination} en passant'
        elif self.piece_captured:
            return f'{self.origin} takes {self.destination}'
        else:
            return f'{self.origin} -> {self.destination}'

    def execute_move(self):
        self.board.get_square(square=self.origin).piece = None
        self.board.get_square(square=self.destination).piece = self.piece_moved
        if self.en_passant:
            func = Square.up if self.to_move is Color.BLACK else Square.down
            square = func(self.destination)
            self.board.get_square(square=square).piece = None

        self.origin: Square = self.board.get_square(square=self.origin)
        self.destination: Square = self.board.get_square(square=self.destination)

    def _not_in_check(self):
        """
        This function simulates the new board state if the desired move is executed. If the new board state
        has a check in it, I throw an InvalidNotationError
        """

        board_copy = deepcopy(self.board)
        board_copy.get_square(square=self.origin).piece = None
        board_copy.get_square(square=self.destination).piece = self.piece_moved

        if board_copy.in_check(self.to_move):
            raise InvalidNotationError('This move puts you in check')


class Castle:
    def __init__(self, board: Board, to_move: Color,
                 king_side: bool=True, king_moved: bool=False, rook_moved: bool=False):
        if board.in_check(to_move) or king_moved or rook_moved:
            raise InvalidNotationError
        rank = '1' if to_move is Color.WHITE else '8'
        direction = Square.right if king_side else Square.left
        rook_file = 'h' if king_side else 'a'
        rook_dest = 'f' if king_side else 'd'

        origin = Square(f'e{rank}')

        self.king_side = king_side
        self.king_move1 = Move(board, to_move, origin, direction(origin))
        self.king_move2 = Move(board, to_move, origin, direction(direction(origin)))
        self.rook_move = Move(board, to_move, Square(f'{rook_file}{rank}'), Square(f'{rook_dest}{rank}'))
        self.origin = origin
        self.destination = direction(direction(origin))
        self.piece_moved: Piece = Piece(PieceType.KING, to_move)
        self.piece_captured: Piece = None

    def __repr__(self):
        return 'king-side castle' if self.king_side else 'queen-side castle'

    def execute_move(self):
        self.king_move1.execute_move()
        self.king_move2.execute_move()
        self.rook_move.execute_move()

