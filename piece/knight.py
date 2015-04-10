from piece.base import SingleMovePiece


class Knight(SingleMovePiece):
    VALUE = 3
    MOVE_VECTORS = [
        (-2, 1),
        (-2, -1),
        (2, 1),
        (2, -1),
        (-1, 2),
        (-1, -2),
        (1, 2),
        (1, -2)
    ]

