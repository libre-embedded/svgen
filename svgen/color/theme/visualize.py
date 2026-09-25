"""
A module for visualizing color themes.
"""

# built-in
from collections.abc import Iterator

# internal
from svgen.cartesian.rectangle import Rectangle
from svgen.cartesian.rectangle.grid import RectangleGrid
from svgen.color.theme import ColorTheme
from svgen.color.theme.manager import THEMES, ColorThemeManager
from svgen.element.rect import Rect


def visualize_theme(
    theme: ColorTheme | str, rect: Rectangle, columns: bool = True
) -> Iterator[Rect]:
    """
    Create filled rectangle elements for this theme inside another
    rectangle.
    """

    # Allow a theme to be specified as a string name.
    if isinstance(theme, str):
        theme = THEMES.data[theme]

    assert isinstance(theme, ColorTheme)
    for box, color in zip(
        RectangleGrid(
            rect, theme.size if columns else 1, 1 if columns else theme.size
        ).boxes,
        theme.data.values(),
    ):
        curr = Rect(box)
        curr.assign_fill_color(color)
        yield curr


def visualize(
    rect: Rectangle, manager: ColorThemeManager = None, columns: bool = True
) -> Iterator[Rect]:
    """Visualize all managed themes within a provided rectangle."""

    if manager is None:
        manager = THEMES

    for box, theme in zip(
        RectangleGrid(rect, 1, manager.size).boxes, manager.data.values()
    ):
        if theme is not None:
            yield from visualize_theme(theme, box, columns=columns)
