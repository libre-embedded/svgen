"""
A module for adding pin elements to circuit chips.
"""

# built-in
from typing import Iterator

# internal
from svgen.cartesian.point import Point
from svgen.cartesian.rectangle.corner import BL, BR, TL, TR, RectangleCorner
from svgen.element import Element
from svgen.element.rect import Rect


def translate_maps(
    width: float, height: float
) -> tuple[
    dict[RectangleCorner, float | int], dict[RectangleCorner, float | int]
]:
    """Get translation mappings for x/y based on rectangle corner."""

    return {
        TL: -(width / 2.0),
        TR: -(2.0 * height),
        BL: height,
        BR: -(width / 2.0),
    }, {
        TL: height,
        TR: -(width / 2.0),
        BL: -(width / 2.0),
        BR: -height * 2.0,
    }


def corners_translated(
    rect: Rect, width: float, height: float
) -> Iterator[tuple[RectangleCorner, Point]]:
    """Iterate over corners and translate the origin point."""

    translate_x_map, translate_y_map = translate_maps(width, height)
    for corner in RectangleCorner:
        yield corner, rect.corner(corner).translate(
            translate_x_map[corner], translate_y_map[corner]
        )


def add_pins(rect: Rect, count: int, color: str) -> list[Element]:
    """Add some number of pins to a rectangle."""

    assert rect.square

    result: list[Element] = []

    width = rect.width / 3.0
    height = (width / count) * 3 / 2
    radius = height / 2.0

    pin_spacing = (
        (rect.width - (2 * height) - (height * count)) / (count - 1)
    ) + height

    for corner, curr in corners_translated(rect, width, height):
        for _ in range(count):
            new_rect = Rect.create(
                width if corner.vertical else height,
                height if corner.vertical else width,
                curr,
                rx=radius,
                ry=radius,
            )
            new_rect.style.add_color(color, "fill")
            result.append(new_rect)

            curr = curr.translate(
                pin_spacing * corner.vector_dx, pin_spacing * corner.vector_dy
            )

    return result
