from board.location import Location
from util.character_map import CharacterMap
from piece import King, Queen, Rook, Bishop, Knight, Pawn
from util.enums import Player, Side
import random


class Board:
    """
    Chess board class containing chess pieces and methods to make valid moves during game play
    """
    def __init__(self, new_game=True):
        """ initializer

        :param new_game: initialize a new game with pieces
        :return:
        """
        self._pieces_by_location = {l: None for l in Location.all()}
        self._pieces = []
        self._promoted_pawns = []  # pawns that are removed due to being promoted
        self._captured_pieces = []
        self._moves = []  # history of moves
        self.character_map = CharacterMap()  # piece character map
        self.turn = Player.WHITE  # current player's turn

        if new_game:
            self._create_royalty()
            self._create_nobles()
            self._create_pawns()

    def _create_pawns(self):
        """ Create all of the pawn pieces in their starting positions

        :return: None
        """
        for col in Location.COLS:
            Pawn(Location(7, col), Player.BLACK, self)
            Pawn(Location(2, col), Player.WHITE, self)

    def _create_nobles(self):
        """ Create all of the rooks, bishops, and knights in their starting positions

        :return: None
        """
        for index, piece_class in enumerate([Rook, Knight, Bishop]):
            for col in [Location.COLS[index], Location.COLS[-(index+1)]]:
                piece_class(Location(8, col), Player.BLACK, self)
                piece_class(Location(1, col), Player.WHITE, self)

    def _create_royalty(self):
        """ Create all of the kings and queens in their starting positions

        :return: None
        """
        King(Location(8, 'e'), Player.BLACK, self)
        Queen(Location(8, 'd'), Player.BLACK, self)
        King(Location(1, 'e'), Player.WHITE, self)
        Queen(Location(1, 'd'), Player.WHITE, self)

    def add_piece(self, piece):
        if not self.empty(piece.location):
            raise ValueError('board already contains a piece at {}'.format(piece.location))
        self._pieces.append(piece)
        self._pieces_by_location[piece.location] = piece

    def undo_add_piece(self, piece):
        p = self.piece(piece.location)
        if p != piece:
            raise ValueError('this piece is not at the location')
        self._pieces.remove(piece)
        self._pieces_by_location[piece.location] = None

    def remove_piece(self, piece):
        self._pieces_by_location[piece.location] = None

    def undo_remove_piece(self, piece):
        self._pieces_by_location[piece.location] = piece

    def capture_piece(self, piece):
        self.remove_piece(piece)
        self._pieces.remove(piece)
        self._captured_pieces.append(piece)

    def undo_capture_piece(self, piece):
        self.undo_remove_piece(piece)
        self._pieces.append(piece)
        self._captured_pieces.remove(piece)

    def move_piece(self, piece, new_location):
        if not self.empty(new_location):
            raise ValueError('piece is already present at {}'.format(new_location))
        # remove the piece from the old location
        self.remove_piece(piece)
        # add the piece to the new location
        self._pieces_by_location[new_location] = piece

    def promote_pawn(self, pawn, promoted_piece_class):
        """ Promote a pawn from the board

        :param pawn: Pawn class
        :return: None
        """
        # remove the pawn
        self.remove_piece(pawn)
        # store the pawn in promoted pieces
        self._promoted_pawns.append(pawn)
        # create the new piece
        promoted_piece_class(pawn.location, pawn.player, self)

    def undo_promote_pawn(self, pawn, promoted_piece):
        """ Undo the pawn promotion and creation of a new piece

        :param pawn: Pawn class
        :return: None
        :return:
        """
        # remove the promoted piece
        self.remove_piece(promoted_piece)
        # undo remove the pawn
        self.undo_remove_piece(pawn)
        # remove the pawn from promoted storage
        self._promoted_pawns.remove(pawn)

    def move(self, move):
        """ Make a move on the board and update the current player to the next player.  Validation of the move
        should be performed before calling this method.

        :param move: Move class
        :return: None
        """
        if move.castle:
            # move the king and the rook
            move.piece.move(move.new_location)
            move.rook_piece.move(move.rook_new_location)
        elif move.en_passant:
            # capture the pawn
            self.capture_piece(move.captured_piece)
            # move pawn to new location
            move.piece.move(move.new_location)
        elif move.promotion:
            # capture piece
            if move.captured_piece:
                self.capture_piece(move.captured_piece)
            # move the pawn
            move.piece.move(move.new_location)
            # promote pawn to new type
            self.promote_pawn(move.piece, move.promotion_piece_class)
        else:
            # standard moves
            if move.captured_piece:
                self.capture_piece(move.captured_piece)
            move.piece.move(move.new_location)

        self.turn = self.turn.opponent()
        self._moves.append(move)

    def undo_move(self):
        """ Undo the previous move on the board and update the current player to the previous player

        :return: None
        """
        move = self._moves.pop()
        if move.castle:
            # revert the king and rook moves
            move.piece.move(move.old_location, undo=True)
            move.rook_piece.move(move.rook_old_location, undo=True)
        elif move.en_passant:
            # undo the capture
            self.undo_capture_piece(move.captured_piece)
            # move pawn back to original location
            move.piece.move(move.old_location, undo=True)
        elif move.promotion:
            # get the piece at the location of the promoted piece
            p = self.piece(move.new_location, move.piece.player)

            # remove the promoted piece and restore the pawn
            self.undo_promote_pawn(move.piece, p)

            # move the pawn back to the original location
            move.piece.move(move.old_location, undo=True)

            # restore captured pieces
            if move.captured_piece:
                self.undo_capture_piece(move.captured_piece)
        else:
            # undo standard moves
            move.piece.move(move.old_location, undo=True)
            if move.captured_piece:
                self.undo_capture_piece(move.captured_piece)
        self.turn = self.turn.opponent()

    def random_move(self):
        """ Get a random move from the current player's valid moves

        :return: Move
        """
        moves = list(self.valid_moves())
        index = random.randint(0, len(moves)-1)
        self.move(moves[index])

    def valid_moves(self):
        """ Get all valid moves for the current player

        :return: Move generator
        """
        for move in self.possible_moves(self.turn):
            if self.valid_move(move):
                yield move

    def valid_move(self, move):
        """ Check if a move is valid (aka player does not end the turn in check)

        :param move: Move
        :return: boolean
        """
        # castle moves can't move king through an attacked area
        if move.castle:
            if move.castle_side == Side.KING:
                if self.check(self.turn, move.new_location.offset(0, -1)):
                    return False
            elif move.castle_side == Side.QUEEN:
                if self.check(self.turn, move.new_location.offset(0, 1)):
                    return False
            else:
                raise ValueError('uh oh!!! not sure what happened')
        # make the move and see if the player is in check
        self.move(move)
        check = self.check(self.turn.opponent())
        self.undo_move()
        return not check

    def score(self, player=None):
        """ Get the score for a given player (defaults to the current player)

        :param player: Player Enum
        :return: score as integer
        """
        player = self.turn if player is None else player
        s = 0
        for p in self._captured_pieces:
            if p.player != player:
                s += p.VALUE
        return s

    def check(self, player, location=None):
        """ Check if a given player is in check

        :param player: Player Enum
        :param location: Location Class (defaults to current location of king)
        :return: boolean
        """
        king = list(self.pieces(piece_class=King, player=player))[0]
        return king.checked(location)

    def status(self):
        check = self.check(self.turn)
        valid_moves = len(list(self.valid_moves()))
        draw = valid_moves == 0 and not check
        checkmate = valid_moves == 0 and check
        return check, draw, checkmate

    def draw(self):
        """ Check if the game is a draw (current player has no valid moves but is not in check)

        :return: boolean
        """
        if len(list(self.valid_moves())) == 0 and not self.check(self.turn):
            return True
        return False

    def checkmate(self):
        """ Check if the game is in checkmate (current player has no valid moves and is in check)

        :return: boolean
        """
        if len(list(self.valid_moves())) == 0 and self.check(self.turn):
            return True
        return False

    def last_move(self):
        """ Get the last move if exists else returns None

        :return: Move or None
        """
        if len(self._moves) > 0:
            return self._moves[-1]
        return None

    def pieces(self, piece_class=None, player=None):
        """ Search and return pieces that match the filters

        :param piece_class: class of piece to return (defaults to all classes)
        :param player: Player Enum (defaults to both players)
        :return: Piece generator
        """
        for p in self._pieces:
            if piece_class is not None and player is not None:
                if isinstance(p, piece_class) and p.player == player:
                    yield p
            elif piece_class is not None:
                if isinstance(p, piece_class):
                    yield p
            elif player is not None:
                if p.player == player:
                    yield p
            else:
                yield p

    def piece(self, location, player=None):
        """ Get the piece at a given location and player if it exists

        :param location: Location class
        :param player: Player enum (defaults to both players)
        :return: Piece or None
        """
        p = self._pieces_by_location[location]
        if p is None or player is None or p.player == player:
            return p
        return None

    def empty(self, location, player=None):
        """ Check if a given location is empty with an optional player filter

        :param location: Location class
        :param player: Player enum
        :return: boolean
        """
        return self.piece(location, player) is None

    def attacked_locations(self, player):
        """ Get all locations that are under attack by a given player

        :param player: Player enum
        :return: Location generator
        """
        for p in self.pieces(player=player):
            yield from p.attacked_locations()

    def possible_moves(self, player):
        """ Get all possible moves for a given player (these are not validated)

        :param player:
        :return:
        """
        for p in self.pieces(player=player):
            yield from p.moves()

    def __str__(self):
        """ Print the chessboard """
        s = self._horizontal_border('-') + '\n'
        for row in sorted(Location.ROWS, reverse=True):
            s += '{} |'.format(row)
            for col in Location.COLS:
                l = Location(row, col)
                piece = self.piece(l)
                if not piece:
                    piece = self.character_map(l.color)
                s += ' {} |'.format(piece)
            s += '\n{}\n'.format(self._horizontal_border('-'))
        s += '  '
        for col in Location.COLS:
            s += '| {} '.format(col)
        s += '|\n'

        return s

    @staticmethod
    def _horizontal_border(character):
        """ Get a border using the input character for the chessboard

        :param character: str
        :return: str
        """
        return character * ((len(Location.COLS) * 4) + 3)