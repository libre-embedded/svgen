"""
A module for adding pin elements to circuit chips.
"""

# internal
from svgen.cartesian.rectangle.corner import BL, BR, TL, TR, RectangleCorner
from svgen.element import Element
from svgen.element.rect import Rect


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

    translate_x_map = {
        TL: -(width / 2.0),
        TR: -(2.0 * height),
        BL: height,
        BR: -(width / 2.0),
    }
    translate_y_map = {
        TL: height,
        TR: -(width / 2.0),
        BL: -(width / 2.0),
        BR: -height * 2.0,
    }

    for corner in RectangleCorner:
        curr_width = width if corner.vertical else height
        curr_height = height if corner.vertical else width

        curr = rect.corner(corner).translate(
            translate_x_map[corner], translate_y_map[corner]
        )

        for _ in range(count):
            new_rect = Rect.create(
                curr_width, curr_height, curr, rx=radius, ry=radius
            )
            new_rect.style.add_color(color, "fill")
            result.append(new_rect)

            curr = curr.translate(
                pin_spacing * corner.vector_dx, pin_spacing * corner.vector_dy
            )

    return result
