"""
svgen - A module for Cartesian-coordinate interfaces.
"""

# built-in
from math import isclose
from typing import NamedTuple

# internal
from svgen.attribute import SimpleAttribute
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import DEFAULT, Point

UNITY: float = 1.0


def distance(point_a: Point, point_b: Point = DEFAULT) -> float:
    """Compute the distance between two points."""

    return point_a.distance(point_b)


class DimensionAttrs(NamedTuple):
    """A grouping for 'width' and 'height' attributes."""

    width: SimpleAttribute
    height: SimpleAttribute

    @property
    def width_val(self) -> float:
        """Get this 'width' value for these dimensions."""
        return float(self.width.value)

    @property
    def height_val(self) -> float:
        """Get the 'height' value for these dimensions."""
        return float(self.height.value)


class Dimensions(NamedTuple):
    """A set of dimensions describing a rectangular entity."""

    width: float
    height: float

    def __str__(self) -> str:
        """Get this instance as a string."""
        return f"width={self.width}, height={self.height})"

    def __hash__(self) -> int:
        """Get a suitable hash value for this instance."""
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        """Determine if these dimensions are equivalent to another set."""

        if not isinstance(other, Dimensions):
            return NotImplemented
        return isclose(self.width, other.width) and isclose(
            self.height, other.height
        )

    @property
    def dx(self) -> float:
        """An alias for width."""
        return self.width

    @property
    def dy(self) -> float:
        """An alias for height."""
        return self.height

    @property
    def width_attr(self) -> SimpleAttribute:
        """Get the 'width' attribute for these dimensions."""
        return SimpleAttribute("width", str(self.width))

    @property
    def height_attr(self) -> SimpleAttribute:
        """Get the 'height' attribute for these dimensions."""
        return SimpleAttribute("height", str(self.height))

    @property
    def attrs(self) -> DimensionAttrs:
        """Get the 'width' and 'height' attributes for these dimensions."""
        return DimensionAttrs(self.width_attr, self.height_attr)

    @property
    def square(self) -> bool:
        """Determine if these dimensions are square."""
        return isclose(self.width, self.height)

    def scale(
        self, width_scale: float = UNITY, height_scale: float = UNITY
    ) -> "Dimensions":
        """Scale these dimensions."""
        return Dimensions(self.width * width_scale, self.height * height_scale)

    def to_square(self, scale: float = UNITY) -> "Dimensions":
        """Convert these dimensions to a scaled square."""
        return self.to_centered_square(scale)[0]

    def to_centered_square(
        self, scale: float = UNITY
    ) -> tuple["Dimensions", Translation]:
        """
        Make dimensions square and determine the resulting translation that
        would be needed to logically center the new object.
        """

        length = min(self.width, self.height)
        dimensions = Dimensions(length, length).scale(scale, scale)

        # Determine how much the object needs to move if the caller wants to
        # center the result.
        dx = abs(self.width - dimensions.dx) / 2.0
        dy = abs(self.height - dimensions.dy) / 2.0

        return dimensions, Translation(dx, dy)
