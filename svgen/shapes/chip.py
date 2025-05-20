"""
A module for adding circuit chips to SVG documents.
"""

# internal
from svgen.cartesian.rectangle import Rectangle
from svgen.element import Element
from svgen.element.circle import Circle
from svgen.element.rect import Rect
from svgen.shapes.pins import add_pins


def add_chip(
    box: Rectangle,
    body_color: str = "black",
    pin_color: str = "gray",
    circle_color: str = None,
    pin_count: int = 3,
    debug: bool = False,
) -> tuple[list[Element], Rect]:
    """
    Add a circuit chip to the document based on the provided rectangle and
    other configurations.
    """

    result: list[Element] = []

    has_circle = circle_color is not None

    body_ratio = 1 / 2 if has_circle else 3 / 4
    body_width = box.to_square(body_ratio).width

    # Add a circle behind the body.
    if has_circle:
        result.append(Circle.centered(box, color=circle_color))

    # Add the body.
    body = Rect.centered(
        box,
        body_ratio,
        body_ratio,
        body_color,
        rx=body_width / 6,
        ry=body_width / 6,
    )

    result += add_pins(body, pin_count, pin_color)
    result.append(body)

    # Add points for debugging.
    if debug:
        grid = body.grid(10, 10)
        for point in grid.points:
            result.append(Circle.create(point, 1.0, "orange"))

    return result, body
