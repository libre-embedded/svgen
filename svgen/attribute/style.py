"""
svgen - A module for the 'style' attribute.
"""

# built-in
from typing import NamedTuple, Union

# internal
from svgen.attribute import Attribute
from svgen.color import Colorlike
from svgen.color.resolve import get_color


class CssProperty(NamedTuple):
    """A class for interacting with css properties."""

    key: str
    value: str

    def __eq__(self, other: object) -> bool:
        """Determine if two css properties are the same."""

        if not isinstance(other, CssProperty):
            return NotImplemented
        return self.key == other.key and self.value == other.value

    @staticmethod
    def color(color: Colorlike, prop: str = "fill", **kwargs) -> "CssProperty":
        """Get a CSS property for a color."""
        return CssProperty(prop, str(get_color(color, **kwargs)))

    @staticmethod
    def decode(value: str) -> list["CssProperty"]:
        """Create css properties from a string."""

        result: list[CssProperty] = []

        value = value.strip()
        props = [x.strip() for x in value.split(";")]
        for prop in props:
            if prop:
                tokens = prop.split(":")
                assert len(tokens) == 2
                key = tokens[0].strip()
                val = tokens[1].strip()
                result.append(CssProperty(key, val))

        return result

    @property
    def encoded(self) -> str:
        """Convert this css property to a string."""
        return f"{self.key}: {self.value}"

    @staticmethod
    def encode(props: list["CssProperty"]) -> str:
        """Encode a list of css properties to a string."""
        return "; ".join(x.encoded for x in props)

    @staticmethod
    def from_dict(
        data: dict[str, Union[str, int, float]],
    ) -> list["CssProperty"]:
        """Get a list of attributes from dictionary data."""
        return [CssProperty(key, str(value)) for key, value in data.items()]


PossibleProperties = Union[
    dict[str, Union[str, int, float]], list[CssProperty], CssProperty
]


def properties(data: PossibleProperties = None) -> list[CssProperty]:
    """
    Get properties from either an existing list of properties, or dictionary
    data.
    """

    if data is None:
        data = []
    if isinstance(data, dict):
        data = CssProperty.from_dict(data)
    elif not isinstance(data, list):
        data = [data]
    return data


class Style(Attribute):
    """An interface for style attributes."""

    def __init__(self, props: PossibleProperties = None) -> None:
        """Construct a new style attribute."""

        self.properties: list[CssProperty] = properties(props)

    def add(self, props: PossibleProperties) -> None:
        """Add CSS properties to this style instance."""
        self.properties.extend(properties(props))

    def __eq__(self, other: object) -> bool:
        """Determine if two style attributes are the same."""

        if not isinstance(other, Style):
            return NotImplemented

        result = self.key == other.key
        result = result and len(self.properties) == len(other.properties)
        if result:
            props = sorted(self.properties)
            other_props = sorted(other.properties)
            for idx, prop in enumerate(props):
                if not result:
                    break
                result = result and prop == other_props[idx]

        return result

    def add_color(
        self,
        color: Colorlike,
        prop: str = "fill",
        **kwargs,
    ) -> "Style":
        """Set a style property to a color."""
        self.properties.append(CssProperty.color(color, prop=prop, **kwargs))
        return self

    @property
    def value(self) -> str:
        """Get the string value for this attribute."""
        return CssProperty.encode(self.properties)

    @classmethod
    def decode(cls: type["Style"], key: str, value: str) -> "Style":
        """Create this attribute from a string."""

        assert key == "style"
        return cls(CssProperty.decode(value))
