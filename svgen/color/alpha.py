"""
svgen - A module for working with alpha channels for colors.
"""

# built-in
from math import isclose
from typing import Self

# internal
from svgen.color.numbers import css_number_to_ratio

Alphalike = float | int | str


class Alpha(float):
    """A class describing the transparency of a color."""

    def __eq__(self, other: object) -> bool:
        """Determine if two alpha values are equal."""

        if not isinstance(other, Alpha):
            return NotImplemented
        return isclose(float(self), float(other), rel_tol=1e-4, abs_tol=0.005)

    def __new__(cls, val: Alphalike) -> Self:
        """From the provided value, get a ratio between 0.0 and 1.0."""

        return super().__new__(cls, css_number_to_ratio(val))

    @property
    def hex_str(self) -> str:
        """Convert this alpha value to a hex string."""

        return f"{int(float(self) * 255.0):X}"


# Provide a default that has no transparency.
DEFAULT = Alpha(1.0)
