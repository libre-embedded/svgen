"""
sample - A test script for composing an SVG document.
"""

# built-in

# internal
from svgen.attribute.viewbox import ViewBox
from svgen.element import Element


def compose(viewbox: ViewBox, config: dict) -> list[Element]:
    """An example function for composing a document."""

    print(viewbox)
    print(config)
    return []
