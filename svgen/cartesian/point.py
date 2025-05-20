"""
A module for interfacing with points.
"""

# built-in
from math import isclose, sqrt
from typing import NamedTuple, Union

# internal
from svgen.attribute import SimpleAttribute
from svgen.cartesian.mutate import Translation


class PointAttrs(NamedTuple):
    """A grouping for 'x' and 'y' attributes."""

    x: SimpleAttribute
    y: SimpleAttribute

    @property
    def x_val(self) -> float:
        """Get the 'x' coordinate for these attributes."""
        return float(self.x.value)

    @property
    def y_val(self) -> float:
        """Get the 'y' coordinate for these attributes."""
        return float(self.y.value)


class Point(NamedTuple):
    """A definition of a point in a Cartesian coordinate system."""

    x: float = 0.0
    y: float = 0.0
    center: bool = False
    idx: int = -1

    def translate(self, move: Union[Translation, float], *args) -> "Point":
        """Move a point by a given translation."""
        move = (
            Translation(move, *args)
            if not isinstance(move, Translation)
            else move
        )
        return Point(self.x + move.dx, self.y + move.dy, self.center, self.idx)

    def with_index(self, idx: int) -> "Point":
        """Get a new point with the specified index, from an existing point."""
        return Point(self.x, self.y, False, idx)

    @property
    def x_attr(self) -> SimpleAttribute:
        """Get the 'x' attribute for this point."""

        attr = "x"
        if self.center:
            attr = "c" + attr
        elif self.idx >= 0:
            attr += str(self.idx)
        return SimpleAttribute(attr, str(self.x))

    @property
    def y_attr(self) -> SimpleAttribute:
        """Get the 'y' attribute for this point."""

        attr = "y"
        if self.center:
            attr = "c" + attr
        elif self.idx >= 0:
            attr += str(self.idx)
        return SimpleAttribute(attr, str(self.y))

    @property
    def attrs(self) -> PointAttrs:
        """Get the 'x' and 'y' attributes for this point."""
        return PointAttrs(self.x_attr, self.y_attr)

    def __eq__(self, other: object) -> bool:
        """Determine if two points are the same."""

        if not isinstance(other, Point):
            return NotImplemented
        return isclose(self.x, other.x) and isclose(self.y, other.y)

    def distance(self, point: "Point") -> float:
        """Compute the distance from this point to another."""

        run = point.x - self.x
        rise = point.y - self.y
        return sqrt(run * run + rise * rise)

    def to_center(self) -> "Point":
        """
        Convert an existing point to one that is definitely a 'center' type.
        """
        return Point(self.x, self.y, True)


def to_center(point: Point) -> Point:
    """Convert an existing point to one that is definitely a 'center' type."""
    return point.to_center()


DEFAULT = Point()
DEFAULT_CENTER = to_center(DEFAULT)
NamedPoints = dict[str, Point]


class PointManager:
    """A class for managing points."""

    def __init__(self, points: NamedPoints = None) -> None:
        """Initialize this point manager."""

        if points is None:
            points = {}
        self.points = points

    def get_point(self, name: str) -> Point:
        """Access a point object."""
        return self.points[name]

    def add_point(self, name: str, point: Union[Point, float], *args) -> Point:
        """Add a named point to this manager."""

        if not isinstance(point, Point):
            point = Point(point, *args)

        assert name not in self.points, f"Already managing point '{name}'!"
        self.points[name] = point
        return self.points[name]

    def translate(self, move: Union[Translation, float], *args) -> None:
        """Translate all entities in the plane by some amount."""

        for key, val in self.points.items():
            self.points[key] = val.translate(move, *args)
