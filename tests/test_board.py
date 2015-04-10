from unittest import TestCase

from board import Board
from util.input_parser import parse
from util.enums import Player
from piece import Pawn, Queen, Rook, Bishop, Knight


class TestBoard(TestCase):
    def setUp(self):
        self.board = Board()

    def batch_move(self, moves):
        for move in moves:
            move = parse(self.board, move)
            self.board.move(move)

    def test_two_move_checkmate(self):
        moves = [
            'f2 f3',
            'e7 e5',
            'g2 g4',
            'd8 h4',
        ]
        self.batch_move(moves)

        self.assertTrue(self.board.checkmate())

    def test_en_passant(self):
        moves = [
            'a2 a4',
            'a7 a6',
            'a4 a5',
            'b7 b5',
        ]
        self.batch_move(moves)

        move = parse(self.board, 'a5 b6')  # white en passant attack
        self.assertTrue(move.en_passant)
        self.assertTrue(move in self.board.valid_moves())
        self.assertEquals(self.board.score(Player.WHITE), 0)
        self.board.move(move)
        self.assertEquals(self.board.score(Player.WHITE), Pawn.VALUE)

    def test_king_side_castle(self):
        moves = [
            'g1 h3',
            'a7 a6',
            'g2 g4',
            'b7 b6',
            'f1 g2',
            'c7 c6',
        ]
        self.batch_move(moves)

        move = parse(self.board, 'e1 g1')  # white
        self.assertTrue(move.castle)
        self.assertTrue(move in self.board.valid_moves())
        self.board.move(move)

    def test_promotion(self):
        moves = [
            'a2 a4',
            'b7 b5',
            'a4 b5',
            'h7 h6',
            'b5 b6',
            'g7 g6',
            'b6 a7',
            'f7 f6',
        ]
        self.batch_move(moves)

        with self.assertRaises(IOError):
            parse(self.board, 'a7 b8')

        move = parse(self.board, 'a7 b8 q')
        self.assertTrue(move.promotion)
        self.assertEquals(move.promotion_piece_class, Queen)

        move = parse(self.board, 'a7 b8 r')
        self.assertTrue(move.promotion)
        self.assertEquals(move.promotion_piece_class, Rook)

        move = parse(self.board, 'a7 b8 b')
        self.assertTrue(move.promotion)
        self.assertEquals(move.promotion_piece_class, Bishop)

        move = parse(self.board, 'a7 b8 n')
        self.assertTrue(move.promotion)
        self.assertEquals(move.promotion_piece_class, Knight)

        self.board.move(move)
        self.assertEquals(self.board.piece(move.new_location).__class__, Knight)
