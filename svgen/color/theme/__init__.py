"""
A module for working with color themes.
"""

# built-in
from collections import UserDict
from collections.abc import Mapping
from typing import MutableMapping, NamedTuple, Optional, cast

# third-party
from vcorelib.dict import GenericStrDict
from vcorelib.io import ARBITER, DEFAULT_INCLUDES_KEY
from vcorelib.namespace import Namespace, NamespaceMixin
from vcorelib.paths import Pathlike, normalize

# internal
from svgen.color import Color, Colorlike

ColorTokens = dict[str, Color]


class ColorToken(NamedTuple):
    """A simple pairing of a color with a token."""

    token: str
    color: Color

    def __eq__(self, other) -> bool:
        """Determine if a color token is equivalent to something else."""
        if hasattr(other, "color"):
            other = other.color
        return bool(self.color == other)

    def __str__(self) -> str:
        """Get this token as a color string."""
        return str(self.color)

    @staticmethod
    def create(key: Colorlike) -> "ColorToken":
        """Create a color token from a color."""
        return ColorToken(str(key), Color.create(key))


class ColorTheme(
    UserDict,  # type: ignore
    NamespaceMixin,
    MutableMapping[str, Color],
):
    """A class implementing a theme color interface."""

    data: ColorTokens

    def __init__(
        self,
        name: str,
        initialdata: dict[str, Colorlike] = None,
        namespace: Namespace = None,
    ) -> None:
        """Initialize this color theme."""

        NamespaceMixin.__init__(self, namespace=namespace)

        self.name = name
        self.push_name(name)

        if initialdata is None:
            initialdata = {}

        # Ensure we're storing real color objects.
        UserDict.__init__(
            self,
            {
                self.namespace(key): Color.create(val)
                for key, val in initialdata.items()
            },
        )

    def lookup(self, key: str) -> tuple[str, Optional[Color]]:
        """Attempt to find an existing color in this theme by key."""

        result = None
        token = key

        # Always check the current namespace first.
        namespaced = self.namespace(key)

        if namespaced in self.data:
            result = self.data[namespaced]
            token = namespaced

        # Check the global namespace.
        elif key in self.data:
            result = self.data[key]

        return token, result

    def __getitem__(self, key: str) -> Color:
        """Get a color from this theme."""
        key, _ = self.lookup(key)
        return self.data[key]

    def resolve(self, key: str, strict: bool = False) -> ColorToken:
        """Attempt to resolve a color key as a theme color."""

        token, color = self.lookup(key)
        if color is None:
            assert not strict, f"Can't resolve key '{key}' as a color!"
            color = Color.from_ctor(key)
        return ColorToken(token, color)

    def create(self, color: Colorlike) -> Color:
        """
        Attempt to create a color through this theme so that existing tokens
        can be used as color aliases.
        """

        if isinstance(color, str):
            _, color = self.resolve(color)
            if color is not None:
                return color

        return Color.create(color)

    def add(self, key: str, color: Colorlike) -> ColorToken:
        """Add a new color to this theme."""

        namespaced = self.namespace(key)
        color = self.create(color)
        if namespaced in self:
            assert self.data[namespaced] == color, (
                f"Can't add over color '{namespaced}'! "
                f"{self.data[namespaced]} != {color}"
            )
        else:
            self.data[namespaced] = color
        return ColorToken(namespaced, color)

    def add_mapping(self, data: GenericStrDict) -> None:
        """Add a mapping of tokens and colors to this theme."""

        for key, val in data.items():
            key = str(key)
            # Ensure that we recurse into dictionaries.
            if isinstance(val, Mapping):
                with self.names_pushed(key):
                    self.add_mapping(cast(GenericStrDict, val))
            else:
                # Add leaf nodes as actual colors.
                self.add(key, val)

    @staticmethod
    def from_path(path: Pathlike) -> "ColorTheme":
        """Load a color theme from a data file on disk."""

        path = normalize(path)
        assert path.is_file(), f"No file '{path}'!"

        theme = ColorTheme(path.with_suffix("").name)
        theme.add_mapping(
            ARBITER.decode(
                path, includes_key=DEFAULT_INCLUDES_KEY, require_success=True
            ).data
        )
        return theme

    @property
    def size(self) -> int:
        """Get the number of colors in this theme."""
        return len(self.data.keys())
