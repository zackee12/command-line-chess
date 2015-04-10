from piece.base import MultipleMovePiece


class Bishop(MultipleMovePiece):
    VALUE = 3
    MOVE_VECTORS = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1)
    ]
