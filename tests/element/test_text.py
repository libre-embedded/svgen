"""
Test the 'element.text' module.
"""

from svgen.element.rect import Rect
from svgen.element.svg import Svg

# module under test
from svgen.element.text import Text


def test_text_basic():
    """Test basic text element scenarios."""

    rect = Rect.centered(Svg.app().viewbox)
    rect.assign_fill_color("blue")
    assert Text("Hello, world!", rect)
