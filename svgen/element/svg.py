"""
svgen - A module for the 'svg' element.
"""

# third-party
from vcorelib.dict import GenericStrDict

# internal
from svgen.attribute import XMLNS, Attribute
from svgen.attribute.viewbox import ViewBox
from svgen.config import initialize_config
from svgen.element import Element
from svgen.element.path import compose_borders
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

    @staticmethod
    def app(config: GenericStrDict = None) -> "Svg":
        """Get an application SVG document."""

        if config is None:
            config = {}
        initialize_config(config)
        doc = Svg(ViewBox.from_dict(config))

        add_background_grid(doc, config["background"], config["grid"])
        if "border" in config:
            doc.children.extend(compose_borders(doc.viewbox, config["border"]))
        if "opacity" in config:
            doc["opacity"] = config["opacity"]

        return doc


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
        elem = Rect.centered(
            svg.viewbox,
            color=background["color"],
            prop=background.get("property", "fill"),
        )

        opacity = background.get("opacity", None)
        if opacity is not None:
            elem["fill-opacity"] = opacity

        to_add.append(elem)

    # Add any new children to the beginning of the document.
    svg.children = to_add + svg.children
