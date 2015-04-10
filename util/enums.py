import enum


class Player(enum.Enum):
    WHITE = 0
    BLACK = 1

    def opponent(self):
        return Player.WHITE if self.value == Player.BLACK.value else Player.BLACK


class Color(enum.Enum):
    WHITE = 0
    BLACK = 1


class Side(enum.Enum):
    KING = 0
    QUEEN = 1