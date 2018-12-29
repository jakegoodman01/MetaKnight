from metaknight.piece import PieceType, Piece, Color
from metaknight.square import Square
from typing import List


class Board:
    def __init__(self):
        self.squares = [[Square(file + rank) for file in Square.files] for rank in Square.ranks]
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
        self.squares = [[Square(file + rank) for file in Square.files] for rank in Square.ranks]

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

    def get_square(self, location=None, square=None) -> Square:
        """
        :param location: string coordinates of a square. For example: 'a3' or 'c8'
        :param square: a square object that is not located in this board
        :return: the square at location in this board
        """
        if location == '00' or square == Square('00'):
            return Square('00')

        if location:
            file = Square.files.index(location[0])
            rank = Square.ranks.index(location[1])
        elif square:
            file = Square.files.index(square.file)
            rank = Square.ranks.index(square.rank)
        else:
            raise ValueError('Must enter either a string location, or a Square object')
        return self.squares[rank][file]

    def pawn_moves(self, square: Square) -> List[List[Square]]:
        # TODO: Account for en passant
        moves = []
        square = self.get_square(square=square)
        color = square.piece.color
        forward = Square.up
        rank = '2'
        if square.piece.color is Color.BLACK:
            forward = Square.down
            rank = '7'

        forward_square = self.get_square(square=forward(square))
        if forward_square.piece is None:
            moves.append([forward_square])
            forward_square = self.get_square(square=forward(forward_square))
            if square.rank == rank and forward_square.piece is None:
                moves[0].append(forward_square)
        if square.file != 'a':
            diagonal = self.get_square(square=forward(square).left())
            if diagonal.piece and diagonal.piece.color is not color:
                moves.append([diagonal])
        if square.file != 'h':
            diagonal = self.get_square(square=forward(square).right())
            if diagonal.piece and diagonal.piece.color is not color:
                moves.append([diagonal])
        return moves

    def knight_moves(self, square: Square) -> List[List[Square]]:
        original = self.get_square(square=square)
        color = original.piece.color
        moves = [
            self.get_square(square=original.up().up().left()),
            self.get_square(square=original.up().up().right()),
            self.get_square(square=original.down().down().left()),
            self.get_square(square=original.down().down().right()),
            self.get_square(square=original.left().left().up()),
            self.get_square(square=original.left().left().down()),
            self.get_square(square=original.right().right().up()),
            self.get_square(square=original.right().right().down())
        ]
        possible_moves = []
        for move in moves:
            if move != Square('00') and (not move.piece or move.piece.color is not color):
                possible_moves.append([move])
        return possible_moves

    def bishop_moves(self, square: Square) -> List[List[Square]]:
        moves = []
        original = self.get_square(square=square)
        color = original.piece.color
        for func1 in (Square.up, Square.down):
            for func2 in (Square.left, Square.right):
                diagonal = []
                square = original
                while True:
                    square = self.get_square(square=func2(func1(square)))
                    if square == Square('00'):
                        break
                    if not square.piece and square != Square('00'):
                        diagonal.append(square)
                    elif square.piece.color is not color:
                        diagonal.append(square)
                        break
                    else:
                        break
                if len(diagonal) >= 1:
                    moves.append(diagonal.copy())
        return moves

    def rook_moves(self, square: Square) -> List[List[Square]]:
        moves = []
        original = self.get_square(square=square)
        color = original.piece.color
        for func in (Square.up, Square.down, Square.left, Square.right):
            line = []
            square = original
            while True:
                square = self.get_square(square=func(square))
                if square == Square('00'):
                    break
                if not square.piece and square != Square('00'):
                    line.append(square)
                elif square.piece.color is not color:
                    line.append(square)
                    break
                else:
                    break
            if len(line) >= 1:
                moves.append(line.copy())
        return moves

    def queen_moves(self, square: Square) -> List[List[Square]]:
        return self.rook_moves(square) + self.bishop_moves(square)

    def king_moves(self, square: Square) -> List[List[Square]]:
        original = self.get_square(square=square)
        color = original.piece.color
        moves = [
            self.get_square(square=original.up().left()),
            self.get_square(square=original.up()),
            self.get_square(square=original.up().right()),
            self.get_square(square=original.right()),
            self.get_square(square=original.right().down()),
            self.get_square(square=original.down()),
            self.get_square(square=original.down().left()),
            self.get_square(square=original.left())
        ]
        possible_moves = []
        for move in moves:
            if move != Square('00') and (not move.piece or move.piece.color is not color):
                possible_moves.append([move])
        return possible_moves
