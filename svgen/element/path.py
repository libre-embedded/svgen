"""
A module implementing a path element.
"""

# built-in
from enum import StrEnum
from typing import Any

# internal
from svgen.attribute.viewbox import ViewBox
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import Point
from svgen.color.resolve import get_color
from svgen.element import Element


class Path(Element):
    """A path element."""

    @staticmethod
    def create(*cmds: str, **kwargs) -> "Path":
        """A helper for creating path elements."""
        return Path(d=" ".join(cmds), **kwargs)


class PathCmd(StrEnum):
    """An enumeration of svg path commands."""

    MOVE = "M"
    LINE = "L"


class PathBuilder:
    """A class implementing a path building interface."""

    def __init__(self) -> None:
        """Initialize this instance."""
        self.cmds: list[str] = []

    def close(self) -> None:
        """Close the current path."""
        self.cmds.append("Z")

    def horizontal(self, count: float, relative: bool = True) -> None:
        """Issue a horizontal command."""
        cmd = "h"
        if not relative:
            cmd = cmd.upper()
        self.cmds.append(f"{cmd} {count}")

    def vertical(self, count: float, relative: bool = True) -> None:
        """Issue a vertical command."""
        cmd = "v"
        if not relative:
            cmd = cmd.upper()
        self.cmds.append(f"{cmd} {count}")

    def point(self, point: Point, cmd: PathCmd) -> None:
        """Issue a point-based command."""
        self.cmds.append(f"{cmd} {point.x} {point.y}")

    def translation(self, translation: Translation, cmd: PathCmd) -> None:
        """Issue a translation-based command."""
        self.cmds.append(f"{cmd.lower()} {translation.dx} {translation.dy}")

    def path(self, **kwargs) -> Path:
        """Get a path element based on this builder's state."""
        return Path.create(*self.cmds, **kwargs)


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
