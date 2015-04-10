from piece.base import MultipleMovePiece


class Queen(MultipleMovePiece):
    VALUE = 9
    MOVE_VECTORS = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]
