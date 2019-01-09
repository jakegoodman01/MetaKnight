from metaknight.board import Board
from metaknight.square import Square
from metaknight.move import Move, InvalidNotationError, Castle
from metaknight.piece import Piece, Color, PieceType
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
        move = self.notation_parser(notation)
        move.execute_move()

        if move.piece_moved.piece_type == PieceType.KING:
            self.king_moved[self.to_move.value] = True
        elif move.piece_moved.piece_type == PieceType.ROOK:
            if move.origin.file == 'a':
                self.a_rook_moved[self.to_move.value] = True
            elif move.origin.file == 'h':
                self.h_rook_moved[self.to_move.value] = True

        captured = move.piece_captured
        if self.to_move is Color.WHITE and captured:
            self.black_captured.append(captured.piece_type)
        elif captured:
            self.white_captured.append(captured.piece_type)

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

    def notation_parser(self, notation: str) -> Move or Castle:
        if notation == 'O-O':
            rook = self.h_rook_moved[self.to_move.value]
            king = self.king_moved[self.to_move.value]
            return Castle(self.board, self.to_move, king_side=True, king_moved=king, rook_moved=rook)
        elif notation == 'O-O-O':
            rook = self.a_rook_moved[self.to_move.value]
            king = self.king_moved[self.to_move.value]
            return Castle(self.board, self.to_move, king_side=False, king_moved=king, rook_moved=rook)

        destination, en_passant = self._find_destination(notation)
        origin = self._find_origin(notation, destination)
        return Move(self.board, self.to_move, origin, destination, en_passant)

    def _find_destination(self, notation: str) -> (Square, bool):
        if 'x' in notation and self.board.get_square(location=notation[-2:]).piece is None:
            # A piece made a capture on a square that has no piece!
            # This is an invalid notation, unless en passant happened here
            if len(notation) == 4 and 97 <= ord(notation[0]) <= 104:
                # A pawn made the capture
                if notation[3] == '6' and self.to_move == Color.WHITE or \
                        notation[3] == '3' and self.to_move == Color.BLACK:
                    # The capture was made on the correct rank for en passant
                    file = notation[2]
                    rank = int(notation[3]) + 1 if self.to_move == Color.BLACK else int(notation[3]) - 1
                    square = self.board.get_square(location=f'{file}{rank}')  # a pawn of opposite color should be here
                    if square.piece and square.piece.color != self.to_move:
                        # The board conditions for en passant were met
                        en_passant_file = self.en_passant_file()
                        if en_passant_file and en_passant_file == square.file:
                            return self.board.get_square(location=notation[-2:]), True
            raise InvalidNotationError()

        return self.board.get_square(location=notation[-2:]), False

    def _find_origin(self, notation: str, destination) -> Square:
        increment = -1 if self.to_move is Color.WHITE else 1
        if len(notation) == 2:
            # A pawn simply advanced
            file = notation[0]
            rank = int(notation[1])
            if (self.to_move is Color.WHITE and rank == 4) or (self.to_move is Color.BLACK and rank == 5):
                # The pawn could have come from the start row, special case
                if self.board.get_square(location=f'{file}{rank + increment}').piece is None:
                    # if the square that the pawn came from has no piece there
                    return self.board.get_square(location=f'{file}{rank + 2 * increment}')
            return self.board.get_square(location=f'{file}{rank + increment}')
        elif len(notation) == 4 and 97 <= ord(notation[0]) <= 104:
            # A pawn captured another piece
            file = notation[0]
            rank = int(notation[3])
            return self.board.get_square(location=f'{file}{rank + increment}')
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

            if len(notation) == 4 and notation[1] != 'x':
                if notation[2].isdigit():
                    rank = int(notation) - 1
                    for square in self.board.squares[rank]:
                        if square.piece == Piece(piece_moved, self.to_move):
                            moves = self.board.get_moves(square=square)
                            for direction in moves:
                                for move in direction:
                                    if move == destination:
                                        return square
                else:
                    for rank in self.board.squares:
                        file = Square.files.index(notation[1])
                        square = rank[file]
                        if square.piece == Piece(piece_moved, self.to_move):
                            moves = self.board.get_moves(square=square)
                            for direction in moves:
                                for move in direction:
                                    if move == destination:
                                        return square

            else:
                for rank in self.board.squares:
                    for square in rank:
                        if square.piece == Piece(piece_moved, self.to_move):
                            moves = self.board.get_moves(square=square)
                            for direction in moves:
                                for move in direction:
                                    if move == destination:
                                        return square
        raise InvalidNotationError()
