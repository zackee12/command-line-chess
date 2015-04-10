import sys
from piece import King, Queen, Rook, Bishop, Knight, Pawn
from util.enums import Player, Color


class CharacterMap:
    CHARACTERS = {
        (Player.WHITE, King): ('\u2654', 'k', 'K'),
        (Player.WHITE, Queen): ('\u2655', 'q', 'Q'),
        (Player.WHITE, Rook): ('\u2656', 'r', 'R'),
        (Player.WHITE, Bishop): ('\u2657', 'b', 'B'),
        (Player.WHITE, Knight): ('\u2658', 'n', 'N'),
        (Player.WHITE, Pawn): ('\u2659', 'p', ''),
        (Player.BLACK, King): ('\u265A', 'K', 'K'),
        (Player.BLACK, Queen): ('\u265B', 'Q', 'Q'),
        (Player.BLACK, Rook): ('\u265C', 'R', 'R'),
        (Player.BLACK, Bishop): ('\u265D', 'B', 'B'),
        (Player.BLACK, Knight): ('\u265E', 'N', 'N'),
        (Player.BLACK, Pawn): ('\u265F', 'P', ''),
        (Color.WHITE, None): ('\u2610', ' ', ' '),
        (Color.BLACK, None): ('\u2610', ' ', ' '),
    }

    def __init__(self):
        self.unicode = self._unicode()

    @classmethod
    def _unicode(cls):
        for c, _, _ in cls.CHARACTERS.values():
            try:
                c.encode(sys.stdout.encoding)
            except UnicodeEncodeError:
                return False
        return True

    def character(self, player_or_color, piece_type=None):
        return self.CHARACTERS[(player_or_color, piece_type)][1]

    def unicode_character(self, player_or_color, piece_type=None):
        return self.CHARACTERS[(player_or_color, piece_type)][0]

    def algebraic_notation(self, player, piece_type):
        return self.CHARACTERS[(player, piece_type)][2]

    def __call__(self, player_or_color, piece_type=None):
        if self.unicode:
            return self.unicode_character(player_or_color, piece_type)
        return self.character(player_or_color, piece_type)
