"""
A module for adding circuit chips to SVG documents.
"""

# internal
from svgen.cartesian.rectangle import Rectangle
from svgen.color.resolve import get_color
from svgen.element import Element
from svgen.element.circle import Circle
from svgen.element.path import Path
from svgen.element.rect import Rect
from svgen.shapes.pins import add_pins, corners_translated


def add_outline_pins(  # pylint: disable=too-many-locals
    rect: Rect,
    count: int,
    color: str,
    stroke_width: int | float = 3.0,
) -> list[Element]:
    """Add some number of pins to a rectangle."""

    assert rect.square

    result: list[Element] = []

    h_stroke = stroke_width / 2.0

    width = rect.width / 3.0
    height = (width / count) * 3 / 2

    pin_spacing = (
        (rect.width - (2 * height) - (height * count)) / (count - 1)
    ) + height

    radius = (height / 2.0) - (h_stroke / 2.0)

    for corner, curr in corners_translated(rect, width, height):
        c_width = width if corner.vertical else height
        c_height = height if corner.vertical else width

        for _ in range(count):
            cmds = [
                f"M {curr.x} {curr.y}",
                f"m {h_stroke / 2.0} {h_stroke / 2.0}",
            ]

            if corner.vertical:
                # left pins
                if corner.on_left:
                    cmds += [
                        f"m {radius} 0",
                        f"h {(c_width / 2.0) - (h_stroke + radius)}",
                        f"m 0 {c_height - h_stroke}",
                        f"h -{(c_width / 2.0) - (h_stroke + radius)}",
                        f"a {radius} {radius} 0 0 1 -{radius} -{radius}",
                        f"a {radius} {radius} 0 0 1 {radius} -{radius}",
                    ]

                # right pins
                else:
                    cmds += [
                        f"m {(c_width / 2.0) - h_stroke} 0",
                        f"h {(c_width / 2.0) - (h_stroke + radius / 2.0)}",
                        f"m 0 {c_height - h_stroke}",
                        f"h -{(c_width / 2.0) - (h_stroke + radius / 2.0)}",
                        f"m {(c_width / 2.0) - (h_stroke + radius / 2.0)} 0",
                        f"a {radius} {radius} 0 0 0 {radius} -{radius}",
                        f"a {radius} {radius} 0 0 0 -{radius} -{radius}",
                    ]
            else:
                # top pins
                if corner.on_top:
                    cmds += [
                        f"m 0 {radius}",
                        f"m {c_width - h_stroke} 0",
                        f"v {(c_height / 2.0) - (h_stroke + radius)}",
                        f"m -{c_width - h_stroke} 0",
                        f"v -{(c_height / 2.0) - (h_stroke + radius)}",
                        f"a {radius} {radius} 0 0 1 {radius} -{radius}",
                        f"a {radius} {radius} 0 0 1 {radius} {radius}",
                    ]

                # bottom pins
                else:
                    cmds += [
                        f"m 0 {(c_height / 2.0) - h_stroke}",
                        f"m {c_width - h_stroke} 0",
                        f"v {(c_height / 2.0) - (h_stroke + radius / 2.0)}",
                        f"m -{c_width - h_stroke} 0",
                        f"v -{(c_height / 2.0) - (h_stroke + radius / 2.0)}",
                        f"m 0 {(c_height / 2.0) - (h_stroke + radius / 2.0)}",
                        f"a {radius} {radius} 0 0 0 {radius} {radius}",
                        f"a {radius} {radius} 0 0 0 {radius} -{radius}",
                    ]

            result.append(
                Path.create(
                    *cmds,
                    attrib={
                        "fill": "none",
                        "stroke": get_color(color),
                        "stroke-width": stroke_width,
                    },
                )
            )

            curr = curr.translate(
                pin_spacing * corner.vector_dx, pin_spacing * corner.vector_dy
            )

    return result


def add_outline_chip(
    box: Rectangle,
    pin_color: str = "gray",
    circle_color: str = None,
    pin_count: int = 3,
    debug: bool = False,
    stroke_width: int | float = 3.0,
) -> tuple[list[Element], Rect]:
    """
    Add a circuit chip to the document based on the provided rectangle and
    other configurations (outline variant).
    """

    result: list[Element] = []

    has_circle = circle_color is not None

    body_ratio = 1 / 2 if has_circle else 3 / 4
    body_width = box.to_square(body_ratio).width

    # Add a circle behind the body.
    if has_circle:
        assert circle_color is not None
        result.append(
            Circle.centered(
                box,
                attrs={
                    "stroke": get_color(circle_color),
                    "fill": "none",
                    "stroke-width": stroke_width,
                },
            )
        )

    # Add the body.
    body = Rect.centered(
        box,
        body_ratio,
        body_ratio,
        None,
        rx=body_width / 6,
        ry=body_width / 6,
    )

    result += add_outline_pins(body, pin_count, pin_color)
    result.append(body)

    if debug:
        result.extend(handle_debug(body))

    return result, body


def handle_debug(
    rect: Rect, count: int = 10, radius: float = 1.0
) -> list[Circle]:
    """Add points for debugging"""

    grid = rect.grid(count, count)
    result = []
    for point in grid.points:
        result.append(Circle.create(point, radius, "orange"))
    return result


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
        assert circle_color is not None
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

    if debug:
        result.extend(handle_debug(body))

    return result, body
