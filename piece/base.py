from util.enums import Player, Side
from board.move import Move


class Piece:
    VALUE = 0

    def __init__(self, location, player, board):
        self.player = player
        self.location = location
        self._initial_position = location
        self._board = board
        self._total_moves = 0

        if not self.board.empty(location):
            raise ValueError('board already contains a piece at {}'.format(location))

        self._board.add(self)

    @property
    def moved(self):
        return self._total_moves > 0

    @property
    def board(self):
        return self._board

    def move(self, location, undo=False):
        self.location = location
        self._total_moves += (-1 if undo else 1)

    def attacked_locations(self):
        raise NotImplementedError

    def moves(self):
        for loc in self.attacked_locations():
            yield Move(self, loc, self.board.piece(loc, self.player.opponent()))

    def __repr__(self):
        return '{}({}, {}, {}())'\
            .format(self.__class__.__name__, repr(self.player), repr(self.location), self.board.__class__.__name__)

    def __str__(self):
        return self.board.character_map(self.player, self.__class__)


class SingleMovePiece(Piece):
    """ Makes 1 move based on the MOVE_VECTORS unless off the board"""
    MOVE_VECTORS = []

    def attacked_locations(self):
        for row, col in self.MOVE_VECTORS:
            loc = self.location.offset(row, col)
            if loc is not None:
                # location is empty
                if self.board.empty(loc):
                    yield loc
                # location is empty of the same player (aka opposing player is there)
                elif self.board.empty(loc, player=self.player):
                    yield loc


class MultipleMovePiece(Piece):
    """ Makes moves from the MOVE_VECTORS until off the board or blocked"""
    MOVE_VECTORS = []

    def attacked_locations(self):
        # try each tuple in the move vectors
        for row, col in self.MOVE_VECTORS:
            loc = self.location
            # continue until blocked or off the board
            while True:
                loc = loc.offset(row, col)
                if loc is not None:
                    # location is empty
                    if self.board.empty(loc):
                        yield loc
                    # location is empty of the same player (aka opposing player is there)
                    elif self.board.empty(loc, player=self.player):
                        yield loc
                        break
                    # location contains a teammate
                    else:
                        break
                # location if off of the board
                else:
                    break