"""
A module implementing grid interfaces for rectangles.
"""

# built-in
from collections.abc import Iterable
from typing import NamedTuple

# internal
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import Point
from svgen.cartesian.rectangle import Rectangle


class RectangleIndex(NamedTuple):
    """An index into a rectangle grid."""

    column: int
    row: int


class RectangleGrid(NamedTuple):
    """A class for locating points within a rectangle."""

    rect: Rectangle
    columns: int
    rows: int

    @property
    def x_scale(self) -> float:
        """Get the scalar value for 'x' coordinates."""
        return self.rect.width / float(self.columns)

    @property
    def y_scale(self) -> float:
        """Get the scalar value for 'y' coordinates."""
        return self.rect.height / float(self.rows)

    def __call__(self, x: float, y: float) -> Point:
        """Get the true location of a point within this grid."""

        # Ensure the coordinates are within the sub-divisions.
        assert x <= self.columns
        assert y <= self.rows
        return self.rect.origin.translate(x * self.x_scale, y * self.y_scale)

    @property
    def points(self) -> Iterable[Point]:
        """Iterate over points in the grid."""
        for row in range(self.rows + 1):
            for col in range(self.columns + 1):
                yield self(col, row)

    def box(self, x: float, y: float) -> Rectangle:
        """Get a rectangle object from provided coordinates."""
        return Rectangle.create(self.x_scale, self.y_scale, self(x, y))

    @property
    def boxes(self) -> Iterable[Rectangle]:
        """Iterate over boxes belonging to this grid."""
        for row in range(self.rows):
            for col in range(self.columns):
                yield self.box(col, row)

    @property
    def enumerate_boxes(self) -> Iterable[tuple[RectangleIndex, Rectangle]]:
        """Iterate over boxes belonging to this grid."""
        for row in range(self.rows):
            for col in range(self.columns):
                yield RectangleIndex(col, row), self.box(col, row)

    def adjust(
        self, columns: int = None, rows: int = None, rect: Rectangle = None
    ) -> "RectangleGrid":
        """Create a new grid from new parameters."""
        if columns is None:
            columns = self.columns
        if rows is None:
            rows = self.rows
        if rect is None:
            rect = self.rect
        return RectangleGrid(rect, columns, rows)

    def translate(
        self, dx: Translation | float, *args, **kwargs
    ) -> "RectangleGrid":
        """Translate this rectangle grid."""

        return RectangleGrid(
            self.rect.translate(dx, *args, **kwargs), self.columns, self.rows
        )
