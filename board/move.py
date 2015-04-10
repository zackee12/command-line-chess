from util.enums import Side


class Move:
    def __init__(self, piece, location, captured_piece=None):
        self.piece = piece
        self.old_location = piece.location
        self.new_location = location
        self.captured_piece = captured_piece

        # castling
        self.castle = False
        self.rook_piece = None
        self.rook_old_location = None
        self.rook_new_location = None
        self.castle_side = None

        # en passant
        self.en_passant = False

        # promotion
        self.promotion = False
        self.promotion_piece_class = None

    def __str__(self):
        if self.castle:
            if self.castle_side == Side.KING:
                return 'O-O'
            elif self.castle_side == Side.QUEEN:
                return 'O-O-O'
            raise ValueError('move castling side is invalid: {}'.format(self.castle_side))

        piece = self.piece.board.character_map.algebraic_notation(self.piece.player, self.piece.__class__)
        separator = '-' if self.captured_piece is None else 'x'

        # TODO include check/checkmate (+ and #)
        return '{}{}{}{}'.format(piece, self.old_location, separator, self.new_location)

    def __repr__(self):
        return "Move({}, {}, {})".format(repr(self.piece), repr(self.piece.location), repr(self.new_location))

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            o = vars(other)
            for k, v in vars(self).items():
                if k not in o or o[k] != v:
                    return False
            return True
        return NotImplemented

    @classmethod
    def create_castle(cls, king, king_location, rook, rook_location):
        move = cls(king, king_location)
        move.castle = True
        move.rook_piece = rook
        move.rook_old_location = rook.location
        move.rook_new_location = rook_location
        if king_location.col > king.location.col:
            move.castle_side = Side.KING
        else:
            move.castle_side = Side.QUEEN
        return move

    @classmethod
    def create_en_passant(cls, pawn_piece, pawn_new_location, captured_pawn_piece):
        move = cls(pawn_piece, pawn_new_location, captured_pawn_piece)
        move.en_passant = True
        return move

    @classmethod
    def create_promotion(cls, pawn_piece, pawn_new_location, promoted_piece_class, captured_piece=None):
        move = cls(pawn_piece, pawn_new_location, captured_piece)
        move.promotion = True
        move.promotion_piece_class = promoted_piece_class
        return move

