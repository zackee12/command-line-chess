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
        self.board2 = Board(False)
        King(Location(8, 'e'), Player.BLACK, self.board2)
        King(Location(1, 'e'), Player.WHITE, self.board2)

    def batch_move(self, board, moves):
        for move in moves:
            move = parse(board, move)
            self.board.move(move)

    def test_two_move_checkmate(self):
        moves = [
            'f2 f3',
            'e7 e5',
            'g2 g4',
            'd8 h4',
        ]
        self.batch_move(self.board, moves)

        self.assertTrue(self.board.checkmate())

    def test_draw(self):
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
            'c8 e6',
        ]
        self.assertFalse(self.board.draw())
        self.batch_move(self.board, moves)
        self.assertTrue(self.board.draw())
        self.assertFalse(self.board.checkmate())

    def test_en_passant(self):
        moves = [
            'a2 a4',
            'a7 a6',
            'a4 a5',
            'b7 b5',
        ]
        self.batch_move(self.board, moves)

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
        self.batch_move(self.board, moves)

        move = parse(self.board, 'e1 g1')  # white
        self.assertTrue(move.castle)
        self.assertTrue(move in self.board.valid_moves())
        self.assertEquals(move.castle_side, Side.KING)
        self.assertEquals(str(move), 'O-O')
        self.board.move(move)

    def test_queen_side_castle(self):
        moves = [
            'b1 a3',
            'a7 a6',
            'b2 b4',
            'b7 b6',
            'c1 b2',
            'c7 c6',
            'c2 c4',
            'd7 d6',
            'd1 c2',
            'e7 e6',
        ]
        self.batch_move(self.board, moves)

        move = parse(self.board, 'e1 c1')  # white
        self.assertTrue(move.castle)
        self.assertTrue(move in self.board.valid_moves())
        self.assertEquals(move.castle_side, Side.QUEEN)
        self.assertEquals(str(move), 'O-O-O')
        self.board.move(move)

    def test_king_side_castle_check_in_middle(self):
        Rook(Location(1, 'h'), Player.WHITE, self.board2)
        Queen(Location(2, 'f'), Player.BLACK, self.board2)
        with self.assertRaises(IOError):
            parse(self.board2, 'e1 g1')

    def test_queen_side_castle_check_in_middle(self):
        Rook(Location(1, 'a'), Player.WHITE, self.board2)
        Queen(Location(2, 'd'), Player.BLACK, self.board2)
        with self.assertRaises(IOError):
            parse(self.board2, 'e1 c1')

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
        self.batch_move(self.board, moves)

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

    def test_random_game(self):
        for i in range(5):
            if self.board.checkmate():
                break
            if self.board.draw():
                break

            self.assertEquals(len(self.board._moves), i)
            self.board.random_move()

    def test_score(self):
        self.assertEquals(self.board2.score(Player.BLACK), 0)
        p = Pawn(Location(2, 'a'), Player.WHITE, self.board2)
        self.board2.capture_piece(p)
        self.assertEquals(self.board2.score(Player.BLACK), Pawn.VALUE)
        k = Knight(Location(3, 'a'), Player.WHITE, self.board2)
        self.board2.capture_piece(k)
        self.assertEquals(self.board2.score(Player.BLACK), Pawn.VALUE + Knight.VALUE)

    def test_last_move(self):
        self.assertEquals(self.board2.last_move(), None)

    def test_pieces(self):
        all_pieces = list(self.board.pieces())
        self.assertEquals(all_pieces, self.board._pieces)
        kings = list(self.board.pieces(piece_class=King))
        self.assertTrue(all([king.__class__ is King for king in kings]))
        white = list(self.board.pieces(player=Player.WHITE))
        self.assertTrue(all([p.player is Player.WHITE for p in white]))
        white_knights = list(self.board.pieces(piece_class=Knight, player=Player.WHITE))
        self.assertTrue(all([p.player is Player.WHITE and p.__class__ is Knight for p in white_knights]))

    def test_str(self):
        s = "-----------------------------------\n" \
            "8 | R | N | B | Q | K | B | N | R |\n" \
            "-----------------------------------\n" \
            "7 | P | P | P | P | P | P | P | P |\n" \
            "-----------------------------------\n" \
            "6 |   |   |   |   |   |   |   |   |\n" \
            "-----------------------------------\n" \
            "5 |   |   |   |   |   |   |   |   |\n" \
            "-----------------------------------\n" \
            "4 |   |   |   |   |   |   |   |   |\n" \
            "-----------------------------------\n" \
            "3 |   |   |   |   |   |   |   |   |\n" \
            "-----------------------------------\n" \
            "2 | p | p | p | p | p | p | p | p |\n" \
            "-----------------------------------\n" \
            "1 | r | n | b | q | k | b | n | r |\n" \
            "-----------------------------------\n" \
            "  | a | b | c | d | e | f | g | h |\n"
        self.board.character_map.unicode = False
        self.assertEquals(str(self.board), s)