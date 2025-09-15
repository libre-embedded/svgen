"""
svgen - Common interfaces for rgb colors. See also:

        https://www.w3schools.com/colors/colors_rgb.asp
"""

# built-in
from typing import NamedTuple

# internal
from svgen.color.alpha import DEFAULT, Alpha, Alphalike
from svgen.color.numbers import parse_ctor


class RgbPrimitive(int):
    """An integer type for rgb values."""

    def __new__(cls, val: int) -> "RgbPrimitive":
        """Create a new primitive value for an rgb color."""

        val = max(val, 0)
        val = min(val, 255)
        return super().__new__(cls, val)

    def __str__(self) -> str:
        """Get this color value as a hex string."""
        return f"{int(self):02X}"

    @property
    def ratio(self) -> float:
        """Get this color as a ratio between 0 and 1."""
        return float(self) / 255.0


class Rgb(NamedTuple):
    """A definition of an rgb color."""

    red: RgbPrimitive
    green: RgbPrimitive
    blue: RgbPrimitive
    alpha: Alpha = DEFAULT

    def animate(
        self,
        red: int = None,
        green: int = None,
        blue: int = None,
        alpha: float = None,
        delta: bool = False,
    ) -> "Rgb":
        """Animate a color."""

        if red is None:
            red = self.red
        elif delta:
            red = self.red + red

        if green is None:
            green = self.green
        elif delta:
            green = self.green + green

        if blue is None:
            blue = self.blue
        elif delta:
            blue = self.blue + blue

        if alpha is None:
            alpha = self.alpha
        elif delta:
            alpha = self.alpha + alpha

        return rgba(red, green, blue, alpha)

    def __str__(self) -> str:
        """Get this color as a hex string."""

        result = f"#{self.red}{self.green}{self.blue}"

        # Add the alpha contents if relevant.
        if self.alpha != DEFAULT:
            result += self.alpha.hex_str
        return result

    @property
    def rgb(self) -> str:
        """Get this color as an 'rgb' constructor."""
        return f"rgb({int(self.red)}, {int(self.green)}, {int(self.blue)})"

    @property
    def rgba(self) -> str:
        """Get this color as an 'rgba' constructor."""
        return (
            f"rgba({int(self.red)}, {int(self.green)}, "
            f"{int(self.blue)}, {self.alpha})"
        )

    @staticmethod
    def from_hex(value: str) -> "Rgb":
        """Get an rgb color from a hex string."""

        value = value.strip()
        if value.startswith("#"):
            value = value[1:]

        assert len(value) == 6 or len(value) == 8, value

        # Parse the alpha value if present.
        alpha = DEFAULT
        if len(value) == 8:
            alpha = Alpha(value[6:8])

        return Rgb(
            RgbPrimitive(int(value[0:2], 16)),
            RgbPrimitive(int(value[2:4], 16)),
            RgbPrimitive(int(value[4:6], 16)),
            alpha,
        )

    @staticmethod
    def from_ctor(value: str) -> "Rgb":
        """Get an rgb color from a constructor string."""

        colors = parse_ctor(value, "rgb", "a")
        assert len(colors) == 3 or len(colors) == 4

        # Parse the alpha value if present.
        alpha = DEFAULT
        if len(colors) == 4:
            alpha = Alpha(colors[3])

        return Rgb(
            RgbPrimitive(int(colors[0])),
            RgbPrimitive(int(colors[1])),
            RgbPrimitive(int(colors[2])),
            alpha,
        )


def rgb(red: int, green: int, blue: int) -> Rgb:
    """Create a new RGB color."""
    return Rgb(RgbPrimitive(red), RgbPrimitive(green), RgbPrimitive(blue))


def rgba(red: int, green: int, blue: int, alpha: Alphalike) -> Rgb:
    """Create a new RGB color with a transparency value."""

    return Rgb(
        RgbPrimitive(red),
        RgbPrimitive(green),
        RgbPrimitive(blue),
        Alpha(alpha),
    )
