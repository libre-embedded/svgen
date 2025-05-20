"""
svgen - A module for the 'viewBox' attribute.
"""

# built-in
from typing import NamedTuple, Union

# third-party
from vcorelib.dict import GenericStrDict

# internal
from svgen.attribute import Attribute
from svgen.cartesian import Dimensions
from svgen.cartesian.mutate import Translation
from svgen.cartesian.plane import Plane
from svgen.cartesian.point import Point
from svgen.cartesian.rectangle import Rectangle
from svgen.cartesian.rectangle.grid import RectangleGrid


class ViewBoxData(NamedTuple):
    """Primitive data for a viewBox attribute."""

    min_x: int
    min_y: int
    width: int
    height: int

    def translate(self, dx: int, dy: int) -> "ViewBoxData":
        """Translate this viewBox."""
        return ViewBoxData(
            self.min_x + dx, self.min_y + dy, self.width, self.height
        )

    @property
    def origin(self) -> Point:
        """Get the origin for this viewBox."""
        return Point(float(self.min_x), float(self.min_y))

    @property
    def center(self) -> Point:
        """Get the center point for this viewBox."""
        return Point(
            self.min_x + (float(self.width) / 2.0),
            self.min_y + (float(self.height) / 2.0),
            True,
        )

    @staticmethod
    def from_dict(data: GenericStrDict) -> "ViewBoxData":
        """Create viewBox data from a dictionary."""
        return ViewBoxData(
            data.get("min_x", 0),
            data.get("min_y", 0),
            data["width"],
            data["height"],
        )


class ViewBox(Attribute):
    """An interface for viewBox attributes."""

    def __init__(
        self, min_x: int, min_y: int, width: int, height: int
    ) -> None:
        """Construct a new viewBox."""

        self.data = ViewBoxData(min_x, min_y, width, height)
        self.plane = Plane(self.data.origin)
        self.box = Rectangle(self.dimensions, self.origin)
        self.grid = RectangleGrid(self.box, width, height)

    @property
    def width(self) -> int:
        """Get the width of this viewbox."""
        return self.data.width

    @property
    def height(self) -> int:
        """Get the height of this viewbox."""
        return self.data.height

    def new_grid(
        self, rect: Rectangle = None, columns: int = None, rows: int = None
    ) -> RectangleGrid:
        """Create a grid from this viewBox."""
        return self.grid.adjust(columns, rows, rect)

    def translate(
        self, dx: Union[Translation, float], *args, **kwargs
    ) -> None:
        """Apply a translation to this viewBox."""

        move = Translation.normalize(dx, *args, **kwargs)

        # Update instance attributes.
        self.data = self.data.translate(int(move.dx), int(move.dy))
        self.box = self.box.translate(move)
        self.plane.translate(move)
        self.grid = self.grid.translate(move)

    @property
    def dimensions(self) -> Dimensions:
        """Get this viewBox's dimensions."""
        return Dimensions(float(self.data.width), float(self.data.height))

    @property
    def origin(self) -> Point:
        """Get this viewBox's origin."""
        return self.plane.origin

    @property
    def key(self) -> str:
        """Get the string key for this attribute."""
        return "viewBox"

    @property
    def value(self) -> str:
        """Get the string value for this attribute."""
        return (
            f"{self.data.min_x} {self.data.min_y} "
            f"{self.data.width} {self.data.height}"
        )

    @property
    def center(self) -> Point:
        """Get the center point for this viewBox."""
        return self.data.center

    @classmethod
    def decode(cls: type["ViewBox"], key: str, value: str) -> "ViewBox":
        """Create this attribute from a string."""

        assert key == "viewBox"
        args = [int(x) for x in value.split()]
        assert len(args) == 4
        return cls(*args)

    @staticmethod
    def from_dict(data: GenericStrDict) -> "ViewBox":
        """Create a viewBox from dictionary data."""
        return ViewBox(*ViewBoxData.from_dict(data))
