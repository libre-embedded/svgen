"""
svgen - An interface for retrieving and interacting with test data.
"""

from collections.abc import Iterator

# built-in
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

# internal
from svgen import PKG_NAME


def resource(resource_name: str, *parts: str, pkg: str = __name__) -> Path:
    """Locate the path to a test resource."""

    # Can't search in other packages.
    assert pkg == __name__
    return Path(__file__).parent.joinpath("data", resource_name, *parts)


get_resource = resource


def get_config(name: str = "sample") -> Path:
    """Get the path to a test configuration."""
    return get_resource(f"{name}.json")


def get_script(name: str = "sample") -> Path:
    """Get the path to a test script."""
    return get_resource(f"{name}.py")


@contextmanager
def base_args(
    name: str = "sample", include_config: bool = True
) -> Iterator[list[str]]:
    """Get base arguments to invoke this package's command-line entry."""

    with TemporaryDirectory() as tmpdir:
        args = [PKG_NAME, "-C", tmpdir, "--images"]
        if include_config:
            args.extend(["-c", str(get_config(name))])
        args.append(str(get_script(name)))
        yield args
