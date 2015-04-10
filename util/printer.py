from util.enums import Player


def print_moves(board):
    """ Print all valid moves in long algebraic form

    :param board: Board class
    :return: None
    """
    for move in board.valid_moves():
        print(str(move))


def print_score(board):
    """ Print score for both players

    :param board: board class
    :return: None
    """
    print('White: {}'.format(board.score(Player.WHITE)))
    print('Black: {}'.format(board.score(Player.BLACK)))


def print_board(board):
    """ Print chessboard

    :param board: board class
    :return: None
    """
    print(board)