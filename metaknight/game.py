from metaknight.board import Board
from metaknight.square import Square
from metaknight.move import Move, InvalidNotationError, Castle
from metaknight.piece import Piece, Color, PieceType
from typing import List

from copy import deepcopy


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

    def play_move(self, notation: str=None, m: Move=None):
        move = None
        if notation:
            move = self.notation_parser(notation)
        else:
            move = m
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

    def undo_move(self):
        self.game_history[-1].undo()
        del self.game_history[-1]
        self.to_move = self.to_move.switch()

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

        promotion: PieceType = PieceType.QUEEN
        if not notation[-1].isdigit():
            if notation[-1] == 'Q':
                promotion = PieceType.QUEEN
            elif notation[-1] == 'N':
                promotion = PieceType.KNIGHT
            elif notation[-1] == 'B':
                promotion = PieceType.BISHOP
            elif notation[-1] == 'R':
                promotion = PieceType.ROOK
            notation = notation[:-1]

        destination, en_passant = self._find_destination(notation)
        origin = self._find_origin(notation, destination)
        return Move(self.board, self.to_move, origin, destination, en_passant, promotion=promotion)

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

    def generate_moves(self, to_move: Color=None) -> List[Move or Castle]:
        """
        :return: List of all legal moves from the current board state
        """
        if not to_move:
            to_move = self.to_move
        moves: List[Move or Castle] = []
        for row in self.board.squares:
            for square in row:
                if square.piece and square.piece.color is to_move:
                    for i in self.board.get_moves(square=square):
                        for j in i:
                            try:
                                moves.append(Move(self.board, square.piece.color, square, j))
                            except InvalidNotationError:
                                pass
        try:
            moves.append(self.notation_parser("O-O"))
        except InvalidNotationError:
            pass

        try:
            moves.append(self.notation_parser("O-O-O"))
        except InvalidNotationError:
            pass

        file = self.en_passant_file()
        if file:
            rank = '5' if to_move is Color.WHITE else '4'
            capture = '6' if to_move is Color.WHITE else '3'
            if file != 'a':
                f = Square.files.index(file) - 1
                origin = self.board.get_square(location=f'{Square.files[f]}{rank}')
                destination = self.board.get_square(location=f'{file}{capture}')
                try:
                    m = Move(self.board, to_move, origin, destination, en_passant=True)
                    moves.append(m)
                except InvalidNotationError:
                    pass

            if file != 'h':
                f = Square.files.index(file) + 1
                origin = self.board.get_square(location=f'{Square.files[f]}{rank}')
                destination = self.board.get_square(location=f'{file}{capture}')
                try:
                    m = Move(self.board, to_move, origin, destination, en_passant=True)
                    moves.append(m)
                except InvalidNotationError:
                    pass
        return moves

    def copy(self):
        """
        This function returns a copy of this current game
        """

        return deepcopy(self)

    def possible_games(self, n: int) -> List[List[Move or Castle]]:
        """
        :param n: number of moves
        :return: List of lists of possible moves for the next n moves
        """
        games: List[List[Move or Castle]] = []
        if n == 0:
            return [[]]
        for move in self.generate_moves():
            new_game = self.copy()
            move.board = new_game.board
            new_game.play_move(m=move)
            for g in new_game.possible_games(n-1):
                li = [move] + g
                games.append(li)
        return games

    def is_stalemate(self):
        return len(self.generate_moves()) == 0 and self.board.in_check(self.to_move) is False

    def is_checkmate(self):
        return len(self.generate_moves()) == 0 and self.board.in_check(self.to_move) is True

    def is_draw_by_insufficient_material(self):
        return len(self.white_captured) == 15 and len(self.black_captured) == 15

