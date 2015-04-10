from board import Board
from board.move import Move
from util import input_parser
from util.printer import print_moves
from util.enums import Player

if __name__ == '__main__':
    player = input_parser.player()

    # load and print initial board
    board = Board(True)
    print(board)

    # game loop
    while True:
        if board.checkmate():
            print('{} wins by checkmate'.format(Player.opponent(board.turn)))
            break
        if board.draw():
            print('draw!')
            break
        if board.check(board.turn):
            print('check!!!')

        if player is None or board.turn == player:
            cmd = input_parser.cmd(board)

            if isinstance(cmd, Move):
                board.move(cmd)
                print(board)
            elif cmd == 'q':
                break
            elif cmd == 'r':
                board.random_move()
                print(board)
            elif cmd == 'l':
                print_moves(board.valid_moves())
            else:
                pass
        else:
            # ai turn
            board.random_move()
            print(board)

