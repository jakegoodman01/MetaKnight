class Square:
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self, coordinates: str):
        # A Square will have coordinates '00' if it out of bounds (does not exist in the chess board
        self.file = coordinates[0]
        self.rank = coordinates[1]
        self.piece = None

    def __repr__(self):
        return f'{self.file}{self.rank}'

    def __eq__(self, other):
        return isinstance(other, Square) and other.file == self.file and other.rank == self.rank

    def up(self):
        if self.rank in ('8', '0'):
            return Square('00')
        next_rank = Square.ranks[Square.ranks.index(self.rank) + 1]
        return Square(self.file + next_rank)

    def down(self):
        if self.rank in ('1', '0'):
            return Square('00')
        next_rank = Square.ranks[Square.ranks.index(self.rank) - 1]
        return Square(self.file + next_rank)

    def left(self):
        if self.file in ('a', '0'):
            return Square('00')
        next_file = Square.files[Square.files.index(self.file) - 1]
        return Square(next_file + self.rank)

    def right(self):
        if self.file in ('h', '0'):
            return Square('00')
        next_file = Square.files[Square.files.index(self.file) + 1]
        return Square(next_file + self.rank)
