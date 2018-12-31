from metaknight.board import Board
from metaknight.square import Square
from metaknight.piece import Color, Piece, PieceType


class InvalidNotationError(Exception):
    pass


class Move:
    def __init__(self, board: Board, notation: str, to_move: Color):
        self.origin: Square = None  # the square at which the piece began
        self.destination: Square = None  # the square at which the piece was moved to
        self.check: bool = False  # True if the move results in a check

        self._set_destination(board, notation, to_move)
        self._set_origin(board, notation, to_move)

    def _set_destination(self, board: Board, notation: str, to_move: Color):
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
            # A pawn was moved
            piece_moved = PieceType.PAWN
            file = notation[0]
            rank = int(notation[3])
            self.origin = board.get_square(location=f'{file}{rank + increment}')
        elif len(notation) == 4 or len(notation) == 3:
            # A piece was moved, or there was a capture
            move_func = board.knight_moves
            piece_moved = PieceType.KNIGHT
            if notation[0] == 'B':
                move_func = board.bishop_moves
                piece_moved = PieceType.BISHOP
            elif notation[0] == 'R':
                move_func = board.rook_moves
                piece_moved = PieceType.ROOK
            elif notation[0] == 'Q':
                move_func = board.queen_moves
                piece_moved = PieceType.QUEEN
            elif notation[0] == 'K':
                move_func = board.king_moves
                piece_moved = PieceType.KING

            for rank in board.squares:
                for square in rank:
                    if square.piece == Piece(piece_moved, to_move):
                        moves = move_func(square)
                        for direction in moves:
                            for move in direction:
                                if move == self.destination:
                                    self.origin = square
                                    return

        if not self.origin or not self.origin.piece or self.origin.piece != Piece(piece_moved, to_move):
            raise InvalidNotationError()
