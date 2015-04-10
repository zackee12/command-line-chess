from piece.base import SingleMovePiece
from piece.rook import Rook
from board.location import Location
from util.enums import Player, Side
from board.move import Move


class King(SingleMovePiece):
    MOVE_VECTORS = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    def checked(self, location=None):
        location = self.location if location is None else location
        return location in self.board.attacked_locations(self.player.opponent())

    def can_castle(self, side):
        if not self.moved:
            rook = self._get_unmoved_rook(side)
            if rook is not None:
                # check that no pieces are between the rook and king
                for loc in Location.from_between(rook.location, self.location):
                    if not self.board.empty(loc):
                        return False
                return True
        return False

    def _get_unmoved_rook(self, side):
        if side == Side.KING:
            rook = self.board.piece(Location(self.location.row, Location.COLS[-1]), self.player)
        else:
            rook = self.board.piece(Location(self.location.row, Location.COLS[0]), self.player)
        if rook and isinstance(rook, Rook) and not rook.moved:
            return rook
        return None

    def moves(self):
        yield from super().moves()

        if self.can_castle(Side.KING):
            rook = self._get_unmoved_rook(Side.KING)
            yield Move.create_castle(self, self.location.offset(0, 2), rook, rook.location.offset(0, -2))
        if self.can_castle(Side.QUEEN):
            rook = self._get_unmoved_rook(Side.QUEEN)
            yield Move.create_castle(self, self.location.offset(0, -2), rook, rook.location.offset(0, 3))