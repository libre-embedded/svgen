"""
A module implementing an interface for style elements.
"""

# third-party
from vcorelib import DEFAULT_ENCODING
from vcorelib.paths import find_file

# internal
from svgen import PKG_NAME
from svgen.element import Element


class Style(Element):
    """A class for html elements."""

    @staticmethod
    def cascadia_font() -> "Style":
        """Get a style element for the cascadia fonts."""

        path = find_file("cascadia.css", package=PKG_NAME, strict=True)
        assert path is not None
        with path.open("r", encoding=DEFAULT_ENCODING) as path_fd:
            return Style(text=path_fd.read())
