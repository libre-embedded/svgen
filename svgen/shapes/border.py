"""
A module implementing interfaces for adding borders to SVG documents.
"""

# built-in
from typing import Any

# third-party
from svgen.attribute.viewbox import ViewBox
from svgen.color.resolve import get_color
from svgen.element import Element
from svgen.element.path import PathBuilder, PathCmd


def compose_borders(viewbox: ViewBox, config: dict[str, Any]) -> list[Element]:
    """An example function for composing a document."""

    builder = PathBuilder()
    builder.point(viewbox.box.top_left, PathCmd.MOVE)

    builder.horizontal(viewbox.width)
    builder.vertical(viewbox.height)
    builder.horizontal(-viewbox.width)
    builder.close()

    data = {
        "fill": "none",
        "stroke-width": config.get("stroke_width", 2),
        "stroke": get_color(config["color"]),
    }
    if "opacity" in config:
        data["stroke-opacity"] = config["opacity"]

    return [builder.path(attrib=data)]
