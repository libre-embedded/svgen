"""
Test the 'shapes.chip' module.
"""

# module under test
from svgen.cartesian.rectangle import Rectangle
from svgen.shapes.chip import add_chip, add_outline_chip


def test_shapes_add_chip_basic():
    """Test basic functionality of adding chip elements."""

    assert add_chip(
        Rectangle.create(100, 100), circle_color="blue", debug=True
    )

    assert add_outline_chip(
        Rectangle.create(100, 100), circle_color="blue", debug=True
    )
