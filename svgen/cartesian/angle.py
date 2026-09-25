"""
A module implementing an interface for angles.
"""

# built-in
from abc import ABC, abstractmethod
from typing import Self, TypeVar

T = TypeVar("T", bound="Rotatable")


class Rotatable(ABC):
    """A generic interface for rotatable instances."""

    @abstractmethod
    def arc(self: T, count: int = 1, divisor: int = 2) -> T:
        """Rotate this angle around the circle."""


class DegreePrimitive(int, Rotatable):
    """
    A class to manage integer primitives for degrees within a 0 and 360 range.
    """

    def __new__(cls, val: int) -> Self:
        """Construct a new degree value."""
        return super().__new__(cls, val % 360)

    def rotate(self, val: int) -> "DegreePrimitive":
        """Rotate this degree instance."""
        return DegreePrimitive(self + val)

    def arc(self, count: int = 1, divisor: int = 2) -> "DegreePrimitive":
        """Rotate this angle around the circle."""
        return self.rotate(round(count * (360 / divisor)))
