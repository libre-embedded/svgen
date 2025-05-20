"""
A module for working with common display assets.
"""

# built-in
from math import isclose
from typing import Iterator, NamedTuple, Union

# internal
from svgen.attribute.viewbox import ViewBox

DEFAULT_DELIM = ":"


class AspectRatio(NamedTuple):
    """A class to storge a width and height ratio."""

    width: int
    height: int
    final: bool = False

    @property
    def square(self) -> bool:
        """Determine if this is a square aspect ratio."""
        return self.width == self.height

    def __str__(self) -> str:
        """Get this aspect ratio as a string."""
        return self.as_str()

    def as_str(self, delim: str = DEFAULT_DELIM) -> str:
        """Get this aspect ratio as a string."""
        return str(self.width) + delim + str(self.height)

    def __eq__(self, other) -> bool:
        """Determine if two aspect ratios are equivalent."""
        return isclose(self.over_height, other.over_height)

    @property
    def landscape(self) -> bool:
        """Determine if this ratio is landscape."""
        return self.width > self.height

    @property
    def portrait(self) -> bool:
        """Determine if this ratio is portrait."""
        return self.height > self.width

    def rotate(self) -> "AspectRatio":
        """Get this aspect ratio rotated."""
        return AspectRatio(self.height, self.width, self.final)

    @property
    def over_height(self) -> float:
        """Express this ratio as one of width over height."""
        return float(self.width) / float(self.height)

    @staticmethod
    def create(wxh: str, delim: str = DEFAULT_DELIM) -> "AspectRatio":
        """Create an aspect ration from a string."""
        parts = wxh.split(delim)
        return AspectRatio(int(parts[0].strip()), int(parts[1].strip()))

    @property
    def args(self) -> list[str]:
        """Get inkscape command-line arguments."""
        assert self.final
        return ["-w", str(self.width), "-h", str(self.height)]


COMMON_RATIOS = [
    "16:9",
    "16:10",
    "4:3",
    "5:4",
    "1:1",
    "256:135",
    "32:9",
    "21:9",
    "3:2",
    "4:1",
]
ICON_SIZES = [16, 24, 32, 64, 128, 256]
COMMON_SIZES = {
    "4:3": [AspectRatio(1024, 768, True), AspectRatio(1600, 1200, True)],
    "5:4": [AspectRatio(1280, 1024, True)],
    "3:2": [AspectRatio(2160, 1440, True), AspectRatio(2560, 1700, True)],
    "16:10": [
        AspectRatio(1280, 800, True),
        AspectRatio(1920, 1200, True),
        AspectRatio(2880, 1800, True),
    ],
    "16:9": [
        AspectRatio(1280, 720, True),
        AspectRatio(1366, 768, True),
        AspectRatio(1920, 1080, True),
        AspectRatio(2560, 1440, True),
    ],
    "17:9": [AspectRatio(4096, 2160, True)],
    "21:9": [AspectRatio(2560, 1080, True), AspectRatio(3440, 1440, True)],
    "32:9": [AspectRatio(3840, 1080, True), AspectRatio(5120, 1440, True)],
    "1:1": [
        AspectRatio(400, 400, True),
        AspectRatio(512, 512, True),
        AspectRatio(1024, 1024, True),
        AspectRatio(1920, 1920, True),
    ],
    # GitHub social preview.
    "2:1": [AspectRatio(1280, 640, True)],
    "4:1": [
        AspectRatio(17280, 4320, True),
        AspectRatio(1600, 400, True),
        AspectRatio(1584, 396, True),
    ],
    # Twitter banner.
    "3:1": [AspectRatio(1500, 500, True)],
    # 14-inch Macbook Pro monitor.
    "189:124": [AspectRatio(3024, 1984, True)],
    # Facebook banner.
    "205:78": [AspectRatio(820, 312, True)],
    # Buy me a Coffee banner.
    "2560:423": [AspectRatio(2560, 423, True)],
    # Twitch banner.
    "1200:480": [AspectRatio(1200, 480, True)],
    # Google admin logo.
    "80:33": [AspectRatio(320, 132, True)],
}
COMMON_SIZES["1:1"].extend(AspectRatio(x, x, True) for x in ICON_SIZES)


def common_sizes(
    ratio: Union[str, AspectRatio, ViewBox],
) -> Iterator[AspectRatio]:
    """Iterate over common sizes for a given aspect ratio."""

    if isinstance(ratio, ViewBox):
        ratio = AspectRatio(ratio.width, ratio.height)
    if not isinstance(ratio, AspectRatio):
        ratio = AspectRatio.create(ratio)

    # Look for a ratio equivalent to a known one and iterate over sizes.
    for common, sizes in COMMON_SIZES.items():
        candidates = [AspectRatio.create(common)] + sizes

        # Attempt to match to a common aspect ratio.
        for candidate in candidates:
            found = False
            if candidate == ratio:
                yield from sizes
                found = True
                break

            # Check if this is a rotated version of this common ratio.
            if not found and candidate.rotate() == ratio:
                for size in sizes:
                    yield size.rotate()
