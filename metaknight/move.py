from metaknight.board import Board
from metaknight.square import Square
from metaknight.piece import Color


class Move:
    def __init__(self, board: Board, notation: str, to_move: Color):
        self.origin: Square = None  # the square at which the piece began
        self.destination: Square = None  # the square at which the piece was moved to
        self.check: bool = False  # True if the move results in a check

        self._find_origin(board, notation, to_move)

    def _find_origin(self, board: Board, notation: str, to_move: Color):
        increment = -1 if to_move is Color.WHITE else 1
        if len(notation) == 2:
            # A pawn simply advanced
            file = notation[0]
            rank = int(notation[1])
            if (to_move is Color.WHITE and rank == 4) or (to_move is Color.BLACK and rank == 5):
                # The pawn could have come from the start row, special case
                if board.get_square(location=f'{file}{rank + increment}').piece is None:
                    # if the square that the pawn came from has no piece there
                    self.origin = board.get_square(location=f'{file}{rank + 2 * increment}')
            if self.origin is None:
                self.origin = board.get_square(location=f'{file}{rank + increment}')
        elif len(notation) == 3:
            pass
        elif len(notation) == 4:
            # A piece captured another piece
            if 97 <= ord(notation[0]) <= 104:
                # A pawn was moved
                file = notation[0]
                rank = int(notation[3])
                self.origin = board.get_square(location=f'{file}{rank + increment}')
            else:
                # A piece was moved
                pass



