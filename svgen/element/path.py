"""
A module implementing a path element.
"""

# internal
from svgen.element import Element


class Path(Element):
    """A path element."""

    @staticmethod
    def create(*cmds: str, **kwargs) -> "Path":
        """A helper for creating path elements."""
        return Path(d=" ".join(cmds), **kwargs)
