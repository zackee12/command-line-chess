from util.enums import Color


class Location:
    ROWS = [1, 2, 3, 4, 5, 6, 7, 8]  # RANKS
    COLS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']  # FILES

    def __init__(self, row, col):
        self.row, self.col = row, col.lower()

        if self.row not in self.ROWS:
            raise ValueError("'{}' is not a valid location")
        elif self.col not in self.COLS:
            raise ValueError("'{}' is not a valid location")

    @property
    def color(self):
        """ Color of the board location

        :return: BLACK or WHITE
        """
        even_col = self.COLS.index(self.col) % 2 == 0
        even_row = self.ROWS.index(self.row) % 2 == 0
        if even_row:
            return Color.BLACK if even_col else Color.WHITE
        else:
            return Color.WHITE if even_col else Color.BLACK

    def offset(self, rows, cols):
        """ offset by the number of cols and rows specified

        :param cols: number of cols to offset by (+/-)
        :param rows: number of rows to offset by (+/-)
        :return: Location or None if out of bounds
        """
        col = self.COLS.index(self.col) + cols
        row = self.ROWS.index(self.row) + rows
        if 0 <= col < len(self.COLS) and 0 <= row < len(self.ROWS):
            return Location(self.ROWS[row], self.COLS[col])
        return None

    @property
    def end_of_row(self):
        return self.row == self.ROWS[0] or self.row == self.ROWS[-1]

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, repr(self.row), repr(self.col))

    def __str__(self):
        return '{}{}'.format(self.col, self.row)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if hasattr(other, 'col') and hasattr(other, 'row'):
            return (self.col, self.row) == (other.col, other.row)
        else:
            return str(self) == str(other)

    def __getitem__(self, index):
        if index == 0:
            return self.row
        elif index == 1:
            return self.col
        else:
            raise IndexError("'{}' is invalid: use 0 for row and 1 for col".format(index))

    @classmethod
    def from_string(cls, location):
        if len(location) != 2:
            raise ValueError('string must be 2 characters (e.g. a5)')

        row, col = location[1], location[0]
        if not row.isdigit():
            raise ValueError('2nd character must be an integer (e.g. a5)')

        return cls(int(row), col)

    @classmethod
    def from_between(cls, l1, l2, inclusive=False):
        if l1.row == l2.row:
            low_idx = min(cls.COLS.index(l1.col), cls.COLS.index(l2.col))
            high_idx = max(cls.COLS.index(l1.col), cls.COLS.index(l2.col)) + 1
            if not inclusive:
                low_idx += 1
                high_idx -= 1
            for i in cls.COLS[low_idx:high_idx]:
                yield cls(l1.row, i)
        elif l1.col == l2.col:
            low_idx = min(cls.ROWS.index(l1.row), cls.ROWS.index(l2.row))
            high_idx = max(cls.ROWS.index(l1.row), cls.ROWS.index(l2.row)) + 1
            if not inclusive:
                low_idx += 1
                high_idx -= 1
            for i in cls.ROWS[low_idx:high_idx]:
                yield cls(i, l1.col)
        else:
            raise ValueError('locations must be on the same row or column')