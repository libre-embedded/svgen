"""
Test the 'cartesian.point' module.
"""

# module under test
from svgen.cartesian.point import Point


def test_point_polar():
    """Test polar point translations."""

    origin = Point()
    assert origin.polar(0) == Point(1, 0)
    assert origin.polar(90) == Point(0, 1)
    assert origin.polar(90, ccw=False) == Point(0, -1)
