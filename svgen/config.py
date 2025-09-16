"""
A module implementing package configuration data interfaces.
"""

# built-in
import argparse

# third-party
from vcorelib.dict import GenericStrDict
from vcorelib.dict.config import Config

# internal
from svgen.color.theme.manager import DEFAULT_THEME

DEFAULT_HEIGHT = 100
DEFAULT_WIDTH = DEFAULT_HEIGHT


def initialize_config(
    config: Config | GenericStrDict,
    default_height: int = DEFAULT_HEIGHT,
    default_width: int = DEFAULT_WIDTH,
    default_theme: str = DEFAULT_THEME,
) -> None:
    """Set initial values for SVG document configurations."""

    settings = {
        "height": default_height,
        "width": default_width,
        "scripts": [],
        "grid": {},
        "background": {},
        "theme": default_theme,
    }

    if isinstance(config, Config):
        for key, val in settings.items():
            config.set_if_not(key, val)
    else:
        for key, val in settings.items():
            config.setdefault(key, val)


def add_dimension_args(parser: argparse.ArgumentParser) -> None:
    """Add dimension-related arguments to the command-line parser."""

    parser.add_argument(
        "--height",
        type=int,
        default=DEFAULT_HEIGHT,
        help=(
            "height of the document, if not specified by "
            "configuration (default: %(default)s)"
        ),
    )

    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help=(
            "width of the document, if not specified by "
            "configuration (default: %(default)s)"
        ),
    )
