from util.enums import Side


class Move:
    """
    Data structure to hold needed information relating to a chess move
    """
    def __init__(self, piece, location, captured_piece=None):
        """ initializer

        :param piece: Piece class
        :param location: Location class
        :param captured_piece: Piece class
        :return:
        """
        # standard moves
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
        """ Long algebraic notation"""
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
            # compare all dict keys
            o = vars(other)
            for k, v in vars(self).items():
                if k not in o or o[k] != v:
                    return False
            return True
        return NotImplemented

    @classmethod
    def create_castle(cls, king, king_location, rook, rook_location):
        """ Creates a castle move
        :param king: King class
        :param king_location: Location class for new location of king
        :param rook: Rook class
        :param rook_location: Location class for new location of rook
        :return: Move
        """
        move = cls(king, king_location)
        move.castle = True
        move.rook_piece = rook
        move.rook_old_location = rook.location
        move.rook_new_location = rook_location

        # determine if king side or queen side castle
        if king_location.col > king.location.col:
            move.castle_side = Side.KING
        else:
            move.castle_side = Side.QUEEN
        return move

    @classmethod
    def create_en_passant(cls, pawn_piece, pawn_new_location, captured_pawn_piece):
        """ Create an en passant pawn move

        :param pawn_piece: Pawn
        :param pawn_new_location: Location class for new location of pawn
        :param captured_pawn_piece: Pawn
        :return: Move
        """
        move = cls(pawn_piece, pawn_new_location, captured_pawn_piece)
        move.en_passant = True
        return move

    @classmethod
    def create_promotion(cls, pawn_piece, pawn_new_location, promoted_piece_class, captured_piece=None):
        """ Create a pawn promotion move

        :param pawn_piece: Pawn
        :param pawn_new_location: Location class for new location of pawn
        :param promoted_piece_class: class of the desired piece to promote pawn to
        :param captured_piece: Piece class for any piece that is captured during move
        :return: Move
        """
        move = cls(pawn_piece, pawn_new_location, captured_piece)
        move.promotion = True
        move.promotion_piece_class = promoted_piece_class
        return move

