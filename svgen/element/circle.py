"""
svgen - A module for the 'circle' element.
"""

# built-in
from typing import Union

# internal
from svgen.attribute import PossibleAttributes, attributes
from svgen.attribute.viewbox import ViewBox
from svgen.cartesian import UNITY
from svgen.cartesian.circle import Circle as CartCircle
from svgen.cartesian.mutate import Translation
from svgen.cartesian.point import Point, to_center
from svgen.cartesian.rectangle import Rectangle
from svgen.color import Colorlike
from svgen.element import Element


class Circle(Element):
    """A class for circle elements."""

    def __init__(
        self, circle: CartCircle, attrs: PossibleAttributes = None, **extra
    ) -> None:
        """Construct a new circle element."""

        self.raw = circle
        assert self.raw.center.center

        real_attrs = attributes(attrs)
        real_attrs.append(self.raw.radius_attr)
        real_attrs += [*self.raw.center_attrs]

        super().__init__(attrib=real_attrs, **extra)

    def translate(self, move: Translation) -> "Circle":
        """Move this circle by a given translation."""
        return Circle(self.raw.translate(move))

    def scale(self, scale: float = UNITY) -> "Circle":
        """Scale this circle's radius."""
        return Circle(self.raw.scale(scale))

    @property
    def radius(self) -> float:
        """Get this circle's radius."""
        return self.raw.radius

    @property
    def center(self) -> Point:
        """Get this circle's center."""
        return self.raw.center

    def __eq__(self, other: object) -> bool:
        """Determine if this circle is equivalent to another."""

        if not isinstance(other, Circle):
            return NotImplemented
        return self.raw == other.raw

    @staticmethod
    def create(
        center: Point,
        radius: float,
        color: Colorlike = None,
        prop: str = "fill",
        **kwargs,
    ) -> "Circle":
        """Create a circle from a point and radius."""

        result = Circle(CartCircle(radius, center.to_center()), **kwargs)
        if color is not None:
            result.style.add_color(color, prop)
        return result

    @staticmethod
    def centered(
        box: Union[ViewBox, Rectangle],
        radius_scale: float = UNITY,
        color: Colorlike = None,
        prop: str = "fill",
        **kwargs,
    ) -> "Circle":
        """
        From a viewBox, create a circle that is centered with an appropriately
        scaled radius.
        """

        # Compute everything from an actual rectangle instance.
        if isinstance(box, ViewBox):
            box = box.box

        radius = float(min(box.width, box.height)) / 2.0

        circ = CartCircle(radius, to_center(box.center)).scale(radius_scale)

        # Handle translation.
        if "translation" in kwargs and kwargs["translation"]:
            circ = circ.translate(Translation(**kwargs["translation"]))
            del kwargs["translation"]

        result = Circle(circ, **kwargs)

        if color is not None:
            result.style.add_color(color, prop)

        return result
