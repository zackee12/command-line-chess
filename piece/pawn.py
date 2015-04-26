from piece.base import Piece
from piece.bishop import Bishop
from piece.knight import Knight
from piece.queen import Queen
from piece.rook import Rook
from util.enums import Player
from board.move import Move


class Pawn(Piece):
    VALUE = 1

    @property
    def en_passant_vulnerable(self):
        """ Check if a pawn is vulnerable to an en passant attack

        :return: boolean
        """
        last_move = self.board.last_move()
        # if the last move was this piece and it moved by two spaces then it is vulnerable
        return (last_move is not None and
                self == last_move.piece and
                abs(last_move.old_location.row - last_move.new_location.row) == 2)

    def attacked_locations(self):
        """ Get all locations under attack by this piece

        :return: Location generator
        """
        for col in [-1, 1]:
            loc = self.location.offset(self.direction, col)
            # pawn can only attack when opponent is diagonal
            if loc is not None and not self.board.empty(loc, player=self.player.opponent()):
                yield loc

    def moves(self):
        """ Get all possible moves by this piece (unvalidated moves)

        :return: Move generator
        """
        # check attacking moves for promotions
        for move in super().moves():
            if move.new_location.end_of_row:
                for t in [Queen, Rook, Bishop, Knight]:
                    yield Move.create_promotion(self, move.new_location, t, move.captured_piece)
            else:
                yield move

        up1 = self.location.offset(self.direction, 0)

        # if space ahead is empty then can move
        if up1 and self.board.empty(up1):
            # check move for promotions
            if up1.end_of_row:
                for t in [Queen, Rook, Bishop, Knight]:
                    yield Move.create_promotion(self, up1, t)
            else:
                # regular move
                yield Move(self, up1)

            # if on the first move the two spaces ahead is empty then can move
            up2 = up1.offset(self.direction, 0)
            if not self.moved and self.board.empty(up2):
                yield Move(self, up2)

        # en passant
        for col in [-1, 1]:
            loc = self.location.offset(0, col)
            if loc is not None:
                p = self.board.piece(loc, self.player.opponent())
                if isinstance(p, Pawn) and p.en_passant_vulnerable:
                    yield Move.create_en_passant(self, loc.offset(self.direction, 0), p)

    @property
    def direction(self):
        """ Get the direction that a pawn moves

        :return: -1 or 1
        """
        return -1 if self.player == Player.BLACK else 1