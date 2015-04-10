from piece.base import MultipleMovePiece


class Rook(MultipleMovePiece):
    VALUE = 5
    MOVE_VECTORS = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]
