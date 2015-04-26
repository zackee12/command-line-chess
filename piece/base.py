from board.move import Move


class Piece:
    """
    Base class for all chess pieces
    """
    VALUE = 0  # value to be used for calculating score

    def __init__(self, location, player, board):
        """ initializer

        :param location: Location of piece
        :param player: Player that owns piece
        :param board: Board object that piece is placed on
        :return:
        """
        self.player = player
        self.location = location
        self._initial_position = location
        self.board = board
        self._total_moves = 0

        # add self to the board
        self.board.add_piece(self)

    @property
    def moved(self):
        """ Check if the piece has moved

        :return:
        """
        return self._total_moves > 0

    def move(self, location, undo=False):
        """ Move the piece to the given location and update the total moves

        :param location: new location for pawn
        :param undo: boolean that indicates if total moves should be increased or descreased
        :return:
        """
        self.board.move_piece(self, location)
        self._total_moves += (-1 if undo else 1)

    def attacked_locations(self):
        """ Get all locations under attack by this piece

        Sub classes should implement
        :return: Location generator
        """
        raise NotImplementedError

    def moves(self):
        """ Get all possible moves by this piece (unvalidated moves)

        :return: Move generator
        """
        for loc in self.attacked_locations():
            yield Move(self, loc, self.board.piece(loc, self.player.opponent()))

    def __repr__(self):
        return '{}({}, {}, {}())'\
            .format(self.__class__.__name__, repr(self.player), repr(self.location), self.board.__class__.__name__)

    def __str__(self):
        """ Get string representation of piece using the character map"""
        return self.board.character_map(self.player, self.__class__)


class SingleMovePiece(Piece):
    """
    Base class for chess pieces that make moves based on a single move offset (e.g. king)
    """
    MOVE_VECTORS = []  # offsets that piece can move from current location

    def attacked_locations(self):
        """ Get all locations under attack by this piece

        :return: Location generator
        """
        for row, col in self.MOVE_VECTORS:
            loc = self.location.offset(row, col)
            if loc is not None:
                p = self.board.piece(loc)
                # location is empty or has enemy player
                if p is None or p.player != self.player:
                    yield loc


class MultipleMovePiece(Piece):
    """
    Base class for chess pieces that make moves based on multiple move offset (continuous) (e.g. Queen)
    """
    MOVE_VECTORS = []  # offsets that piece can move from current location

    def attacked_locations(self):
        """ Get all locations under attack by this piece

        :return: Location generator
        """
        # try each tuple in the move vectors
        for row, col in self.MOVE_VECTORS:
            loc = self.location
            # continue until blocked or off the board
            while True:
                loc = loc.offset(row, col)
                if loc is not None:
                    p = self.board.piece(loc)
                    # location is empty
                    if p is None:
                        yield loc
                    # location is has an enemy player
                    elif p.player != self.player:
                        yield loc
                        break
                    # location contains a teammate
                    else:
                        break
                # location if off of the board
                else:
                    break