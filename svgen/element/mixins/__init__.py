"""
A module implementing svg element mixin classes.
"""

# built-in
from collections.abc import Iterator

# internal
from svgen.attribute import Attribute, SimpleAttribute
from svgen.cartesian.rectangle import Rectangle
from svgen.color import Color, Colorlike
from svgen.element import Element


class RectangularMixin:
    """A class mixin for rectangular entities."""

    has_dimensions = True

    def __init__(self, rect: Rectangle) -> None:
        """Initialize this instance."""

        self.rect = rect
        self.location = self.rect.location
        self.dimensions = self.rect.dimensions

    @property
    def rect_attributes(self) -> Iterator[Attribute]:
        """Get attributes for this instance."""

        yield from self.location.attrs
        if self.has_dimensions:
            yield from self.dimensions.attrs


class RadiusXyMixin:
    """A class mixin for entities with 'rx' and 'ry' attributes."""

    def __init__(self, rx: float = 0.0, ry: float = 0.0) -> None:
        """Initialize this instance."""

        self.rx = rx
        self.ry = ry

    @property
    def radius_xy_attributes(self) -> Iterator[Attribute]:
        """Get attributes for this instance."""

        yield SimpleAttribute("rx", str(self.rx))
        yield SimpleAttribute("ry", str(self.ry))


class FillColorMixin(Element):
    """A mixin class for elements with a 'fill' color attribute."""

    _fill_color: Color | None = None

    @property
    def has_fill_color(self) -> bool:
        """Determine if this instance has a fill color."""
        return self._fill_color is not None

    @property
    def fill_color(self) -> Color:
        """Get the fill color for this instance."""
        assert self._fill_color is not None, "No fill color for this element!"
        return self._fill_color

    def assign_fill_color(self, data: Colorlike) -> None:
        """Assign a fill color for this instance."""

        assert not self.has_fill_color, (self._fill_color, data)
        self._fill_color = Color.create(data)
        self.style.add_color(self.fill_color, "fill")
