import enum


class Player(enum.Enum):
    WHITE = 0
    BLACK = 1

    def __init__(self, val):
        self.val = val # boolean

    #@classmethod
    #def opponent(cls, player):
    #    return Player.WHITE if player == Player.BLACK else Player.BLACK

    def opponent(self):
        return Player.WHITE if self.val == Player.BLACK.value else Player.BLACK


class Color(enum.Enum):
    WHITE = 0
    BLACK = 1


class Side(enum.Enum):
    KING = 0
    QUEEN = 1