from unittest import TestCase
from board import Location
from util.enums import Color


class TestLocation(TestCase):

    def test_constructor_out_of_bounds(self):
        with self.assertRaises(ValueError):
            l = Location(50, 'a')

    def test_color(self):
        l1, l2, l3, l4 = Location(1, 'a'), Location(5, 'c'), Location(5, 'f'), Location(8, 'a')
        self.assertEquals(l1.color, Color.BLACK)
        self.assertEquals(l2.color, Color.BLACK)
        self.assertEquals(l3.color, Color.WHITE)
        self.assertEquals(l4.color, Color.WHITE)

    def test_offset(self):
        l = Location(1, 'a').offset(1, 1)
        self.assertEquals(l, Location(2, 'b'))

    def test_offset_out_of_bounds(self):
        l = Location(1, 'a').offset(-1, 1)
        self.assertEquals(l, None)

    def test_from_string(self):
        l = Location.from_string('a1')
        self.assertEquals(l.row, 1)
        self.assertEquals(l.col, 'a')

    def test_from_between_rows(self):
        comp = [Location(2, 'a'), Location(3, 'a'), Location(4, 'a')]
        ls = list(Location.from_between(Location(1, 'a'), Location(5, 'a')))
        self.assertEquals(comp, ls)

    def test_from_between_cols(self):
        comp = [Location(2, 'b'), Location(2, 'c'), Location(2, 'd')]
        ls = list(Location.from_between(Location(2, 'a'), Location(2, 'e')))
        self.assertEquals(comp, ls)

    def test_from_between_rows_inclusive(self):
        comp = [Location(2, 'a'), Location(3, 'a'), Location(4, 'a')]
        ls = list(Location.from_between(Location(2, 'a'), Location(4, 'a'), inclusive=True))
        self.assertEquals(comp, ls)

    def test_from_between_cols_inclusive(self):
        comp = [Location(2, 'b'), Location(2, 'c'), Location(2, 'd')]
        ls = list(Location.from_between(Location(2, 'b'), Location(2, 'd'), inclusive=True))
        self.assertEquals(comp, ls)

    def test_from_between_error(self):
        with self.assertRaises(ValueError):
            list(Location.from_between(Location(1, 'b'), Location(2, 'c')))