from board.location import Location
from util.character_map import CharacterMap
from piece import King, Queen, Rook, Bishop, Knight, Pawn
from util.enums import Player, Side
import random


class Board:

    def __init__(self, new_game=True):
        self._pieces = []
        self._promoted_pawns = []
        self._removed_pieces = []
        self._moves = []
        self.character_map = CharacterMap()
        self.turn = Player.WHITE

        if new_game:
            self._create_royalty()
            self._create_nobles()
            self._create_pawns()

    def _create_pawns(self):
        for col in Location.COLS:
            Pawn(Location(7, col), Player.BLACK, self)
            Pawn(Location(2, col), Player.WHITE, self)

    def _create_nobles(self):
        for index, piece_class in enumerate([Rook, Knight, Bishop]):
            for col in [Location.COLS[index], Location.COLS[-(index+1)]]:
                piece_class(Location(8, col), Player.BLACK, self)
                piece_class(Location(1, col), Player.WHITE, self)

    def _create_royalty(self):
        King(Location(8, 'e'), Player.BLACK, self)
        Queen(Location(8, 'd'), Player.BLACK, self)
        King(Location(1, 'e'), Player.WHITE, self)
        Queen(Location(1, 'd'), Player.WHITE, self)

    def add(self, piece):
        self._pieces.append(piece)

    def remove(self, piece):
        self._removed_pieces.append(piece)
        self._pieces.remove(piece)

    def undo_add(self, piece):
        self._pieces.remove(piece)

    def undo_remove(self, piece):
        self._removed_pieces.remove(piece)
        self._pieces.append(piece)

    def promote_pawn(self, pawn):
        self._pieces.remove(pawn)
        self._promoted_pawns.append(pawn)

    def undo_promote_pawn(self, pawn, promoted_piece):
        self._pieces.remove(promoted_piece)
        self._promoted_pawns.remove(pawn)
        self._pieces.append(pawn)

    def move(self, move):
        if move.castle:
            move.piece.move(move.new_location)
            move.rook_piece.move(move.rook_new_location)
        elif move.en_passant:
            move.piece.move(move.new_location)
            self.remove(move.captured_piece)
        elif move.promotion:
            if move.captured_piece:
                self.remove(move.captured_piece)
            self.promote_pawn(move.piece)
            move.promotion_piece_class(move.new_location, move.piece.player, self)
        else:
            move.piece.move(move.new_location)
            if move.captured_piece:
                self.remove(move.captured_piece)

        self.turn = self.turn.opponent()
        self._moves.append(move)

    def undo_move(self):
        move = self._moves.pop()
        if move.castle:
            move.piece.move(move.old_location, undo=True)
            move.rook_piece.move(move.rook_old_location, undo=True)
        elif move.en_passant:
            move.piece.move(move.old_location, undo=True)
            self.undo_remove(move.captured_piece)
        elif move.promotion:
            p = self.piece(move.new_location, move.piece.player)
            if p is None:
                raise ValueError('failed to undo promotion move')
            self.undo_promote_pawn(move.piece, p)
            if move.captured_piece:
                self.undo_remove(move.captured_piece)
        else:
            move.piece.move(move.old_location, undo=True)
            if move.captured_piece:
                self.undo_remove(move.captured_piece)
        self.turn = self.turn.opponent()

    def random_move(self):
        moves = list(self.valid_moves())
        index = random.randint(0, len(moves)-1)
        self.move(moves[index])

    def valid_moves(self):
        for move in self.possible_moves(self.turn):
            if self.valid_move(move):
                yield move

    def valid_move(self, move):
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

        self.move(move)
        check = self.check(self.turn.opponent())
        self.undo_move()
        return not check

    def score(self, player):
        s = 0
        for p in self._removed_pieces:
            if p.player == player:
                s += p.VALUE
        return s

    def check(self, player, location=None):
        king = list(self.pieces(piece_class=King, player=player))[0]
        return king.checked(location)

    def draw(self):
        # no valid moves but not in check means a draw
        if len(list(self.valid_moves())) == 0 and not self.check(self.turn):
            return True
        return False

    def checkmate(self):
        if len(list(self.valid_moves())) == 0 and self.check(self.turn):
            return True
        return False

    def last_move(self):
        if len(self._moves) > 0:
            return self._moves[-1]
        return None

    def pieces(self, piece_class=None, player=None):
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
        for p in self._pieces:
            if p.location == location and (player is None or player == p.player):
                return p
        return None

    def empty(self, location, player=None):
        for p in self.pieces(player=player):
            if p.location == location:
                return False
        return True

    def attacked_locations(self, player):
        for p in self.pieces(player=player):
            yield from p.attacked_locations()

    def possible_moves(self, player):
        for p in self.pieces(player=player):
            yield from p.moves()

    def __str__(self):
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
        return character * ((len(Location.COLS) * 4) + 3)