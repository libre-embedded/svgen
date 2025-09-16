"""
svgen - Test the 'svgen.color' module.
"""

# module under test
from svgen.color import Color
from svgen.color.hsl import Hsl
from svgen.color.resolve import get_color
from svgen.color.rgb import Rgb


def test_color_basic():
    """Test basic color interactions."""

    assert Color.from_ctor("rgb(0, 0, 0)") == Color.from_ctor("hsl(0, 0%, 0%)")
    assert get_color(color="aliceblue") == Color.from_hex("#f0f8ff")
    assert Color.from_ctor("#f0f8ff") == Color.from_hex("#f0f8ff")

    assert Color.create(Hsl.from_ctor("hsl(0, 0%, 0%)")) == "#000000"
    assert Color.create(Rgb.from_ctor("rgb(0, 0, 0)")) == "#000000"

    assert Color.from_ctor("hsl(0, 0%, 0%)").hsl_arc(
        hue_divisor=2,
        saturation_count=0,
        lightness_count=0,
    ) == Color.from_ctor("hsl(180, 0%, 0%)")
