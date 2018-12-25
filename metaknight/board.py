class Square:
    def __init__(self, coordinates: str):
        self.file = coordinates[0]
        self.rank = coordinates[1]

    def __repr__(self):
        return f'{self.file}{self.rank}'

    def __eq__(self, other):
        return isinstance(other, Square) and other.file == self.file and other.rank == self.rank


class Board:
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self):
        self.squares = [[Square(file + rank) for file in Board.files] for rank in Board.ranks]
