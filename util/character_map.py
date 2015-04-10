import sys
from piece import King, Queen, Rook, Bishop, Knight, Pawn
from util.enums import Player, Color


class CharacterMap:
    """
    Map for various representations of the chess pieces
    """
    CHARACTERS = {
        (Player.WHITE, King): ('\u2654', 'k', 'K'),  # (unicode, ascii, algebraic)
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
        """ Check if unicode characters can be printed to stdout

        :return: boolean
        """
        for c, _, _ in cls.CHARACTERS.values():
            try:
                c.encode(sys.stdout.encoding)
            except UnicodeEncodeError:
                return False
        return True

    def unicode_character(self, player_or_color, piece_type=None):
        """ Return the unicode character representation of a piece or tile

        :param player_or_color: Player enum or Color enum
        :param piece_type: Class of piece (e.g. Pawn) or None if looking for tile character
        :return: str
        """
        return self.CHARACTERS[(player_or_color, piece_type)][0]

    def character(self, player_or_color, piece_type=None):
        """ Return the ascii character representation of a piece or tile

        :param player_or_color: Player enum or Color enum
        :param piece_type: Class of piece (e.g. Pawn) or None if looking for tile character
        :return: str
        """
        return self.CHARACTERS[(player_or_color, piece_type)][1]

    def algebraic_notation(self, player, piece_type):
        """ Return the algebraic notation for a piece

        :param player: Player enum
        :param piece_type: Class of piece (e.g. Pawn)
        :return: str
        """
        return self.CHARACTERS[(player, piece_type)][2]

    def __call__(self, player_or_color, piece_type=None):
        """ Return the unicode/ascii character representation of a piece or tile depending on what is printable

        :param player_or_color: Player enum or Color enum
        :param piece_type: Class of piece (e.g. Pawn) or None if looking for tile character
        :return: str
        """
        # return unicode if available to print
        if self.unicode:
            return self.unicode_character(player_or_color, piece_type)
        return self.character(player_or_color, piece_type)
