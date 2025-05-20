"""
svgen - A module for the 'svg' element.
"""

# third-party
from vcorelib.dict import GenericStrDict

# internal
from svgen.attribute import XMLNS, Attribute
from svgen.attribute.viewbox import ViewBox
from svgen.element import Element
from svgen.element.rect import Rect


class Svg(Element):
    """A class for svg elements."""

    def __init__(
        self, viewbox: ViewBox, document: bool = True, **extra
    ) -> None:
        """Construct a new svg element (or document)."""

        self.viewbox = viewbox
        attrs: list[Attribute] = [self.viewbox]
        if document:
            attrs.append(XMLNS)
        super().__init__(attrib=attrs, **extra)


def add_background_grid(
    svg: Svg, background: GenericStrDict, grid: GenericStrDict
) -> None:
    """
    Add background and grid objects to an svg element, if they're specified
    in their respective configurations.
    """

    del grid

    to_add: list[Element] = []

    # Add a colored background rectangle, if at least 'color' is specified.
    if "color" in background:
        to_add.append(
            Rect.centered(
                svg.viewbox,
                color=background["color"],
                prop=background.get("property", "fill"),
            )
        )

    # Add any new children to the beginning of the document.
    svg.children = to_add + svg.children
