"""
Test the 'element.path' module.
"""

# moduler under test
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import Point
from svgen.element.path import PathBuilder, PathCmd


def test_path_builder_basic():
    """Test basic path building."""

    builder = PathBuilder()
    builder.point(Point(10, 10), PathCmd.MOVE)
    builder.point(Point(20, 20), PathCmd.LINE)
    builder.translation(Translation(-10, -10), PathCmd.MOVE)
    builder.translation(Translation(5, 5), PathCmd.LINE)

    builder.horizontal(10.0)
    builder.horizontal(10.0, relative=False)

    builder.vertical(20.0)
    builder.vertical(20.0, relative=False)

    builder.close()

    assert builder.path()
