"""
svgen - Test the 'svgen.color.hsl' module.
"""

# module under test
from svgen.cartesian.angle import DegreePrimitive
from svgen.color import Color
from svgen.color.hsl import Hsl, PercentPrimitive, hsl, hsla
from svgen.color.resolve import get_color


def test_hsl_basic():
    """Test basic functionality of hsl colors."""

    color = hsl(0, 1.0, 0.5)
    assert color.hue == 0 and color.hue == DegreePrimitive(360)
    assert str(color) == "hsl(0, 100%, 50%)"
    assert Hsl.from_ctor(str(color)) == color

    prim = PercentPrimitive(50)
    assert prim == prim.arc(count=2, divisor=1)


def test_hsl_animate():
    """Test animating properties."""

    assert get_color(color="white", lightness=0) == get_color()

    color = Color.from_ctor("hsla(0, 50%, 50%, 0.5)")

    assert color.animate(
        hue=180, saturation=0.25, lightness=0.75, alpha=0.25
    ) == Color.from_ctor("hsla(180, 25%, 75%, 0.25)")

    assert color.animate(
        hue=90, saturation=-0.25, lightness=0.25, alpha=0.25, delta=True
    ) == Color.from_ctor("hsla(90, 25%, 75%, 0.75)")

    assert color.animate() == color


def test_hsla_basic():
    """Test hsl colors with an alpha value."""

    color = hsla(0, 1.0, 0.5, 0.25)
    assert color == Hsl.from_ctor(str(color))
