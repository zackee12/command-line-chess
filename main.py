from board import Board
from board.move import Move
from util import input_parser
import util.printer as printer
from util.enums import Player

if __name__ == '__main__':
    # get desired player or None for two player
    player = input_parser.player()

    # load and print initial board
    board = Board(True)
    printer.print_board(board)

    # game loop
    while True:
        # if checkmate then end the game
        if board.checkmate():
            print('{} wins by checkmate'.format(Player.opponent(board.turn)))
            break
        # if draw then end the game
        if board.draw():
            print('draw!')
            break
        # print check message
        if board.check(board.turn):
            print('check!!!')

        if player is None or board.turn == player:
            cmd = input_parser.cmd(board)

            if isinstance(cmd, Move):  # move
                board.move(cmd)
                printer.print_board(board)
            elif cmd == 'q':  # quit
                break
            elif cmd == 'r':  # random move
                board.random_move()
                printer.print_board(board)
            elif cmd == 'l':  # list possible moves
                printer.print_moves(board)
            elif cmd == 's':  # current score
                printer.print_score(board)
            else:
                pass
        else:
            # ai turn
            board.random_move()
            print(board)

