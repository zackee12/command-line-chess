from unittest import TestCase

from board import Board
from util.input_parser import parse
from util.enums import Player, Side
from piece import Pawn, Queen, Rook, Bishop, Knight, King
from board.location import Location
from util.printer import print_moves


class TestBoard(TestCase):
    def setUp(self):
        self.board = Board()

    def batch_move(self, board, moves):
        for move in moves:
            move = parse(board, move)
            self.board.move(move)

    def test_two_move_checkmate_recommend_move(self):
        moves = [
            'f2 f3',
            'e7 e5',
            'g2 g4',
            #'d8 h4',
        ]
        self.batch_move(self.board, moves)

        move = self.board.recommended_move(1)
        desired_move = parse(self.board, 'd8 h4')
        self.assertEquals(move, desired_move)

    def test_draw_losing(self):
        moves = [
            'c2 c4',
            'h7 h5',
            'h2 h4',
            'a7 a5',
            'd1 a4',
            'a8 a6',
            'a4 a5',
            'a6 h6',
            'a5 c7',
            'f7 f6',
            'c7 d7',
            'e8 f7',
            'd7 b7',
            'd8 d3',
            'b7 b8',
            'd3 h7',
            'b8 c8',
            'f7 g6',
            #'c8 e6',
        ]
        self.batch_move(self.board, moves)
        move = self.board.recommended_move(1)
        desired_move = parse(self.board, 'c8 e6')
        self.assertEquals(move, desired_move)