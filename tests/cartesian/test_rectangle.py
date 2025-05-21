"""
Test the 'cartesian.rectangle' module.
"""

# module under test
from svgen.cartesian import Dimensions
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import Point
from svgen.cartesian.rectangle import Rectangle
from svgen.cartesian.rectangle.corner import CORNERS, CornerScalar


def test_dimensions_basic():
    """Test the 'Dimensions' class."""

    inst = Dimensions(1.0, 2.0)
    assert hash(inst)
    assert inst.dx == 1.0
    assert inst.dy == 2.0
    assert Translation(1.0, 0.0).rotate() == Translation(0.0, 1.0)


def test_rectangle_squaring():
    """Test scenarios where we attempt to square a rectangle."""

    rect = Rectangle.create(20, 10)
    new_rect = rect.from_center(square=True)
    assert new_rect == Rectangle.create(10, 10, Point(5, 0))
    assert new_rect.dimensions.to_square() == new_rect.dimensions


def test_rectangle_corner_basic():
    """Test functionality of rectangle corners."""

    assert CORNERS["tl"].on_top
    assert CORNERS["bl"].on_bottom
    assert CORNERS["bl"].on_left
    assert CORNERS["br"].on_right

    assert CORNERS["tl"].vertical
    assert CORNERS["bl"].horizontal

    rect = Rectangle.create(10.0, 10.0)
    assert rect.top_left == Point(0.0, 0.0)
    assert rect.top_right == Point(10.0, 0.0)
    assert rect.bottom_left == Point(0.0, 10.0)
    assert rect.bottom_right == Point(10.0, 10.0)

    assert rect.contains(Point(5.0, 5.0))
    assert not rect.contains(Point(15.0, 5.0))
    assert not rect.contains(Point(5.0, 15.0))

    assert CORNERS["tl"].vector_dx == 0.0
    assert CORNERS["tl"].vector_dy == 1.0

    assert CornerScalar(Translation(), Translation()) == CornerScalar(
        Translation(), Translation()
    )
