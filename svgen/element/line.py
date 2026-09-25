"""
svgen - A module for the 'line' element.
"""

# built-in

# internal
from svgen.attribute import PossibleAttributes, attributes
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import Point
from svgen.element import Element


class Line(Element):
    """A definition of a line."""

    def __init__(
        self, p1: Point, p2: Point, attrs: PossibleAttributes = None, **extra
    ) -> None:
        """Initialize this line."""

        self.p1 = p1.with_index(1)
        self.p2 = p2.with_index(2)

        real_attrs = attributes(attrs)
        real_attrs.extend(
            [
                self.p1.x_attr,
                self.p1.y_attr,
                self.p2.x_attr,
                self.p2.y_attr,
            ]
        )
        super().__init__(attrib=real_attrs, **extra)

    def translate(self, move: Translation | float, *args, **kwargs) -> "Line":
        """Move a rectangle by a given translation."""
        move = Translation.normalize(move, *args, **kwargs)
        return Line(self.p1.translate(move), self.p2.translate(move))

    @staticmethod
    def create(
        x2: float,
        y2: float,
        x1: float = 0.0,
        y1: float = 0.0,
        attrs: PossibleAttributes = None,
        **extra,
    ) -> "Line":
        """Create a line."""
        return Line(Point(x1, y1), Point(x2, y2), attrs, **extra)


def line(
    x2: float,
    y2: float,
    x1: float = 0.0,
    y1: float = 0.0,
    attrs: PossibleAttributes = None,
    **extra,
) -> Line:
    """Create a line."""
    return Line.create(x2, y2, x1, y1, attrs, **extra)
