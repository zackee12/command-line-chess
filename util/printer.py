from util.enums import Player


def print_moves(board):
    for move in board.valid_moves():
        print(str(move))


def print_score(board):
    print('White: {}\nBlack: {}'.format(board.score(Player.WHITE), board.score(Player.BLACK)))


def print_board(board):
    print(board)