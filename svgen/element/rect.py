"""
svgen - A module for the 'rect' element.
"""

# built-in
from math import isclose
from typing import Union

# internal
from svgen.attribute import PossibleAttributes, attributes
from svgen.attribute.viewbox import ViewBox
from svgen.cartesian import UNITY
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import DEFAULT, Point
from svgen.cartesian.rectangle import Rectangle
from svgen.cartesian.rectangle.corner import RectangleCorner
from svgen.cartesian.rectangle.grid import RectangleGrid
from svgen.color import Colorlike
from svgen.element.mixins import (
    FillColorMixin,
    RadiusXyMixin,
    RectangularMixin,
)


class Rect(FillColorMixin, RectangularMixin, RadiusXyMixin):
    """A class for rect elements."""

    def __init__(
        self,
        rect: Rectangle,
        rx: float = 0.0,
        ry: float = 0.0,
        attrs: PossibleAttributes = None,
        **extra,
    ) -> None:
        """Construct a new rect element."""

        RectangularMixin.__init__(self, rect)
        RadiusXyMixin.__init__(self, rx=rx, ry=ry)

        super().__init__(
            attrib=attributes(attrs)
            + list(self.rect_attributes)
            + list(self.radius_xy_attributes),
            **extra,
        )

    def corner(self, corner: RectangleCorner) -> Point:
        """Get a specific corner of a rectangle."""
        return self.rect.corner(corner)

    @property
    def top_left(self) -> Point:
        """Get the top left corner point."""
        return self.rect.top_left

    @property
    def top_right(self) -> Point:
        """Get the top right corner point."""
        return self.rect.top_right

    @property
    def bottom_left(self) -> Point:
        """Get the bottom left corner point."""
        return self.rect.bottom_left

    @property
    def bottom_right(self) -> Point:
        """Get the bottom right corner point."""
        return self.rect.bottom_right

    @staticmethod
    def create(
        width: float, height: float, point: Point = DEFAULT, **kwargs
    ) -> "Rect":
        """Create a rectangle element."""
        return Rect(Rectangle.create(width, height, point), **kwargs)

    @property
    def width(self) -> float:
        """Get the width of this rectangle element."""
        return self.rect.width

    @property
    def height(self) -> float:
        """Get the height of this rectangle element."""
        return self.rect.height

    @property
    def square(self) -> bool:
        """Determine if this rectangle is square."""

        return self.rect.square

    def to_square(self, scale: float = UNITY) -> "Rect":
        """Convert this rectangle to a square."""

        return Rect(self.rect.to_square(scale), self.rx, self.ry)

    def translate(self, move: Translation) -> "Rect":
        """Move this rectangle by a given translation."""

        return Rect(self.rect.translate(move), self.rx, self.ry)

    def scale(
        self, width_scale: float = UNITY, height_scale: float = UNITY
    ) -> "Rect":
        """Scale this rectangle's width and height."""

        return Rect(
            self.rect.scale(width_scale, height_scale),
            self.rx,
            self.ry,
        )

    def scale_whole(self, scalar: float = UNITY) -> "Rect":
        """Scale width and height of this rectangle equally."""

        return self.scale(scalar, scalar)

    def __eq__(self, other: object) -> bool:
        """Determine if this rectangle is equivalent to another."""

        if not isinstance(other, Rect):
            return NotImplemented
        return (
            self.rect == other.rect
            and isclose(self.rx, other.rx)
            and isclose(self.ry, other.ry)
        )

    @staticmethod
    def centered(
        box: Union[ViewBox, Rectangle],
        width_scale: float = UNITY,
        height_scale: float = UNITY,
        color: Colorlike = None,
        prop: str = "fill",
        square: bool = False,
        **kwargs,
    ) -> "Rect":
        """From a viewBox, created a centered-and-scaled rectangle."""

        # Compute everything from an actual rectangle instance.
        if isinstance(box, ViewBox):
            box = box.box

        rect = Rectangle.centered(box, width_scale, height_scale, square)

        # Handle translation.
        if "translation" in kwargs and kwargs["translation"]:
            rect = rect.translate(Translation(**kwargs["translation"]))
            del kwargs["translation"]

        result = Rect(rect, **kwargs)

        if color is not None:
            result.style.add_color(color, prop)
        return result

    def grid(self, columns: int, rows: int) -> RectangleGrid:
        """Create a grid from this rectangle."""
        return RectangleGrid(self.rect, columns, rows)
