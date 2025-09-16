"""
svgen - Test the 'element.circle' module.
"""

# third-party
from pytest import approx

# module under test
from svgen.attribute.viewbox import ViewBox
from svgen.cartesian.circle import Circle as CartCircle
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import DEFAULT_CENTER, Point, to_center
from svgen.element.circle import Circle


def test_circle_basic():
    """Test the circle interface."""

    circle = Circle(CartCircle(5.0))
    assert circle.raw.attrs.radius_val == approx(5)
    assert Circle.create(Point(), 5.0, color="blue") == circle


def test_circle_centered():
    """Test that a circle centered in a viewBox is created correctly."""

    # Test a full-scale circle.
    box = ViewBox(0, 0, 100, 100)
    circle = Circle.centered(box, color="blue")
    assert circle.raw.radius == approx(50)
    assert circle.raw.center == Point(50, 50)

    # Test a translated circle.
    circle = Circle.centered(
        box, radius_scale=0.5, translation={"dx": 25, "dy": 25}
    )
    assert circle.raw.radius == approx(25)
    assert circle.raw.center == Point(75, 75)

    # Test a half-scale circle.
    circle = Circle.centered(box, 0.5)
    assert circle.raw.radius == approx(25)
    assert circle.raw.center == Point(50, 50)

    # Test a non-square viewBox.
    box = ViewBox(0, 0, 100, 50)
    circle = Circle.centered(box)
    assert circle.raw.radius == approx(25)
    assert circle.raw.center == Point(50, 25)
    assert circle.raw.center == Point(50, 25)


def test_circle_mutate():
    """Test the correctness of various circle mutations."""

    circle = Circle(CartCircle(5.0))
    assert circle.center == DEFAULT_CENTER
    assert circle.radius == approx(5)

    # Scale the circle.
    assert circle.scale(0.5) == Circle(CartCircle(2.5))

    # Move the circle.
    assert circle.translate(Translation(1.0, 1.0)) == Circle(
        CartCircle(5.0, to_center(Point(1.0, 1.0)))
    )

    # pylint: disable=unnecessary-dunder-call
    assert circle.raw.__eq__(5) is NotImplemented
    assert circle.__eq__(5) is NotImplemented
