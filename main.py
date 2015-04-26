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
    unicode = input_parser.use_unicode(board)
    printer.print_board(board)

    # game loop
    while True:
        # if checkmate then end the game
        check, draw, checkmate = board.status()
        if checkmate:
            print('{} wins by checkmate'.format(Player.opponent(board.current_player)))
            break
        # if draw then end the game
        if draw:
            print('draw!')
            break
        # print check message
        if check:
            print('check!!!')

        # if a human then ask for input
        if player is None or board.current_player == player:
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
            # move = board.random_move()
            print('ai thinking...')
            move = board.recommended_move()
            board.move(move)
            print('{} moved {}'.format(board.current_player.opponent(), board.last_move()))
            printer.print_board(board)

