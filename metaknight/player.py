from random import randint
from metaknight.game import *


class WorstPlayer:
    def __init__(self, game: Game):
        self.game = game

    def make_move(self) -> Move:
        moves = self.game.generate_moves()
        index = randint(0, len(moves) - 1)
        return moves[index]
