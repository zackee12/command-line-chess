import re
from util.enums import Player
from piece import Queen, Rook, Bishop, Knight


def player():
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
    while True:
        text = input('{}: enter command: '.format(board.turn))
        try:
            cmd = parse(board, text)
        except IOError as e:
            print('Error!', e)
        else:
            return cmd


def parse(board, text):
    text = text.lower().strip()
    if text == 'q' or text == 'r' or text == 'l' or 's':
        return text
    else:
        if re.match('^[a-h][1-9] [a-h][1-9]$', text):
            matches = re.findall('[a-h][1-9]', text)
            return create_move(board, matches[0], matches[1])
        elif re.match('^[a-h][1-9] [a-h][1-9] [qrbn]$', text):
            matches = re.findall('[a-h][1-9]', text)
            c = re.findall('[qrbn]', text)[-1]
            if c == 'q':
                c = Queen
            elif c == 'r':
                c = Rook
            elif c == 'b':
                c = Bishop
            elif c == 'n':
                c = Knight
            else:
                raise IOError('uh oh... not sure what happened')
            return create_move(board, matches[0], matches[1], c)
        else:
            raise IOError('command is invalid')


def create_move(board, from_location, to_location, promotion_class=None):
    p = board.piece(from_location, board.turn)
    if p is None:
        raise IOError('{} has no piece at {}'.format(board.turn, from_location))
    for move in p.moves():
        if move.old_location == from_location and move.new_location == to_location:
            if (promotion_class is None and not move.promotion) or \
                    (promotion_class and move.promotion and move.promotion_piece_class == promotion_class):
                if board.valid_move(move):
                    return move
                else:
                    raise IOError('move from {} to {} results in check'.format(from_location, to_location))

    if promotion_class is None:
        raise IOError('move from {} to {} is not possible'.format(from_location, to_location))
    raise IOError('move from {} to {} with {} promotion is not possible'
                  .format(from_location, to_location, promotion_class.__name__.lower()))