from metaknight.board import Board
from metaknight.square import Square
from metaknight.piece import Color, Piece, PieceType

from copy import deepcopy


class InvalidNotationError(Exception):
    pass


class Move:
    def __init__(self, board: Board, to_move: Color, origin: Square, destination: Square):
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
        self.piece_captured: Piece = self.destination.piece  # None if no piece was captured

    def execute_move(self):
        self._not_in_check()
        self.board.get_square(square=self.origin).piece = None
        self.board.get_square(square=self.destination).piece = self.piece_moved

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

"""
class Move:
    def __init__(self, board: Board, notation: str, to_move: Color, en_passant_file: str=None,
                 king_moved: bool=False, h_rook_moved: bool=False, a_rook_moved: bool=False):
        self.origin: Square = None  # the square at which the piece began
        self.destination: Square = None  # the square at which the piece was moved to
        rank = '1' if to_move is Color.WHITE else '8'
        if notation == 'O-O':
            self.castle(board, to_move, king_moved, h_rook_moved, True)
            self.piece_moved: Piece = self.origin.piece
            self._not_in_check(board, to_move)

            # moving the rook
            board.get_square(location=f'h{rank}').piece = None
            board.get_square(location=f'f{rank}').piece = Piece(PieceType.ROOK, to_move)
        elif notation == 'O-O-O':
            self.castle(board, to_move, king_moved, a_rook_moved, False)
            self.piece_moved: Piece = self.origin.piece
            self._not_in_check(board, to_move)

            # moving the rook
            board.get_square(location=f'a{rank}').piece = None
            board.get_square(location=f'd{rank}').piece = Piece(PieceType.ROOK, to_move)
        else:
            self._set_destination(board, notation, to_move, en_passant_file)
            self._set_origin(board, notation, to_move)
            self.piece_moved: Piece = self.origin.piece
            self._not_in_check(board, to_move)

    def _set_destination(self, board: Board, notation: str, to_move: Color, en_passant_legal: str):
        if 'x' in notation and board.get_square(location=notation[-2:]).piece is None:
            # A piece made a capture on a square that has no piece!
            # This is an invalid notation, unless en passant happened here
            if len(notation) == 4 and 97 <= ord(notation[0]) <= 104:
                # A pawn made the capture
                if notation[3] == '6' and to_move == Color.WHITE or notation[3] == '3' and to_move == Color.BLACK:
                    # The capture was made on the right rank for en passant
                    file = notation[2]
                    rank = int(notation[3]) + 1 if to_move == Color.BLACK else int(notation[3]) - 1
                    square = board.get_square(location=f'{file}{rank}')  # a pawn of opposite color should be here
                    if square.piece and square.piece.color != to_move:
                        # The board conditions for en passant were met
                        if en_passant_legal and en_passant_legal == square.file:
                            self.destination = board.get_square(location=notation[-2:])
                            board.get_square(square=square).piece = None
                            return
            raise InvalidNotationError()

        self.destination = board.get_square(location=notation[-2:])

    def _set_origin(self, board: Board, notation: str, to_move: Color):
        increment = -1 if to_move is Color.WHITE else 1
        piece_moved = None
        if len(notation) == 2:
            # A pawn simply advanced
            piece_moved = PieceType.PAWN
            file = notation[0]
            rank = int(notation[1])
            if (to_move is Color.WHITE and rank == 4) or (to_move is Color.BLACK and rank == 5):
                # The pawn could have come from the start row, special case
                if board.get_square(location=f'{file}{rank + increment}').piece is None:
                    # if the square that the pawn came from has no piece there
                    self.origin = board.get_square(location=f'{file}{rank + 2 * increment}')
            if self.origin is None:
                self.origin = board.get_square(location=f'{file}{rank + increment}')
        elif len(notation) == 4 and 97 <= ord(notation[0]) <= 104:
            # A pawn captured another piece
            piece_moved = PieceType.PAWN
            file = notation[0]
            rank = int(notation[3])
            self.origin = board.get_square(location=f'{file}{rank + increment}')
        elif len(notation) == 4 or len(notation) == 3:
            # A piece was moved, or there was a capture
            piece_moved = PieceType.KNIGHT
            if notation[0] == 'B':
                piece_moved = PieceType.BISHOP
            elif notation[0] == 'R':
                piece_moved = PieceType.ROOK
            elif notation[0] == 'Q':
                piece_moved = PieceType.QUEEN
            elif notation[0] == 'K':
                piece_moved = PieceType.KING

            for rank in board.squares:
                for square in rank:
                    if square.piece == Piece(piece_moved, to_move):
                        moves = board.get_moves(square=square)
                        for direction in moves:
                            for move in direction:
                                if move == self.destination:
                                    self.origin = square
                                    return

        if not self.origin or not self.origin.piece or self.origin.piece != Piece(piece_moved, to_move):
            raise InvalidNotationError()

    def _not_in_check(self, board: Board, to_move: Color):
        \"""
        This function simulates the new board state if the desired move is executed. If the new board state
        has a check in it, I throw an InvalidNotationError
        :param board: The board state of the current move
        :param to_move: The color to move
        :return: None
        \"""

        board_copy = deepcopy(board)
        board_copy.get_square(square=self.origin).piece = None
        board_copy.get_square(square=self.destination).piece = self.piece_moved

        if board_copy.in_check(to_move):
            raise InvalidNotationError('This move puts you in check')

    def castle(self, board: Board, to_move: Color, king_moved: bool, rook_moved: bool, king_side: bool):
        \"""
        This function sets the origin and destination for a king-side castle move
        Raises InvalidNotationError is the king is in check, castles through check, or ends up in check
        :param board: The board state of the current move
        :param to_move: The color to move
        :param king_moved: True if the king has moved already
        :param rook_moved: True of the rook on involved in the castle has already moved
        :param king_side: True if this is a king side castle, False if queen side castle
        :return: None
        \"""

        if king_moved or rook_moved:
            # The right to castling is lost
            raise InvalidNotationError('The king or rook have already moved')

        rank = '1' if to_move is Color.WHITE else '8'
        file = 'h' if king_side else 'a'
        if board.get_square(f'e{rank}').piece != Piece(PieceType.KING, to_move) or \
                board.get_square(f'{file}{rank}').piece != Piece(PieceType.ROOK, to_move):
            # This statement verifies that there is indeed a king and a rook on the proper squares to execute a castle
            raise InvalidNotationError('There are not pieces in the right location')

        if board.in_check(to_move):
            raise InvalidNotationError('Cannot castle out of check')

        if king_side:
            Move(board, f'Kf{rank}', to_move)
            self.destination = board.get_square(location=f'g{rank}')
        else:
            Move(board, f'Kd{rank}', to_move)
            self.destination = board.get_square(location=f'c{rank}')
        # if the line above did not throw an exception, then the king would not castle through check
        self.origin = board.get_square(location=f'e{rank}')
"""
