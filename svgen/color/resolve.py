"""
A module for resolving colors.
"""

# built-in
from contextlib import suppress

# internal
from svgen.color import Color, Colorlike
from svgen.color.theme.manager import THEMES, ColorThemeManager


def get_color(
    key: Colorlike = "black", manager: ColorThemeManager = None, **kwargs
) -> Color:
    """Resolve a color using the theme manager."""

    if manager is None:
        manager = THEMES

    color = manager[kwargs.get("color", key)].color
    with suppress(KeyError):
        del kwargs["color"]

    if kwargs:
        color = color.animate(**kwargs)

    return color
