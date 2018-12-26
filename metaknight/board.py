class OutOfBoundsError(Exception):
    """ Raised when a square is referenced that sits outside of the standard 8x8 chess board"""


class Square:
    def __init__(self, coordinates: str):
        self.file = coordinates[0]
        self.rank = coordinates[1]

    def __repr__(self):
        return f'{self.file}{self.rank}'

    def __eq__(self, other):
        return isinstance(other, Square) and other.file == self.file and other.rank == self.rank

    def up(self):
        if self.rank == '8':
            raise OutOfBoundsError()
        next_rank = Board.ranks[Board.ranks.index(self.rank) + 1]
        return Square(self.file + next_rank)


class Board:
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self):
        self.squares = [[Square(file + rank) for file in Board.files] for rank in Board.ranks]
