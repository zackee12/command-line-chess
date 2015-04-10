import re
from util.enums import Player
from piece import Queen, Rook, Bishop, Knight


def player():
    """ Prompt the user to enter the number of players and desired color if single player

    :return: Player enum or None if a 2 player game
    """
    while True:
        num = input('1 or 2 players?: ').lower()
        if num == '1':
            break
        elif num == '2':
            return None
        else:
            print('try again: invalid number of players')

    while True:
        p = input('black (b) or white (w)?: ').lower()
        if p == 'b':
            return Player.BLACK
        elif p == 'w':
            return Player.WHITE
        else:
            print('try again: invalid color')


def cmd(board):
    """ Prompt the user for a command until valid input is entered

    :param board: Board class
    :return:  Move class or str (e.g. 'q', 'r', 'l', 's')
    """
    while True:
        text = input('{}: enter command: '.format(board.turn))
        try:
            cmd = parse(board, text)
        except IOError as e:
            print('Error!', e)
        else:
            return cmd


def parse(board, text):
    """ Parse text input into a command (Move or str)

    :param board: Board class
    :param text: str cmd
    :return: Move class or str (e.g. 'q', 'r', 'l', 's')
    """
    text = text.lower().strip()
    # built-in string command
    if text == 'q' or text == 'r' or text == 'l' or text == 's':
        return text
    else:
        # match to a standard move without promotion (e.g. a2 a4)
        if re.match('^[a-h][1-9] [a-h][1-9]$', text):
            matches = re.findall('[a-h][1-9]', text)
            return create_move(board, matches[0], matches[1])
        # match to a move with promotion character specified (e.g. a7 a8 q)
        elif re.match('^[a-h][1-9] [a-h][1-9] [qrbn]$', text):
            matches = re.findall('[a-h][1-9]', text)
            c = re.findall('[qrbn]', text)[-1]
            c = promotion_char_to_class(c)
            return create_move(board, matches[0], matches[1], c)
        else:
            raise IOError('command is invalid')


def create_move(board, from_location, to_location, promotion_class=None):
    """ Create a move based on user from and to location as well as an optional promotion value

    :param board: Board class
    :param from_location: Location to move piece from
    :param to_location: Location to move piece to
    :param promotion_class: class of piece for pawn promotion
    :return: Move
    """
    # try to get the piece at origin location
    p = board.piece(from_location, board.turn)
    if p is None:
        raise IOError('{} has no piece at {}'.format(board.turn, from_location))

    # check all moves for a match in from and to location as well as promotion and promotion class
    for move in p.moves():
        if move.old_location == from_location and move.new_location == to_location:
            if (promotion_class is None and not move.promotion) or \
                    (promotion_class and move.promotion and move.promotion_piece_class == promotion_class):
                # check to make sure the move is valid
                if board.valid_move(move):
                    return move
                else:
                    raise IOError('move from {} to {} results in check'.format(from_location, to_location))

    # customize error message depending on if promotion is specified
    if promotion_class is None:
        raise IOError('move from {} to {} is not possible'.format(from_location, to_location))
    raise IOError('move from {} to {} with {} promotion is not possible'
                  .format(from_location, to_location, promotion_class.__name__.lower()))


def promotion_char_to_class(c):
    """ Convert promotion character into a class

    :param c: str character
    :return: class of piece
    """
    if c == 'q':
        c = Queen
    elif c == 'r':
        c = Rook
    elif c == 'b':
        c = Bishop
    elif c == 'n':
        c = Knight
    else:
        raise IOError('promotion class does not exist for character: {}'.format(c))
    return c