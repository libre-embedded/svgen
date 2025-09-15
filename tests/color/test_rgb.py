"""
svgen - Test the 'svgen.color.rgb' module.
"""

# built-in
from math import isclose

# module under test
from svgen.color import Color
from svgen.color.numbers import css_number_to_ratio
from svgen.color.rgb import Rgb, rgb, rgba


def test_rgb_animate():
    """Test basic functionality of rgb color animation."""

    color = Color.from_ctor("rgba(50, 50, 50, 0.5)")
    assert color.animate() == color
    assert color.animate(red=color.rgb.red) == color
    assert color.animate(blue=color.rgb.blue) == color
    assert color.animate(green=color.rgb.green) == color

    assert color.animate(
        red=25, green=25, blue=25, alpha=0.25
    ) == Color.from_ctor("rgba(25, 25, 25, 0.25")

    assert color.animate(
        red=25, green=25, blue=25, alpha=0.25, delta=True
    ) == Color.from_ctor("rgba(75, 75, 75, 0.75")


def test_rgb_basic():
    """Test basic functionality of rgb colors."""

    color = rgb(256, 256, 256)
    assert color.red == 255
    assert color.green == 255
    assert color.blue == 255
    assert str(color.red) == "FF"
    assert str(color) == "#FFFFFF"
    assert color.rgb == "rgb(255, 255, 255)"
    assert Rgb.from_hex(str(color)) == color
    assert Rgb.from_ctor(color.rgb) == color


def test_rgba_basic():
    """Test rgb colors with an alpha value."""

    assert rgb(256, 256, 256) == rgba(255, 255, 255, 1.0)
    assert rgba(255, 255, 255, "50%").alpha == 0.5

    color = rgba(128, 128, 128, 0.25)

    # pylint: disable=unnecessary-dunder-call
    assert color.alpha.__eq__(5) is NotImplemented
    # pylint: enable=unnecessary-dunder-call

    assert Rgb.from_ctor("rgba(128, 128, 128, 25%)") == color
    assert Rgb.from_ctor("rgba(128, 128, 128, 26%)") != color
    assert color.rgba == "rgba(128, 128, 128, 0.25)"

    assert Rgb.from_hex("#80808040") == color
    assert color.alpha.hex_str == "3F"
    assert Rgb.from_hex(str(color)) == color

    assert isclose(css_number_to_ratio(255), 1.0)
