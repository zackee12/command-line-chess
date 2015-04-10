from unittest import TestCase
from board import Board, Location
from piece import King, Queen, Rook, Bishop, Knight, Pawn
from util.enums import Player, Side


class TestBase(TestCase):
    def setUp(self):
        self.board = Board(False)


class TestKing(TestBase):
    def test_attacked_locations(self):
        king = King(Location(5, 'd'), Player.BLACK, self.board)
        results = {Location(4, 'c'), Location(4, 'e'), Location(6, 'c'), Location(6, 'e'), Location(4, 'd'),
                   Location(6, 'd'), Location(5, 'c'), Location(5, 'e')}
        self.assertEquals(set(king.attacked_locations()), results)

    def test_checked(self):
        king = King(Location(5, 'd'), Player.BLACK, self.board)
        self.assertFalse(king.checked())
        king2 = King(Location(4, 'e'), Player.WHITE, self.board)
        self.assertTrue(king.checked())
        self.assertTrue(king2.checked())

    def test_can_castle_both(self):
        king = King(Location(8, 'e'), Player.BLACK, self.board)
        rook_king_side = Rook(Location(8, 'h'), Player.BLACK, self.board)
        rook_queen_side = Rook(Location(8, 'a'), Player.BLACK, self.board)
        self.assertTrue(king.can_castle(Side.KING))
        self.assertTrue(king.can_castle(Side.QUEEN))

    def test_can_castle_not_king(self):
        king = King(Location(8, 'e'), Player.BLACK, self.board)
        rook_queen_side = Rook(Location(8, 'a'), Player.BLACK, self.board)
        self.assertFalse(king.can_castle(Side.KING))
        self.assertTrue(king.can_castle(Side.QUEEN))

    def test_can_castle_not_queen(self):
        king = King(Location(8, 'e'), Player.BLACK, self.board)
        rook_king_side = Rook(Location(8, 'h'), Player.BLACK, self.board)
        self.assertTrue(king.can_castle(Side.KING))
        self.assertFalse(king.can_castle(Side.QUEEN))


class TestQueen(TestBase):
    def test_attacked_locations(self):
        queen = Queen(Location(5, 'd'), Player.BLACK, self.board)
        results = {Location(4, 'c'), Location(3, 'b'), Location(2, 'a'), Location(4, 'e'), Location(3, 'f'),
                   Location(2, 'g'), Location(1, 'h'), Location(6, 'c'), Location(7, 'b'), Location(8, 'a'),
                   Location(6, 'e'), Location(7, 'f'), Location(8, 'g'), Location(4, 'd'), Location(3, 'd'),
                   Location(2, 'd'), Location(1, 'd'), Location(6, 'd'), Location(7, 'd'), Location(8, 'd'),
                   Location(5, 'c'), Location(5, 'b'), Location(5, 'a'), Location(5, 'e'), Location(5, 'f'),
                   Location(5, 'g'), Location(5, 'h')}
        self.assertEquals(set(queen.attacked_locations()), results)


class TestRook(TestBase):
    def test_attacked_locations(self):
        rook = Rook(Location(5, 'd'), Player.BLACK,  self.board)
        results = {Location(4, 'd'), Location(3, 'd'), Location(2, 'd'), Location(1, 'd'), Location(6, 'd'),
                   Location(7, 'd'), Location(8, 'd'), Location(5, 'c'), Location(5, 'b'), Location(5, 'a'),
                   Location(5, 'e'), Location(5, 'f'), Location(5, 'g'), Location(5, 'h')}
        self.assertEquals(set(rook.attacked_locations()), results)


class TestBishop(TestBase):
    def test_attacked_locations(self):
        bishop = Bishop(Location(5, 'd'), Player.BLACK, self.board)
        results = {Location(4, 'c'), Location(3, 'b'), Location(2, 'a'), Location(4, 'e'), Location(3, 'f'),
                   Location(2, 'g'), Location(1, 'h'), Location(6, 'c'), Location(7, 'b'), Location(8, 'a'),
                   Location(6, 'e'), Location(7, 'f'), Location(8, 'g')}
        self.assertEquals(set(bishop.attacked_locations()), results)


class TestKnight(TestBase):
    def test_attacked_locations(self):
        knight = Knight(Location(5, 'd'), Player.BLACK, self.board)
        results = {Location(7, 'c'), Location(6, 'b'), Location(4, 'b'), Location(3, 'c'), Location(3, 'e'),
                   Location(4, 'f'), Location(6, 'f'), Location(7, 'e')}
        self.assertEquals(set(knight.attacked_locations()), results)


class TestPawn(TestBase):
    def test_attacked_locations_black(self):
        pawn = Pawn(Location(5, 'd'), Player.BLACK, self.board)
        queen = Queen(Location(4, 'c'), Player.WHITE, self.board)
        knight = Knight(Location(4, 'e'), Player.WHITE, self.board)
        results = {Location(4, 'c'), Location(4, 'e')}
        self.assertEquals(set(pawn.attacked_locations()), results)

    def test_attacked_locations_white(self):
        pawn = Pawn(Location(5, 'd'), Player.WHITE, self.board)
        queen = Queen(Location(6, 'c'), Player.BLACK, self.board)
        knight = Knight(Location(6, 'e'), Player.BLACK, self.board)
        results = {Location(6, 'c'), Location(6, 'e')}
        self.assertEquals(set(pawn.attacked_locations()), results)

    def test_attacked_locations_black_none(self):
        pawn = Pawn(Location(5, 'd'), Player.BLACK, self.board)
        results = set()
        self.assertEquals(set(pawn.attacked_locations()), results)

    def test_attacked_locations_white_none(self):
        pawn = Pawn(Location(5, 'd'), Player.WHITE, self.board)
        results = set()
        self.assertEquals(set(pawn.attacked_locations()), results)