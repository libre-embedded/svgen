"""
svgen - Common interfaces for hsl colors. See also:

        https://www.w3schools.com/colors/colors_hsl.asp
"""

# built-in
from typing import NamedTuple

# internal
from svgen.cartesian.angle import DegreePrimitive, Rotatable
from svgen.color.alpha import DEFAULT, Alpha
from svgen.color.numbers import parse_ctor


class PercentPrimitive(int, Rotatable):
    """A class for integer percentages."""

    def __new__(cls, val: int) -> "PercentPrimitive":
        """Create a new percentage value."""
        return super().__new__(cls, min(max(val, 0), 100))

    def __str__(self) -> str:
        """Get this percentage as a string."""
        return f"{int(self)}%"

    @property
    def ratio(self) -> float:
        """Get this percentage as a ratio between 0 and 1."""
        return float(self) / 100.0

    def arc(self, count: int = 1, divisor: int = 2) -> "PercentPrimitive":
        """Rotate this angle around the circle."""

        new_val = self + round(count * (100 / divisor))
        while new_val > 100:
            new_val -= 100

        return PercentPrimitive(new_val)


class Hsl(NamedTuple):
    """A definition of an hsl color."""

    hue: DegreePrimitive
    saturation: PercentPrimitive
    lightness: PercentPrimitive
    alpha: Alpha = DEFAULT

    def animate(
        self,
        hue: int = None,
        saturation: float = None,
        lightness: float = None,
        alpha: float = None,
        delta: bool = False,
    ) -> "Hsl":
        """Manipulate this color into a new one."""

        if hue is None:
            hue = self.hue
        elif delta:
            hue = self.hue + hue

        if saturation is None:
            saturation = self.saturation.ratio
        elif delta:
            saturation = self.saturation.ratio + saturation

        if lightness is None:
            lightness = self.lightness.ratio
        elif delta:
            lightness = self.lightness.ratio + lightness

        if alpha is None:
            alpha = self.alpha
        elif delta:
            alpha = self.alpha + alpha

        return hsla(hue, saturation, lightness, alpha)

    def arc(
        self,
        hue_count: int = 1,
        hue_divisor: int = 1,
        saturation_count: int = 1,
        saturation_divisor: int = 1,
        lightness_count: int = 1,
        lightness_divisor: int = 1,
    ) -> "Hsl":
        """Rotate this angle around the circle."""

        return Hsl(
            self.hue.arc(count=hue_count, divisor=hue_divisor),
            self.saturation.arc(
                count=saturation_count, divisor=saturation_divisor
            ),
            self.lightness.arc(
                count=lightness_count, divisor=lightness_divisor
            ),
            self.alpha,
        )

    def __str__(self) -> str:
        """Convert this hsl color to a string."""

        if self.alpha == DEFAULT:
            return f"hsl({self.hue}, {self.saturation}, {self.lightness})"
        return (
            f"hsla({self.hue}, {self.saturation}, "
            f"{self.lightness}, {self.alpha})"
        )

    @staticmethod
    def from_ctor(value: str) -> "Hsl":
        """Get an hsl color from a constructor string."""

        colors = parse_ctor(value, "hsl", "a")
        assert len(colors) == 3 or len(colors) == 4

        # Parse the alpha value if present.
        alpha = DEFAULT
        if len(colors) == 4:
            alpha = Alpha(float(colors[3]))

        colors[1] = colors[1].replace("%", "")
        colors[2] = colors[2].replace("%", "")
        return Hsl(
            DegreePrimitive(int(colors[0])),
            PercentPrimitive(int(colors[1])),
            PercentPrimitive(int(colors[2])),
            alpha,
        )


def hsl(hue: int, saturation: float, lightness: float) -> Hsl:
    """Create a new hsl color."""

    return Hsl(
        DegreePrimitive(hue),
        PercentPrimitive(round(saturation * 100.0)),
        PercentPrimitive(round(lightness * 100.0)),
    )


def hsla(hue: int, saturation: float, lightness: float, alpha: float) -> Hsl:
    """Create a new hsl color with a transparency value."""

    return Hsl(
        DegreePrimitive(hue),
        PercentPrimitive(round(saturation * 100.0)),
        PercentPrimitive(round(lightness * 100.0)),
        Alpha(alpha),
    )
