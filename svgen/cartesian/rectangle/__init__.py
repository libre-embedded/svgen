"""
svgen - A module for interacting with rectangular entities.
"""

# built-in
from typing import NamedTuple, Union

# internal
from svgen.cartesian import UNITY, Dimensions
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import DEFAULT, Point
from svgen.cartesian.rectangle.corner import RectangleCorner


class Rectangle(NamedTuple):
    """A definition of a rectangle."""

    dimensions: Dimensions
    location: Point = DEFAULT

    def contains(self, point: Point) -> bool:
        """Determine if a point is within this rectangle."""

        return (
            self.location.x
            <= point.x
            <= self.location.x + self.dimensions.width
        ) and self.location.y <= point.y <= self.dimensions.height

    def __eq__(self, other: object) -> bool:
        """Determine if this rectangle is equivalent to another."""

        if not isinstance(other, Rectangle):
            return NotImplemented
        return (
            self.dimensions == other.dimensions
            and self.location == other.location
        )

    @property
    def width(self) -> float:
        """Get the width of this rectangle."""
        return self.dimensions.width

    @property
    def height(self) -> float:
        """Get the height of this rectangle.."""
        return self.dimensions.height

    @property
    def square(self) -> bool:
        """Determine if this rectangle is square."""
        return self.dimensions.square

    @property
    def center(self) -> Point:
        """Get the center location of this rectangle."""
        return Point(
            self.location.x + (self.width / 2.0),
            self.location.y + (self.height / 2.0),
            True,
        )

    def translate(
        self, move: Union[Translation, float], *args, **kwargs
    ) -> "Rectangle":
        """Move a rectangle by a given translation."""

        return Rectangle(
            self.dimensions,
            self.location.translate(
                Translation.normalize(move, *args, **kwargs)
            ),
        )

    def scale(
        self, width_scale: float = UNITY, height_scale: float = UNITY
    ) -> "Rectangle":
        """Scale this rectangle's width and height."""
        return Rectangle(
            self.dimensions.scale(width_scale, height_scale), self.location
        )

    def scale_whole(self, scalar: float = UNITY) -> "Rectangle":
        """Scale width and height of this rectangle equally."""
        return self.scale(scalar, scalar)

    def to_square(self, scale: float = UNITY) -> "Rectangle":
        """Convert this rectangle to a square."""
        dimensions, move = self.dimensions.to_centered_square(scale)
        return Rectangle(dimensions, self.location.translate(move))

    @staticmethod
    def create(
        width: float, height: float, point: Point = DEFAULT
    ) -> "Rectangle":
        """Create a rectangle from simple parameters."""
        return Rectangle(Dimensions(width, height), point)

    @staticmethod
    def centered(
        source: "Rectangle",
        width_scale: float = UNITY,
        height_scale: float = UNITY,
        square: bool = False,
    ) -> "Rectangle":
        """Create a centered rectangle from another rectangle."""

        # Convert the source rectangle to a square, first.
        if square:
            dimensions, move = source.dimensions.to_centered_square()
            source = Rectangle(dimensions, source.location)
            source = source.translate(move)

        dimensions = source.dimensions.scale(width_scale, height_scale)
        delta_x = (source.dimensions.width - dimensions.width) / 2.0
        delta_y = (source.dimensions.height - dimensions.height) / 2.0
        return Rectangle(
            dimensions, source.origin.translate(Translation(delta_x, delta_y))
        )

    def from_center(
        self,
        width_scale: float = UNITY,
        height_scale: float = UNITY,
        square: bool = False,
    ) -> "Rectangle":
        """Create a new rectangle from this instance's center."""
        return Rectangle.centered(self, width_scale, height_scale, square)

    def corner(self, corner: RectangleCorner) -> Point:
        """Get a specific corner of a rectangle."""
        return corner.origin(self.dimensions, self.location)

    @property
    def top_left(self) -> Point:
        """Get the top left corner point."""
        return self.corner(RectangleCorner.TOP_LEFT)

    @property
    def origin(self) -> Point:
        """Get the origin location for this rectangle."""
        return self.top_left

    @property
    def top_right(self) -> Point:
        """Get the top right corner point."""
        return self.corner(RectangleCorner.TOP_RIGHT)

    @property
    def bottom_left(self) -> Point:
        """Get the bottom left corner point."""
        return self.corner(RectangleCorner.BOTTOM_LEFT)

    @property
    def bottom_right(self) -> Point:
        """Get the bottom right corner point."""
        return self.corner(RectangleCorner.BOTTOM_RIGHT)
